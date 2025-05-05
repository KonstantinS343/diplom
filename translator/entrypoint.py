import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


app = FastAPI(
    title="Translation Service",
    description="API for text translation and language processing",
    version="1.0.0",
    lifespan=lifespan
)

# Настройка CORS
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # Production frontend
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.include_router(translator_router)
app.include_router(docs_translator_router)