import logging

from fastapi import FastAPI
from logging_config import setup_logging
from fastapi.middleware.cors import CORSMiddleware
from routes import router as translation_quality_router

setup_logging(log_level=logging.WARNING)


app = FastAPI(
    title="Translation Quality Service",
    description="API for text translation quality evaluation",
    version="1.0.0",
)

# Настройка CORS
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # Production frontend
    "http://localhost:4000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:4000",
]


app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(translation_quality_router)
