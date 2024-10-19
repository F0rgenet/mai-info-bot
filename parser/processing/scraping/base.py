import asyncio
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Union
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
    async def get_urls(self) -> List[Tuple[str, Dict]]:
        """
        Этот метод должен возвращать список кортежей (url, context),
        где context — это произвольная дополнительная информация для этого URL.
        """
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

    async def scrape_url(self, url: str, context: Dict) -> Tuple[str, Dict, Union[BeautifulSoup, None]]:
        """
        Скрапит URL и возвращает результат в виде кортежа (url, context, результат).
        Если произошла ошибка, результат будет None.
        """
        try:
            html = await self.fetch_html(url)
            parsed_html = await self.parse_html(html)
            return url, context, parsed_html
        except Exception as e:
            logger.error(f"Ошибка скрапинга URL {url}: {str(e)}")
            return url, context, None

    async def scrape(self):
        urls_with_contexts = await self.get_urls()
        chunk_size = self.config.chunk_size
        for i in range(0, len(urls_with_contexts), chunk_size):
            chunk = urls_with_contexts[i:i + chunk_size]
            tasks = [self.scrape_url(url, context) for url, context in chunk]
            results = await asyncio.gather(*tasks)
            for url, context, result in results:
                if result:
                    yield url, context, result
            await asyncio.sleep(self.config.chunk_delay)
