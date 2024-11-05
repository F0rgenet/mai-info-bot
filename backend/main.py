from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger

from database import init_db, shutdown_db
from api import groups_router


def include_routers(fastapi_app: FastAPI):
    fastapi_app.include_router(groups_router, prefix="/groups", tags=["groups"])


@asynccontextmanager
async def app_lifespan(fastapi_app: FastAPI):
    logger.info("Запуск сервера...")
    try:
        await init_db()
        logger.info("Подключение к базе данных успешно.")
        yield
    except Exception as exception:
        logger.error(f"Ошибка при запуске приложения: {exception}")
        raise
    finally:
        logger.info("Завершение работы приложения...")
        await shutdown_db()
        logger.info("База данных отключена.")


app = FastAPI(lifespan=app_lifespan)
include_routers(app)


@app.get("/")
async def root():
    return {"message": "Сервер работает!"}
