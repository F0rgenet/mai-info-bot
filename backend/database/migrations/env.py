import asyncio
import logging
import sys
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from loguru import logger

from config import database_config
from database.models import *
from database.models.base import Base

config = context.config
config.set_main_option("sqlalchemy.url", database_config.url)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        level = logger.level(record.levelname).name if logger.level(record.levelname) else record.levelno
        logger.log(level, record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)

if config.config_file_name is not None:
    file_config = context.config.config_file_name

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Выполнить миграции в 'офлайн' режиме.

    Этот метод настраивает контекст только с URL
    и без Engine, хотя Engine здесь также может использоваться.
    Пропуская создание Engine, нам не нужно, чтобы DBAPI был доступен.

    Вызовы context.execute() в этом методе просто выводят переданную строку в
    скрипт.

    """

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Настроить контекст и выполнить миграции с использованием указанного подключения.

    Этот метод вызывает конфигурацию контекста с подключением, переданным
    как аргумент, и запускает транзакцию для выполнения миграций.

    """

    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """В этом случае мы создаем асинхронный Engine
    и связываем подключение с контекстом.

    Этот метод создает асинхронный Engine на основе конфигурации,
    устанавливает асинхронное подключение и выполняет миграции,
    используя это подключение.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Выполнить миграции в 'онлайн' режиме.

    Этот метод запускает асинхронные миграции, используя метод run_async_migrations(),
    который создает Engine, устанавливает подключение и выполняет миграции.

    """

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
