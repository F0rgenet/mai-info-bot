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
from tenacity import retry, stop_after_attempt, wait_exponential, wait_fixed
from parser.config import parser_config


class UrlWithContext(BaseModel):
    url: str
    context: dict


class Scraper(ABC):
    def __init__(self):
        self.config = parser_config
        self.session: ClientSession
        self.semaphore = asyncio.Semaphore(self.config.concurrent_requests)

    async def __aenter__(self):
        self.session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @abstractmethod
    async def get_urls(self) -> List[UrlWithContext]:
        """
        Must return a list of tuples (url, context),
        where context is any additional information for the URL.
        """
        pass

    @retry(
        stop=stop_after_attempt(parser_config.retry_attempts),
        wait=wait_exponential(multiplier=1, min=parser_config.retry_delay, max=60)
    )
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
        Scrapes the URL and returns a tuple (url, context, result).
        If an error occurs, result will be None.
        """
        try:
            html = await self.fetch_html(url)
            parsed_html = await self.parse_html(html)
            return url, context, parsed_html
        except Exception as e:
            logger.error(f"Error scraping URL {url}: {str(e)}")
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


async def request(url: str, session: ClientSession, **kwargs) -> BeautifulSoup:
    full_url = build_full_url(url, **kwargs)

    try:
        async with session.get(
                full_url,
                headers={"User-Agent": UserAgent().chrome},
                cookies={"schedule-group-cache": "2.0"}
        ) as response:
            response.raise_for_status()
            text = await response.text()
    except aiohttp.ClientError as exc:
        logger.error(f"Error during request {full_url}: {exc}")
        raise ConnectionError(f"Error during request {full_url}: {exc}")

    return BeautifulSoup(text, "html.parser")


def build_full_url(url: str, **kwargs) -> str:
    return f"{url}{'?' if kwargs else ''}{urllib.parse.urlencode(kwargs)}"


async def groups_request(session: ClientSession, **kwargs) -> BeautifulSoup:
    return await request(parser_config.groups_url, session, **kwargs)


async def schedule_request(session: ClientSession, **kwargs) -> BeautifulSoup:
    return await request(parser_config.schedule_url, session, **kwargs)
