from fastapi import FastAPI
from routes import router as autocomplete_router

app = FastAPI()
app.include_router(autocomplete_router)