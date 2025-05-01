from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from db import get_db
from models import Language


class TranslatorRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.db = db

    async def add_language(self, lang_name: str, lang_iso: str):
        language = Language(
            language=lang_name,
            iso=lang_iso,
        )
        self.db.add(language)
        await self.db.commit()
        return language

    async def get_languages(self):
        query = select(Language)
        results = await self.db.execute(query)

        languages_mapping = {}

        for language_item in results.scalars().all():
            languages_mapping[language_item.iso] = language_item.language

        return languages_mapping
