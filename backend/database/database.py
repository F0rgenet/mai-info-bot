from contextlib import asynccontextmanager
from typing import AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError

from config import backend_config

Base = declarative_base()


engine = create_async_engine(
    backend_config.database_url,
    echo=False,
    pool_pre_ping=True,
)


async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Инициализация базы данных."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Модели базы данных успешно созданы.")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка инициализации базы данных: {e}")
        raise


async def shutdown_db():
    """Завершение работы с базой данных."""
    logger.info("Завершение работы базы данных...")
    try:
        await engine.dispose()
        logger.info("Соединения с базой данных закрыты.")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при завершении работы базы данных: {e}")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии базы данных через асинхронный генератор."""
    try:
        async with async_session() as session:
            yield session
    except SQLAlchemyError as e:
        logger.error(f"Ошибка получения сессии базы данных: {e}")
        raise


@asynccontextmanager
async def get_session_generator() -> AsyncGenerator[AsyncSession, None]:
    """Контекстный менеджер для работы с сессией базы данных."""
    session: AsyncSession = async_session()
    try:
        yield session
    except SQLAlchemyError as e:
        logger.error(f"Ошибка работы с сессией: {e}")
        await session.rollback()
        raise
    finally:
        await session.close()
