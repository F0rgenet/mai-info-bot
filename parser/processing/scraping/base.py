import asyncio
from abc import ABC, abstractmethod
from typing import List, Union
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
from parser.config import parser_config


class Scraper(ABC):
    def __init__(self):
        self.config = parser_config
        self.session = None
        self.semaphore = asyncio.Semaphore(self.config.concurrent_requests)

    async def __aenter__(self):
        self.session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @abstractmethod
    async def get_urls(self) -> List[str]:
        pass

    @retry(stop=stop_after_attempt(parser_config.retry_attempts),
           wait=wait_exponential(multiplier=1, min=parser_config.retry_delay, max=60))
    async def fetch_html(self, url: str) -> str:
        async with self.semaphore:
            async with self.session.get(url) as response:
                response.raise_for_status()
                return await response.text()

    @staticmethod
    async def parse_html(html: str) -> BeautifulSoup:
        return BeautifulSoup(html, 'html.parser')

    async def scrape_url(self, url: str) -> Union[BeautifulSoup, None]:
        try:
            html = await self.fetch_html(url)
            return await self.parse_html(html)
        except Exception as e:
            logger.error(f"Ошибка скрапинга URL {url}: {str(e)}")
            return None

    async def scrape(self):
        urls = await self.get_urls()
        chunk_size = self.config.chunk_size
        for i in range(0, len(urls), chunk_size):
            chunk = urls[i:i + chunk_size]
            tasks = [self.scrape_url(url) for url in chunk]
            results = await asyncio.gather(*tasks)
            for url, result in zip(chunk, results):
                if result:
                    yield url, result
            await asyncio.sleep(self.config.chunk_delay)
