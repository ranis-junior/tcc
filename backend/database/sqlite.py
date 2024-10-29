from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from contextlib import asynccontextmanager

from config.default import Config

SQLALCHEMY_DATABASE_URL = Config.sqlalchemy_database_url

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
    poolclass=AsyncAdaptedQueuePool
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, class_=AsyncSession)
Base = declarative_base()


@asynccontextmanager
async def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
