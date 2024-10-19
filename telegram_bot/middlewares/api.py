from typing import Callable, Dict, Any, Awaitable, cast

from aiogram import BaseMiddleware
from aiogram.types import Update, TelegramObject
import aiohttp

class UserMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Update, data: Dict[str, Any]) -> Any:
        # TODO: Api requests
        pass
