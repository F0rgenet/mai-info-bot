from .constants import GROUPS_URL, SCHEDULE_URL
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import httpx


async def __request(url: str, **kwargs) -> BeautifulSoup:
    args = "&".join([f"{key}={str(value).replace(' ', '+')}" for key, value in kwargs.items()])
    link = f"{url}?{args}"
    # TODO: Снизить таймаут
    async with httpx.AsyncClient(timeout=30) as session:
        headers = {'user-agent': UserAgent().chrome}
        response = await session.get(link, headers=headers)
        if response.status_code != 200:
            raise ConnectionError(f"Невозможно установить подключение с {url}")
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


async def groups_request(**kwargs):
    return await __request(GROUPS_URL, **kwargs)


async def schedule_request(**kwargs):
    return await __request(SCHEDULE_URL, **kwargs)
