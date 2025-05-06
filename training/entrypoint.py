import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import router as training_router
from logging_config import setup_logging

setup_logging(log_level=logging.WARNING, log_file="/app/app.log")

app = FastAPI(
    title="Translation Training Service",
    description="API for text translation training",
    version="1.0.0",
)

# Настройка CORS
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # Production frontend
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(training_router)
