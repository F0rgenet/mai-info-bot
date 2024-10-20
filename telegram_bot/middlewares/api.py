from typing import Callable, Dict, Any

import aiohttp
from aiogram import BaseMiddleware
from aiogram.types import Message


class FastAPIMiddleware(BaseMiddleware):
    def __init__(self, api_base_url: str):
        super().__init__()
        self.api_base_url = api_base_url

    async def make_api_request(self, endpoint: str, method: str = 'GET', params: dict = None, data: dict = None):
        """Универсальный метод для выполнения запросов к API."""
        async with aiohttp.ClientSession() as session:
            url = f'{self.api_base_url}/{endpoint}'
            if method.upper() == 'GET':
                async with session.get(url, params=params) as response:
                    return await self.handle_response(response)
            elif method.upper() == 'POST':
                async with session.post(url, json=data) as response:
                    return await self.handle_response(response)

    @staticmethod
    async def handle_response(response):
        """Обрабатывает ответ от API."""
        if response.status == 200:
            return await response.json()
        else:
            return {'error': f'API request failed with status {response.status}'}

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Any], event: Message, data: Dict[str, Any]):
        data['api_middleware'] = self
        return await handler(event, data)
