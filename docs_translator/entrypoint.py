from fastapi import FastAPI
from routes import router as docs_translator_router

app = FastAPI()
app.include_router(docs_translator_router)