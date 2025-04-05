from fastapi import FastAPI
from routes import router as translator_router
from contextlib import asynccontextmanager
from services import TranslationService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await TranslationService.preload_models()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(translator_router)