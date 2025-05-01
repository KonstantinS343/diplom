from pydantic import BaseModel


class DatasetResponse(BaseModel):
    status: str
    message: str


class LanguageRequest(BaseModel):
    source_lang: str
    target_lang: str
