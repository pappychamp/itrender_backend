import os
from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
HOST_NAME = os.environ.get("HOST_NAME")
PORT_NUMBER = os.environ.get("PORT_NUMBER")

DB_URL = "{}://{}:{}@{}:{}/{}".format(
    "postgresql+asyncpg",
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    HOST_NAME,
    PORT_NUMBER,
    POSTGRES_DB,
)
Engine = create_async_engine(DB_URL, echo=True)
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
