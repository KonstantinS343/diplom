import logging

from fastapi import FastAPI

from routes import router as training_router
from logging_config import setup_logging

setup_logging(log_level=logging.WARNING, log_file="/app/app.log")

app = FastAPI()
app.include_router(training_router)
