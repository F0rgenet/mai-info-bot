from collections.abc import AsyncGenerator

from loguru import logger
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import database_config


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(database_config.url)
    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as error:
            # TODO: Логировать все ошибки в loguru
            await session.rollback()
            raise
