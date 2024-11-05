from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config import test_database_config
from database.models.base import Base


@pytest_asyncio.fixture()
async def database_session() -> AsyncGenerator[AsyncSession, None]:
    """Запустить сессию базы данных."""
    engine = create_async_engine(test_database_config.url)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    session = async_sessionmaker(engine)()
    yield session
    await session.close()
