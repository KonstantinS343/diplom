import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from routes import router as autocomplete_router
from services import AutocomplateService
from logging_config import setup_logging

setup_logging(log_level=logging.WARNING)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await AutocomplateService.preload_model()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(autocomplete_router)
