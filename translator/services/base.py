from abc import ABC, abstractmethod
from fastapi import UploadFile
from io import BytesIO


class BaseDocumentTranslator(ABC):
    @abstractmethod
    def translate(self, file: UploadFile, source_lang: str, target_lang: str) -> BytesIO:
        pass
