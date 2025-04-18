import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from routes.translator import router as translator_router
from routes.docs_translator import router as docs_translator_router
from services.translator import TranslationService
from logging_config import setup_logging
from repositories.translator import TranslatorRepository
from db import async_session

setup_logging(log_level=logging.WARNING, log_file="/app/app.log")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session() as db:  # Use async_session directly
        repository = TranslatorRepository(db)
        await TranslationService(repository).preload_models()
        yield


app = FastAPI(lifespan=lifespan)
app.include_router(translator_router)
app.include_router(docs_translator_router)
