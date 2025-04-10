import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from routes.translator import router as translator_router
from services.translator import TranslationService
from logging_config import setup_logging
from repositories.translator import TranslatorRepository
from db import get_db

setup_logging(log_level=logging.WARNING, log_file="/app/app.log")


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_gen = get_db()
    db = await anext(db_gen)
    try:
        repository = TranslatorRepository(db)
        await TranslationService(repository).preload_models()
        yield
    finally:
        await db.close()


app = FastAPI(lifespan=lifespan)
app.include_router(translator_router)
