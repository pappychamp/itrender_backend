from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import (
    ENVIRONMENT,
    HOST_NAME,
    PORT_NUMBER,
    POSTGRES_DB,
    POSTGRES_PASSWORD,
    POSTGRES_USER,
)

DB_URL = "{}://{}:{}@{}:{}/{}".format(
    "postgresql+asyncpg",
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    HOST_NAME,
    PORT_NUMBER,
    POSTGRES_DB,
)
Engine = create_async_engine(DB_URL, echo=False if ENVIRONMENT == "production" else True)
Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=Engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
Base = declarative_base()


async def get_db():
    async with Session() as session:
        yield session
