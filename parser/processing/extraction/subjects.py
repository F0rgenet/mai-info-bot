import locale
from collections import namedtuple
from datetime import datetime, date
from typing import Dict, Tuple, AsyncGenerator

from bs4 import PageElement, Tag, BeautifulSoup

locale.setlocale(locale.LC_TIME, 'rus')


async def get_all_weeks() -> Dict[int, Tuple[str, str]]:
    group = await get_one_group()
    soup = await schedule_request(group=group)
    weeks = {}
    for element in soup.find_all("li", class_="list-group-item"):
        week_number = int(element.find("span", class_="badge").text)
        week_dates = element.find(["a", "span"], class_=["w-100", "d-block", "text-center"])
        weeks[week_number] = tuple(week_dates.text.replace("\n", "").strip().split(" - "))
    return weeks


def process_date(target_date: str) -> date:
    target_date = target_date.lower()
    current_year = datetime.now().year
    target_date = f"{target_date} {current_year}"
    months_genitive_to_nominative = {
        "января": "январь", "февраля": "февраль", "марта": "март", "апреля": "апрель",
        "мая": "май", "июня": "июнь", "июля": "июль", "августа": "август",
        "сентября": "сентябрь", "октября": "октябрь", "ноября": "ноябрь", "декабря": "декабрь"
    }
    for full_month, nominative_month in months_genitive_to_nominative.items():
        target_date = target_date.replace(full_month, nominative_month)
    date_object = datetime.strptime(target_date, "%a, %d %B %Y").date()
    return date_object


async def get_subject_name_and_type(subject_element: Tag):
    header = subject_element.find("div")

    p_element = header.find('p')
    if not p_element:
        raise ValueError("Не найден элемент <p>")

    first_part = p_element.contents[0].get_text(separator=" ", strip=True)
    span_element = p_element.find('span', class_='text-nowrap')
    second_part = ""

    if span_element:
        second_part = span_element.contents[0].get_text(separator=" ", strip=True)
    subject_name = first_part + f" {second_part}" if second_part else ""

    badge_element = p_element.find('span', class_='badge')
    if not badge_element:
        raise ValueError("Не найден элемент <span> с классом 'badge'")
    subject_type = badge_element.get_text(separator=" ", strip=True)
    return subject_name, subject_type


async def get_subject_details(subject_element: Tag):
    items = subject_element.find("ul", class_="list-inline").find_all("li")

    time = None
    teacher = None
    classroom = None

    for item in items:
        if "–" in item.get_text():
            time = item.get_text(separator=" ", strip=True)
        elif item.find('a', class_='text-body'):
            teacher = item.get_text(separator=" ", strip=True)
        elif item.find('i', class_='fa-map-marker-alt'):
            classroom = item.get_text(separator=" ", strip=True)

    time = time.split(" – ")[0].strip()
    return time, teacher, classroom


ParsedEntryData = namedtuple('ParsedEntryData', ['datetime', 'subject_name', 'subject_type', 'teacher_name', 'classroom_name'])


async def parse_subjects(schedule_soup: BeautifulSoup) -> AsyncGenerator[ParsedEntryData, None]:
    daily_schedule_elements = schedule_soup.find_all("li", class_="step-item")
    for day_schedule_element in daily_schedule_elements:
        date_raw = day_schedule_element.find("span", class_="step-title").get_text(separator=" ", strip=True)
        date_clean = date_raw.replace("\xa0", " ")
        subjects_date = process_date(date_clean)
        subjects: PageElement = day_schedule_element.find_all("div", class_="mb-4")
        for subject in subjects:
            subject_name, subject_type = await get_subject_name_and_type(subject)
            subject_time, subject_teacher, subject_classroom = await get_subject_details(subject)
            subject_datetime = datetime.strptime(f"{subjects_date} {subject_time}", "%Y-%m-%d %H:%M")
            yield ParsedEntryData(datetime=subject_datetime,
                                  subject_name=subject_name,
                                  subject_type=subject_type,
                                  teacher_name=subject_teacher,
                                  classroom_name=subject_classroom)
