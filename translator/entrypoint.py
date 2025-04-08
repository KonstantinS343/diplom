from fastapi import FastAPI
from routes import router as translator_router
from contextlib import asynccontextmanager
from services import TranslationService
import logging
from logging_config import setup_logging
from models import TranslatorDAO
from db import get_db

setup_logging(log_level=logging.INFO, log_file="/app/app.log")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    db_gen = get_db()
    # Извлекаем сессию из генератора
    db = await anext(db_gen)
    try:
        await TranslationService.preload_models(TranslatorDAO(), db)
        yield
    finally:
        # Закрываем сессию
        await db.close()

app = FastAPI(lifespan=lifespan)
app.include_router(translator_router)