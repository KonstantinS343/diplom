from abc import ABC, abstractmethod


class FileTranslatorHandler(ABC):
    @abstractmethod
    async def parse(self): ...

    @abstractmethod
    async def translate(self, source: str, target: str): ...


class TxtTranslatorHandler(FileTranslatorHandler): ...


class PdfTranslatorHandler(FileTranslatorHandler): ...


class DocxTranslatorHandler(FileTranslatorHandler): ...
