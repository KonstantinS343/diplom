from schemas.translator import TranslationRequest
from fastapi import APIRouter, Depends
from services.translator import TranslationService

router = APIRouter(tags=["translate"], prefix="/translate")


@router.post("/")
async def translate(request: TranslationRequest, service: TranslationService = Depends()):
    return {"text": await service.translate(request.source_lang, request.target_lang, request.text)}
