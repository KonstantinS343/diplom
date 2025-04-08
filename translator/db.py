from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

# Настройка подключения к базе данных
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@translator-db:5432/postgres"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Зависимость для получения сессии БД
async def get_db():
    async with async_session() as session:
        yield session
