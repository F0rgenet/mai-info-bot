from loguru import logger
import os


os.makedirs("logs", exist_ok=True)

logger.add("logs/{time:YYYY-MM-DD}.log", rotation="1 day", retention="7 days", level="DEBUG",
           format="{time} {level} {message}")


# TODO: Добавить логирование для всех модулей
# TODO: Добавить уровни логирования исходя из конфигурации запуска


__all__ = ["logger"]
