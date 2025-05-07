from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as user_router

app = FastAPI(
    title="User Service",
    description="API for user management",
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
app.include_router(user_router)
