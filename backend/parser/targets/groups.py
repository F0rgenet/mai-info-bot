from typing import AsyncGenerator, List, Tuple
from bs4 import BeautifulSoup
from loguru import logger

from config import backend_config
from database import get_session_generator
from database.crud import crud_group
from database.schemas import GroupCreate
from parser.scrape import url_with_parameters, scrape_target_url, scrape_target_urls


async def scrape_departments_list_page() -> BeautifulSoup:
    """
    Получает страницу выбора группы для дальнейшего парсинга выпадающего списка институтов.
    :return: BeautifulSoup объект html страницы.
    """
    logger.info(f"Скрапинг страницы институтов...")
    target_url = url_with_parameters(backend_config.source.groups_url)
    result = await scrape_target_url(target_url)
    logger.success("Страница институтов получена")
    return BeautifulSoup(result, features="lxml")


async def scrape_department_page(department: str) -> BeautifulSoup:
    target_url = url_with_parameters(backend_config.source.groups_url, department=department, course="all")
    result = await scrape_target_url(target_url)
    return BeautifulSoup(result, features="lxml")


async def scrape_departments_pages(departments: list[str]) -> AsyncGenerator[tuple[BeautifulSoup, str], None]:
    urls_with_context = []
    for department in departments:
        url = url_with_parameters(backend_config.source.groups_url, department=department, course="all")
        context = {"department": department}
        urls_with_context.append((url, context))

    async for result, context in scrape_target_urls(urls_with_context):
        yield BeautifulSoup(result, features="lxml"), context["department"]


async def extract_departments(departments_soup: BeautifulSoup) -> list[str] | None:
    """
    Извлекает институты из html страницы.
    :param departments_soup: BeautifulSoup объект html страницы.
    :return: Генератор, возвращающий названия институтов.
    """
    logger.info("Получение институтов...")
    elements = departments_soup.find("select", {"id": "department"})

    if elements is None:
        logger.warning("Не удалось найти элемент select с id 'department'")
        return

    options = elements.find_all("option")[1:]
    departments = []

    for element in options:
        department: str = element["value"].replace("\n", "").strip()
        if "выберите" in department.lower():
            continue
        departments.append(department)
    return departments


async def extract_department_groups(department_soup: BeautifulSoup) -> List[str]:
    """
    Извлекает группы института из html страницы.
    :param department_soup: BeautifulSoup объект html страницы.
    :return: Список групп института.
    """
    logger.info("Получение групп для института...")
    group_elements = department_soup.find_all("a", class_="btn-group")
    department_groups = [element.text.strip() for element in group_elements]

    if not department_groups:
        logger.warning("Группы института не найдены")
    else:
        logger.info(f"Найдено {len(department_groups)} групп(ы) института")

    return department_groups


async def populate_database() -> list[str]:
    departments_soup = await scrape_departments_list_page()
    departments = await extract_departments(departments_soup)
    all_groups = []
    async for department_soup, department in scrape_departments_pages(departments):
        department_groups = await extract_department_groups(department_soup)
        all_groups.extend([(department_group, department) for department_group in department_groups])

    async with get_session_generator() as db_session:
        for group, department in all_groups:
            group_data = GroupCreate(name=group, department=department)
            await crud_group.create_or_update(db_session, group_data)
    return [group for group, _ in all_groups]
