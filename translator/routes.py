from schemas import TranslationRequest
from entrypoint import app

@app.post("/translate/")
async def translate(request: TranslationRequest):
    return {"translated_text": f"{request.text} -> {request.target_lang}"}