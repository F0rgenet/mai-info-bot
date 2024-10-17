import asyncio

from bs4 import BeautifulSoup

from parser.utils import groups_request
from loguru import logger


async def get_all_departments() -> list[str]:
    soup = await groups_request()
    elements = soup.find("select", {"id": "department"})
    departments = []
    for element in elements.findChildren("option")[1:]:
        department: str = element["value"].replace("\n", "").strip()
        if "выберите" in department.lower():
            continue
        departments.append(department)
    return departments


async def get_all_courses() -> list[int]:
    soup = await groups_request()
    elements = soup.find("select", {"id": "course"})
    courses = []
    for element in elements.findChildren("option")[2:]:
        course = element["value"].replace("\n", "").strip()
        if "выберите" in course.lower() or "все курсы" in course.lower():
            continue
        courses.append(int(course))
    return courses


async def parse_groups() -> dict[str: list[str]]:
    departments = await get_all_departments()

    groups = {}
    for department in departments:
        soup = await groups_request(department=department, course="all")
        group_elements = soup.findChildren("a", {"class": "btn-group"})
        department_groups = [element.text for element in group_elements]
        groups[department] = department_groups
    logger.debug(groups)
