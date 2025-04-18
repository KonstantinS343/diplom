import logging

from fastapi import FastAPI
from logging_config import setup_logging
from routes import router as translation_quality_router

setup_logging(log_level=logging.WARNING)


app = FastAPI()
app.include_router(translation_quality_router)
