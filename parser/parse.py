import asyncio
from datetime import datetime

from loguru import logger

from parser.processing.extraction import parse_groups, get_all_weeks

from parser.database import init_db, get_session, get_session_generator
from parser.database.crud import crud_week, crud_group
from parser.schemas import WeekCreate, GroupCreate
from parser.utils import get_schedule_url


async def parse_groups_to_database():
    async with get_session() as db_session:
        async for department, groups_list in parse_groups():
            for group in groups_list:
                group_data = GroupCreate(name=group, department=department)
                await crud_group.create(db_session, group_data)


async def parse_weeks_to_database():
    logger.info("Начало парсинга недель...")
    weeks = await get_all_weeks()
    async with get_session_generator() as db_session:
        for number, dates in weeks.items():
            start_date = datetime.strptime(dates[0], "%d.%m.%Y").date()
            end_date = datetime.strptime(dates[1], "%d.%m.%Y").date()
            week_data = WeekCreate(number=number, start_date=start_date, end_date=end_date)
            await crud_week.create(db_session, week_data)


async def parse_subjects_to_database(use_database_groups: bool = False, use_database_weeks: bool = False):
    logger.info("Начало парсинга предметов...")
    groups = []
    if not use_database_groups:
        async for _, groups_list in parse_groups():
            groups.extend(groups_list)
    else:
        async with get_session_generator() as db_session:
            groups = await crud_group.get_all_names(db_session)

    if not use_database_weeks:
        weeks = await get_all_weeks()
    else:
        async with get_session_generator() as db_session:
            weeks = await crud_week.get_all_numbers(db_session)

    target_urls = []
    for group in groups:
        for week in weeks:
            target_urls.append(get_schedule_url(group=group, week=week))
    logger.debug(len(target_urls))


async def main():
    await init_db()
    await parse_weeks_to_database()
    # await parse_subjects_to_database(True, True)


if __name__ == "__main__":
    asyncio.run(main())
