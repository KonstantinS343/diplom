import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import router as autocomplete_router
from services import AutocomplateService
from logging_config import setup_logging

setup_logging(log_level=logging.WARNING)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await AutocomplateService.preload_model()
    yield


app = FastAPI(
    title="Autocomplete Service",
    description="API for text autocomplete and language processing",
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
app.include_router(autocomplete_router)
