from pydantic import BaseModel


class TranslationQualityRequest(BaseModel):
    source_text: str
    translated_text: str
    source_lang: str
    target_lang: str
