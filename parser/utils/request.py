import urllib.parse
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from loguru import logger
from tenacity import retry, wait_fixed, stop_after_attempt
from fake_useragent import UserAgent

from parser.config import parser_config


class SessionManager:
    def __init__(self):
        self.user_agent = UserAgent().chrome
        self.cookies = {"schedule-group-cache": "2.0"}

    def get_headers(self):
        return {"User-Agent": self.user_agent}

    def get_cookies(self):
        return self.cookies


session_manager = SessionManager()


@retry(
    stop=stop_after_attempt(parser_config.retry_attempts),
    wait=wait_fixed(parser_config.retry_delay)
)
async def __request(url: str, session: ClientSession, **kwargs) -> BeautifulSoup:
    full_url = get_full_url(url, **kwargs)

    try:
        async with session.get(
                full_url,
                headers=session_manager.get_headers(),
                cookies=session_manager.get_cookies()
        ) as response:
            response.raise_for_status()
            text = await response.text()
    except aiohttp.ClientError as exc:
        logger.error(f"Ошибка при запросе {full_url}: {exc}")
        raise ConnectionError(f"Ошибка при запросе {full_url}: {exc}")
    return BeautifulSoup(text, "html.parser")


def get_full_url(url: str, **kwargs):
    return f"{url}{'?' if kwargs else ''}{urllib.parse.urlencode(kwargs)}"


def get_groups_url(**kwargs):
    return get_full_url(parser_config.groups_url, **kwargs)


def get_schedule_url(**kwargs):
    return get_full_url(parser_config.schedule_url, **kwargs)


async def groups_request(session: ClientSession, **kwargs):
    return await __request(parser_config.groups_url, session, **kwargs)


async def schedule_request(session: ClientSession, **kwargs):
    return await __request(parser_config.schedule_url, session, **kwargs)