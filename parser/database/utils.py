from functools import wraps

from loguru import logger
from sqlalchemy.exc import IntegrityError


def handle_db_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session = kwargs.get('session')
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            logger.error(f"Ошибка целостности данных: {e}")
            if session:
                await session.rollback()
            return None
        except Exception as e:
            logger.error(f"Ошибка базы данных: {e}")
            if session:
                await session.rollback()
            return None
    return wrapper
