from schemas import TranslationRequest
from fastapi import APIRouter, Depends
from services import TranslationService
from models import TranslatorDAO
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db

router = APIRouter(
    tags=['translate'],
    prefix='/translate'
)

@router.post("/")
async def translate(request: TranslationRequest, translator_dao: TranslatorDAO = Depends(), db: AsyncSession = Depends()):
    return {"translated_text": await TranslationService.translate(request.source_lang, request.target_lang, request.text, translator_dao, db)}