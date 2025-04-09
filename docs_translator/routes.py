from fastapi import UploadFile
from fastapi import APIRouter

router = APIRouter(tags=["translate-doc"], prefix="/translate-doc")


@router.post("/")
async def translate_doc(file: UploadFile):
    return {"filename": file.filename, "status": "translated"}
