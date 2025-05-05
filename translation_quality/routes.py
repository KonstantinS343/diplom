from fastapi import APIRouter, Depends

from services import TranslationQualityService, TranslationService
from schemas import TranslationQualityRequest
from config import translator_settings


router = APIRouter(tags=["translation_quality"], prefix="/v1/api/translation")


@router.post("/quality")
async def highlight_differences(
    request: TranslationQualityRequest,
    service: TranslationQualityService = Depends(),
    translator_service: TranslationService = Depends(
        lambda: TranslationService(translator_settings.service_api)
    ),
):
    """
    Highlight differences between original and translated text.
    """
    return await service.highlight_differences(
        request.translated_text,
        await translator_service.translate(
            request.source_text, request.target_lang, request.source_lang
        ),
    )
