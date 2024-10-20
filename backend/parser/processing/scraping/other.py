from aiohttp import ClientSession
from loguru import logger

from backend.parser.processing.scraping.base import groups_request


async def scrape_groups_page(department: str):
    logger.info(f"Скрапинг страницы групп для института {department}...")
    async with ClientSession() as session:
        return await groups_request(session, department=department, course="all")


async def scrape_departments_page():
    logger.info(f"Скрапинг страницы институтов...")
    async with ClientSession() as session:
        return await groups_request(session)
