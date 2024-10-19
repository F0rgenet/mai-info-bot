from aiogram.client.session import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_fixed

from parser.config import parser_config
from parser.processing.scraping.base import groups_request


def scrape_groups_page(department: str):
    async with ClientSession() as session:
        return groups_request(session, department=department, course="all")


def scrape_departments_page():
    async with ClientSession() as session:
        return groups_request(session)
