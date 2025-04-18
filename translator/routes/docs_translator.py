from schemas.translator import TranslateFileRequest
from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from urllib.parse import quote

from services import TranslationService, BaseDocumentTranslator, OpenXmlTranslationService


router = APIRouter(tags=["docs"], prefix="/docs")


def get_openxml_service(service: TranslationService = Depends()) -> BaseDocumentTranslator:
    return OpenXmlTranslationService(service)


@router.post("/translate/")
async def translate(
    source_lang: str = Form(...),
    target_lang: str = Form(...),
    file: UploadFile = File(...),
    translator: BaseDocumentTranslator = Depends(get_openxml_service),
):
    translated_file = await translator.translate(file, source_lang, target_lang)
    encoded_filename = quote(f"translated_{file.filename}")

    return StreamingResponse(
        translated_file,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"},
    )
