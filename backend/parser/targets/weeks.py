from datetime import datetime, date

from bs4 import BeautifulSoup
from loguru import logger

from config import backend_config
from database import get_session_generator
from database.crud import crud_week
from database.schemas import WeekCreate
from parser.scrape import scrape_target_url, url_with_parameters


async def scrape_weeks_page(group: str) -> BeautifulSoup:
    """
    Получает страницу с неделями для дальнейшего парсинга.
    :return: BeautifulSoup объект html страницы.
    """
    logger.info("Скрапинг страницы недель...")
    target_url = url_with_parameters(backend_config.source.schedule_url, group=group)
    result = await scrape_target_url(target_url)
    return BeautifulSoup(result, features="lxml")


async def extract_weeks(group_soup: BeautifulSoup) -> dict[int, tuple[date, ...]]:
    """
    Получение информации о неделях из страницы группы.
    :param group_soup: BeautifulSoup-объект страницы группы.
    :return: Словарь, где ключ - номер недели, значение - кортеж с датами начала и конца недели.
    """
    weeks = {}
    for element in group_soup.find_all("li", class_="list-group-item"):
        week_number = int(element.find("span", class_="badge").text)
        week_dates = element.find(["a", "span"], class_=["w-100", "d-block", "text-center"])
        dates = week_dates.text.replace("\n", "").strip().split(" - ")
        weeks[week_number] = tuple([datetime.strptime(date_string, "%d.%m.%Y").date() for date_string in dates])
    return weeks


async def populate_database(group: str):
    soup = await scrape_weeks_page(group)
    weeks = await extract_weeks(soup)
    for week_number, week_dates in weeks.items():
        week_data = WeekCreate(number=week_number, start_date=week_dates[0], end_date=week_dates[1])
        async with get_session_generator() as db_session:
            await crud_week.create_or_update(db_session, week_data)