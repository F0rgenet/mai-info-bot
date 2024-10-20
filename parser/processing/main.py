import asyncio

from loguru import logger

from parser.config import parser_config
from parser.database import get_session_generator, init_db
from parser.database.crud import crud_group
from parser.processing.extraction import extract_department_groups, extract_departments
from parser.processing.scraping import scrape_departments_page, scrape_groups_page
from parser.schemas import GroupCreate

concurrent_requests = parser_config.concurrent_requests


async def parse_subjects_to_database():
    logger.info("Начало парсинга предметов в базу данных...")


async def parse_group_for_department(department_name: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        groups_soup = await scrape_groups_page(department_name)
        groups = await extract_department_groups(groups_soup)

        async with get_session_generator() as db_session:
            for group in groups:
                group_data = GroupCreate(name=group, department=department_name)
                await crud_group.create_or_update(db_session, group_data)


async def parse_groups_to_database():
    logger.info("Начало парсинга групп в базу данных...")

    semaphore = asyncio.Semaphore(concurrent_requests)

    departments_soup = await scrape_departments_page()

    departments = []
    async for department_name in extract_departments(departments_soup):
        departments.append(department_name)

    await asyncio.gather(*(parse_group_for_department(department_name, semaphore) for department_name in departments))

    logger.info("Парсинг групп завершен.")


async def main():
    await init_db()
    await parse_groups_to_database()


if __name__ == "__main__":
    asyncio.run(main())
