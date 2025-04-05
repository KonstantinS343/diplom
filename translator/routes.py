from schemas import TranslationRequest
from fastapi import APIRouter
from services import TranslationService

router = APIRouter(
    tags=['translate'],
    prefix='/translate'
)

@router.post("/")
async def translate(request: TranslationRequest):
    return {"translated_text": await TranslationService.translate(request.source_lang, request.target_lang, request.text)}