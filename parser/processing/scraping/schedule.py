from typing import List, Tuple, Dict
from .base import Scraper, UrlWithContext
from parser.database.crud import crud_group, crud_week
from parser.database import get_session_generator


class ScheduleScraper(Scraper):
    async def get_urls(self) -> List[UrlWithContext]:
        # TODO: Сделать возвращаемый тип namedtuple с неделей и группой
        async with get_session_generator() as db_session:
            groups = await crud_group.get_all_names(db_session)
            weeks = await crud_week.get_all_numbers(db_session)

        urls = []
        for group in groups:
            for week in weeks:
                url = f"{self.config.schedule_url}?group={group}&week={week}"
                urls.append(UrlWithContext(url=url, context={"week": week, "group": group}))
        return urls
