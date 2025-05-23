import json
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query

from services.training_support import TranslatorSupportService
from services.auth import get_current_user
from schemas import DatasetResponse, LanguageRequest, RateCardRequest

router = APIRouter(tags=["training"], prefix="/v1/api/training")


@router.post("/upload")
async def dataset_upload(
    file: UploadFile = File(...),
    source_lang: str = Form(...),
    target_lang: str = Form(...),
    service: TranslatorSupportService = Depends(),
) -> DatasetResponse:
    try:
        dataset = json.loads(await file.read())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON file: {str(e)}")

    await service.user_file_upload(dataset, source_lang, target_lang)

    return DatasetResponse(
        status="success",
        message="Dataset uploaded successfully",
    )


@router.post("/dislike")
async def dislike(
    request: RateCardRequest,
    service: TranslatorSupportService = Depends(),
    current_user: dict = Depends(get_current_user)
):
    return await service.add_dislike(request.card_id, request.collection, current_user["sub"])


@router.post("/like")
async def like(
    request: RateCardRequest,
    service: TranslatorSupportService = Depends(),
    current_user: dict = Depends(get_current_user)
):
    return await service.add_like(request.card_id, request.collection, current_user["sub"])


@router.get("/pairs")
async def pairs(
    source_lang: str = Query(..., description="Source language"),
    target_lang: str = Query(..., description="Target language"),
    service: TranslatorSupportService = Depends(),
    user: dict = Depends(get_current_user)
):
    return await service.get_language_dataset(source_lang, target_lang, user["sub"])


@router.get("/sections")
async def language_sections(service: TranslatorSupportService = Depends()):
    return await service.get_language_pairs()


@router.post("/section/create")
async def create_language_sections(
    request: LanguageRequest,
    service: TranslatorSupportService = Depends(),
):
    return await service.create_language_pair(request.source_lang, request.target_lang)
