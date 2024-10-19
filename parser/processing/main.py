import asyncio

from loguru import logger

from parser.config import parser_config
from parser.database import get_session_generator, init_db
from parser.database.crud import crud_entry
from parser.schemas import EntryCreate
from parser.processing.scraping import ScheduleScraper
from parser.processing.extraction import parse_subjects


async def process_chunk(chunk):
    async with get_session_generator() as db_session:
        for url, soup in chunk:
            logger.info(f"Processing data from URL: {url}")
            async for subject in parse_subjects(soup):
                logger.debug(subject)
                # await crud_entry.create(db_session, EntryCreate())
        # await db_session.commit()


async def main():
    logger.info("Starting scraping process")
    chunk = []
    chunk_size = parser_config.chunk_size
    await init_db()

    async with ScheduleScraper() as scraper:
        async for url, soup in scraper.scrape():
            logger.info(f"Скрапинг {url}")
            chunk.append((url, soup))
            if len(chunk) >= chunk_size:
                await process_chunk(chunk)
                chunk = []

    if chunk:  # Process any remaining items
        await process_chunk(chunk)

    logger.info("Scraping process completed")


if __name__ == "__main__":
    asyncio.run(main())
