import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config import test_database_config
from database.models.base import Base


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest_asyncio.fixture(scope="session")
def engine():
    """Создание и возвращение engine для всех тестов."""
    engine = create_async_engine(test_database_config.url)
    yield engine


@pytest_asyncio.fixture(scope="function")
async def database_session(engine) -> AsyncSession:
    """Запустить сессию базы данных для каждого теста."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    session = async_sessionmaker(engine)()
    yield session
    await session.close()
