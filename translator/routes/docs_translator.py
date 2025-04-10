from schemas.translator import TranslateFileRequest
from fastapi import APIRouter, Depends, UploadFile, File

router = APIRouter(tags=["docs"], prefix="/docs")


@router.post("translate/")
async def translate(
    request: TranslateFileRequest,
    file: UploadFile = File(...),
):
    return {"text": "OK"}
