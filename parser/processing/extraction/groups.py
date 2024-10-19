from typing import Dict, AsyncGenerator, Tuple

from bs4 import BeautifulSoup
from loguru import logger

from parser.utils import groups_request


async def get_all_departments(departments_soup: BeautifulSoup) -> list[str]:
    logger.info("Получение институтов...")
    elements = departments_soup.find("select", {"id": "department"})
    departments = []
    for element in elements.find_all("option")[1:]:
        department: str = element["value"].replace("\n", "").strip()
        if "выберите" in department.lower():
            continue
        departments.append(department)
    logger.success("Институты получены")
    return departments


async def get_all_courses(courses_soup: BeautifulSoup) -> list[int]:
    elements = courses_soup.find("select", id="course")
    courses = []
    for element in elements.find_all("option")[2:]:
        course = element["value"].replace("\n", "").strip()
        if "выберите" in course.lower() or "все курсы" in course.lower():
            continue
        courses.append(int(course))
    return courses


async def get_one_group() -> str:
    departments = await get_all_departments()
    department = departments[0]
    soup = await groups_request(department=department, course="all")
    group = soup.find("a", class_="btn-group")
    return group.text


async def parse_groups() -> AsyncGenerator[Tuple[str, list[str]], None]:
    logger.info("Запуск получения групп...")
    departments = await get_all_departments()

    for department in departments:
        logger.info(f"Получение групп: {department}")
        try:
            soup = await groups_request(department=department, course="all")
            group_elements = soup.find_all("a", class_="btn-group")
            department_groups = [element.text for element in group_elements]
            logger.success(f"Получены группы: {department}")
            yield department, department_groups
        except Exception as exception:
            logger.error(f"Ошибка при получении групп для {department}: {exception}")
