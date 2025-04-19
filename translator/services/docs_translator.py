import os
import uuid
import shutil
import zipfile
from io import BytesIO
from lxml import etree as LET

import aiofiles
import asyncio
from fastapi import UploadFile, HTTPException

from services.base import BaseDocumentTranslator

NAMESPACES = {
    "docx": {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"},
    "pptx": {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"},
    "xlsx": {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"},
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
        elif ext == ".xlsx":
            return "xlsx"
        else:
            raise HTTPException(
                status_code=400,
                detail=f"File type '{ext}' is not supported. Supported types: .docx, .pptx, .xlsx",
            )

    def _get_translation_targets(self, root_dir: str, file_type: str) -> list[str]:
        if file_type == "docx":
            target_dir = os.path.join(root_dir, "word")
        elif file_type == "pptx":
            target_dir = os.path.join(root_dir, "ppt", "slides")
        elif file_type == "xlsx":
            target_dir = os.path.join(root_dir, "xl")
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
        ns_uri = ns[list(ns.keys())[0]]
        
        tag_t = f"{{{ns_uri}}}t"
        tag_r = f"{{{ns_uri}}}r"
        vert_align_tag = f".//{{{ns_uri}}}rPr/{{{ns_uri}}}vertAlign"

        try:
            async with aiofiles.open(xml_path, mode="r", encoding="utf-8") as f:
                content = await f.read()
                
            parser = LET.XMLParser(remove_blank_text=False)
            root = LET.fromstring(content.encode('utf-8'), parser)
            
            if file_type == "xlsx":
                for si in root.findall(f".//{list(ns.keys())[0]}:si", ns):
                    texts = si.findall(f".//{list(ns.keys())[0]}:t", ns)
                    full_text = "".join([t.text or "" for t in texts]).strip()
                    if full_text:
                        translated = await self.translation_service.translate(source_lang, target_lang, full_text)
                        if texts:
                            texts[0].text = translated
                            for t in texts[1:]:
                                t.text = None
            else:
                
                for t_elem in root.findall(f".//{tag_t}"):
                    r_elem = t_elem.getparent()
                    if r_elem is None or r_elem.tag != tag_r:
                        continue

                    vert_align = r_elem.find(vert_align_tag, ns)
                    if vert_align is not None:
                        continue

                    if t_elem.text and t_elem.text.strip():
                        t_elem.text = await self.translation_service.translate(
                            source_lang, target_lang, t_elem.text
                        )
            output = LET.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=False)
            async with aiofiles.open(xml_path, mode="wb") as f:
                await f.write(output)
        except LET.XMLSyntaxError:
            pass
