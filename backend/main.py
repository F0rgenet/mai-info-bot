from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger

from api.schedule.routes import classroom_router


def include_routers(fastapi_app: FastAPI):
    fastapi_app.include_router(classroom_router)


@asynccontextmanager
async def app_lifespan(fastapi_app: FastAPI):
    logger.info("Запуск сервера...")
    try:
        # TODO: database health check
        logger.info("Подключение к базе данных успешно.")
        yield
    except Exception as exception:
        logger.error(f"Ошибка при запуске приложения: {exception}")
        raise
    finally:
        logger.info("Завершение работы приложения...")
        logger.info("База данных отключена.")


app = FastAPI(lifespan=app_lifespan)
include_routers(app)


@app.get("/")
async def root():
    return {"message": "Сервер работает!"}
