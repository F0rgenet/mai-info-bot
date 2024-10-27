import asyncio

from database import init_db
from parser.targets import populate_database_weeks, populate_database_groups, populate_database_subjects


async def main():
    await init_db()
    groups = await populate_database_groups()
    # await populate_database_weeks(groups[0])
    # await populate_database_subjects()


if __name__ == "__main__":
    asyncio.run(main())
