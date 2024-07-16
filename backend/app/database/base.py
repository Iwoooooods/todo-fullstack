import os
from typing import AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class DatabaseClient:
    def __init__(self):
        self._url = os.getenv("DEV_DATABASE_URL")
        self._engine = create_async_engine(self._url)
        self._async_session = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            autoflush=True
        )
        logger.info(f"Successfully connected to : {self._url}")

    async def get_db(self) -> AsyncGenerator:
        async with self._async_session() as session:
            try:
                yield session
            finally:
                await session.close()


database_client = DatabaseClient()
