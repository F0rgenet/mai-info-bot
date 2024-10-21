import asyncio
import urllib.parse
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Union

import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from loguru import logger
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed
from backend.parser.config import parser_config


class UrlWithContext(BaseModel):
    url: str
    context: dict


class Scraper(ABC):
    def __init__(self):
        self.config = parser_config
        self.session: ClientSession = None
        self.semaphore = asyncio.Semaphore(self.config.concurrent_requests)
        self.url_queue = asyncio.Queue()
        self.result_queue = asyncio.Queue()

    async def __aenter__(self):
        self.session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @retry(stop=stop_after_attempt(parser_config.retry_attempts), wait=wait_fixed(parser_config.retry_delay))
    async def fetch_html(self, url: str) -> str:
        async with self.semaphore:
            async with self.session.get(
                url, headers={"User-Agent": UserAgent().chrome},
                cookies={"schedule-group-cache": "2.0"}
            ) as response:
                response.raise_for_status()
                return await response.text()

    @staticmethod
    async def parse_html(html: str) -> BeautifulSoup:
        return BeautifulSoup(html, 'html.parser')

    async def scrape_worker(self):
        """
        Обработчик для URL-очереди. Берёт URL из очереди, обрабатывает его и помещает результат в result_queue.
        """
        while True:
            url, context = await self.url_queue.get()  # Получение задачи из очереди
            if url is None:  # Завершающий сигнал для завершения обработчиков
                break

            try:
                html = await self.fetch_html(url)
                parsed_html = await self.parse_html(html)
                await self.result_queue.put((url, context, parsed_html))
            except Exception as e:
                logger.error(f"Ошибка обработки URL {url}: {str(e)}")
                await self.result_queue.put((url, context, None))
            finally:
                self.url_queue.task_done()  # Уведомление о завершении задачи

    async def add_urls(self, urls: List[UrlWithContext]):
        """
        Добавляет URL-адреса в очередь для последующей обработки.
        """
        for url_with_context in urls:
            await self.url_queue.put((url_with_context.url, url_with_context.context))

    async def scrape(self):
        """
        Основной метод запуска обработки. Запускает обработчики очереди URL и возвращает результаты из result_queue.
        """
        workers = [asyncio.create_task(self.scrape_worker()) for _ in range(self.config.concurrent_requests)]

        await self.url_queue.join()

        for _ in workers:
            await self.url_queue.put((None, None))

        await asyncio.gather(*workers)

        while not self.result_queue.empty():
            yield await self.result_queue.get()

    @staticmethod
    async def build_url_with_params(url: str, **kwargs) -> str:
        return f"{url}{'?' if kwargs else ''}{urllib.parse.urlencode(kwargs)}"


async def build_groups_url(**kwargs) -> str:
    return await Scraper.build_url_with_params(parser_config.groups_url, **kwargs)


async def build_schedule_url(**kwargs) -> str:
    return await Scraper.build_url_with_params(parser_config.schedule_url, **kwargs)

