import asyncio

from loguru import logger

from parser.utils import schedule_request
from parser.targets.groups import get_one_group


async def get_all_weeks():
    group = await get_one_group()
    soup = await schedule_request(group=group)
    logger.debug(soup.findChildren("li", {"class": "list-group-item"}))


async def parse_subjects(group: str, week: int) -> list[int]:
    pass


if __name__ == "__main__":
    asyncio.run(get_all_weeks())
