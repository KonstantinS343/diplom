from sqlalchemy import select
from sqlalchemy import Column, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from db import get_db

Base = declarative_base()

class Language(Base):
    __tablename__ = "languages"

    language = Column(String, primary_key=True)
    iso = Column(String(2), unique=True, nullable=False)
    

class TranslatorDAO:
    async def add_language(self, lang_name: str, lang_iso: str, db: AsyncSession):
        language = Language(
            language=lang_name,
            iso=lang_iso,
        )
        db.add(language)
        await db.commit()
        return language

    async def get_languages(self, db: AsyncSession):
        query = select(Language)
        results = await db.execute(query)
        
        languages_mapping = {}
        
        for language_item in results.scalars().all():
            languages_mapping[language_item.iso] = language_item.language
        
        return languages_mapping