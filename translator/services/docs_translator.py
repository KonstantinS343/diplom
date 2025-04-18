import os
import uuid
import shutil
import zipfile
from io import BytesIO
from xml.etree import ElementTree as ET

import aiofiles
import asyncio
from fastapi import UploadFile

from services.base import BaseDocumentTranslator

NAMESPACES = {
    "docx": {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"},
    "pptx": {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"},
}


class OpenXmlTranslationService(BaseDocumentTranslator):
    def __init__(self, translation_service):
        self.translation_service = translation_service

    async def translate(self, file: UploadFile, source_lang: str, target_lang: str) -> BytesIO:
        ext = os.path.splitext(file.filename)[1].lower()
        file_type = self._detect_file_type(ext)

        temp_dir = f"/tmp/openxml_{uuid.uuid4().hex}"
        os.makedirs(temp_dir, exist_ok=True)

        file_bytes = await file.read()
        input_io = BytesIO(file_bytes)

        await asyncio.to_thread(self._unzip, input_io, temp_dir)

        translate_targets = self._get_translation_targets(temp_dir, file_type)
        tasks = [
            self._translate_xml(path, file_type, source_lang, target_lang)
            for path in translate_targets
        ]
        await asyncio.gather(*tasks)

        output_io = await asyncio.to_thread(self._zip, temp_dir)
        shutil.rmtree(temp_dir)
        return output_io

    def _detect_file_type(self, ext: str) -> str:
        if ext == ".docx":
            return "docx"
        elif ext == ".pptx":
            return "pptx"
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def _get_translation_targets(self, root_dir: str, file_type: str) -> list[str]:
        if file_type == "docx":
            target_dir = os.path.join(root_dir, "word")
            tag = "w:t"
        elif file_type == "pptx":
            target_dir = os.path.join(root_dir, "ppt", "slides")
            tag = "a:t"
        else:
            return []

        result = []
        for dirpath, _, filenames in os.walk(target_dir):
            for filename in filenames:
                if filename.endswith(".xml"):
                    result.append(os.path.join(dirpath, filename))
        return result

    def _unzip(self, input_io: BytesIO, extract_path: str):
        with zipfile.ZipFile(input_io) as z:
            z.extractall(extract_path)

    def _zip(self, temp_dir: str) -> BytesIO:
        output_io = BytesIO()
        with zipfile.ZipFile(
            output_io, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True
        ) as new_zip:
            for folder, _, files in os.walk(temp_dir):
                for name in files:
                    path = os.path.join(folder, name)
                    arcname = os.path.relpath(path, temp_dir)
                    new_zip.write(path, arcname)
        output_io.seek(0)
        return output_io

    async def _translate_xml(
        self, xml_path: str, file_type: str, source_lang: str, target_lang: str
    ):
        ns = NAMESPACES[file_type]
        tag = list(ns.keys())[0] + ":t"

        try:
            async with aiofiles.open(xml_path, mode="r", encoding="utf-8") as f:
                content = await f.read()
            tree = ET.ElementTree(ET.fromstring(content))
            root = tree.getroot()
            for t in root.findall(f".//{tag}", ns):
                if t.text and t.text.strip():
                    t.text = await self.translation_service.translate(
                        source_lang, target_lang, t.text
                    )
            output = ET.tostring(root, encoding="utf-8", xml_declaration=True)
            async with aiofiles.open(xml_path, mode="wb") as f:
                await f.write(output)
        except ET.ParseError:
            pass
