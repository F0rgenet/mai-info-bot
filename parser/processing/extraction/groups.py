from typing import AsyncGenerator, List, Tuple
from bs4 import BeautifulSoup
from loguru import logger


async def extract_departments(departments_soup: BeautifulSoup) -> AsyncGenerator[Tuple[str], None]:
    logger.info("Начинаю получение институтов...")
    elements = departments_soup.find("select", {"id": "department"})

    if elements is None:
        logger.warning("Не удалось найти элемент select с id 'department'")
        return

    options = elements.find_all("option")[1:]

    valid_departments_count = 0
    for element in options:
        department: str = element["value"].replace("\n", "").strip()
        if "выберите" in department.lower():
            continue

        logger.debug(f"Найден институт: {department}")
        yield department
        valid_departments_count += 1

    logger.success(f"Институты получены: {valid_departments_count}")


async def extract_courses(courses_soup: BeautifulSoup) -> AsyncGenerator[int, None]:
    logger.info("Начинаю получение курсов...")
    elements = courses_soup.find("select", id="course")

    if elements is None:
        logger.warning("Не удалось найти элемент select с id 'course'")
        return

    options = elements.find_all("option")[2:]

    valid_course_count = 0
    for element in options:
        course = element["value"].replace("\n", "").strip()
        if "выберите" in course.lower() or "все курсы" in course.lower():
            continue

        logger.debug(f"Найден курс: {course}")
        yield int(course)
        valid_course_count += 1

    logger.success(f"Курсы получены: {valid_course_count}")


async def extract_department_groups(groups_soup: BeautifulSoup) -> List[str]:
    logger.info("Начинаю получение групп для института..")
    group_elements = groups_soup.find_all("a", class_="btn-group")
    department_groups = [element.text.strip() for element in group_elements]

    if not department_groups:
        logger.warning("Группы института не найдены")
    else:
        logger.info(f"Найдено {len(department_groups)} групп(ы) института")

    return department_groups
