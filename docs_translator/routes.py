from fastapi import UploadFile
from entrypoint import app

@app.post("/translate-doc/")
async def translate_doc(file: UploadFile):
    return {"filename": file.filename, "status": "translated"}