import asyncio
from collections import namedtuple
from typing import AsyncGenerator, List, Tuple
from bs4 import BeautifulSoup
from loguru import logger

from config import backend_config
from database import get_session_generator
from database.crud import crud_group
from database.schemas import GroupCreate
from parser.scrape import url_with_parameters, scrape_target_url, scrape_target_urls


async def scrape_groups_page() -> List[dict]:
    """
    Получает страницу выбора группы для дальнейшего парсинга выпадающего списка институтов.
    :return: BeautifulSoup объект html страницы.
    """
    logger.info(f"Скрапинг страницы групп...")
    target_url = url_with_parameters(backend_config.source.groups_url)
    result = await scrape_target_url(target_url, as_json=True)
    logger.success("Страница групп получена")
    return result


async def extract_groups(data: List[dict]) -> List[GroupCreate]:
    """
    Извлекает группы института из html страницы.
    :param data: Json с информацией о группах.
    :return: Генератор для каждой группы.
    """
    logger.info("Получение групп...")
    groups = []

    for group_dict in data:
        name = group_dict["name"]
        department = group_dict["fac"]
        level = group_dict["level"]
        course = group_dict["course"]
        groups.append(GroupCreate(name=name, department=department, level=level, course=course))
    return groups


async def write_to_database(group: GroupCreate):
    async with get_session_generator() as db_session:
        await crud_group.create_or_update(db_session, group)


async def populate_database() -> list[str]:
    groups_data = await scrape_groups_page()
    tasks = []
    group_names = []
    for group in await extract_groups(groups_data):
        group_names.append(group.name)
        tasks.append(write_to_database(group))
    logger.success("Данные о группах собраны, запись в базу данных...")
    await asyncio.gather(*tasks)
    return group_names