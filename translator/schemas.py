from pydantic import BaseModel

class TranslationRequest(BaseModel):
    text: str
    target_lang: str