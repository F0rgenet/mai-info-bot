import asyncio
from datetime import datetime
import hashlib
from collections import namedtuple
from typing import List, Tuple, AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from config import backend_config
from database import get_session_generator
from database.crud import crud_group, crud_classroom, crud_teacher, crud_type, crud_subject, crud_entry, \
    crud_week
from database.schemas import ClassroomCreate, TeacherCreate, TypeCreate, SubjectCreate, EntryCreate
from parser.scrape import scrape_target_urls, url_with_parameters


async def scrape_schedule_api_pages(target_groups: List[str]) -> (AsyncGenerator[tuple[dict, dict], None] |
                                                                  AsyncGenerator[tuple[None, None], None]):
    logger.info(f"Скрапинг страниц API расписания")
    urls_with_context = []
    for group in target_groups:
        group_hash = hashlib.md5(group.encode()).hexdigest()
        url = f"{backend_config.source.api_url}/{group_hash}.json"
        context = {"group": group}
        urls_with_context.append((url, context))

    async for result, context in scrape_target_urls(urls_with_context, as_json=True):
        yield result, context


SubjectData = namedtuple("SubjectData", ["name", "datetime_start", "datetime_end", "teacher", "type", "classroom"])


def extract_subjects(schedule_json: dict) -> List[SubjectData]:
    """
    Парсинг предметов из страницы расписания.
    :param schedule_json: Объект страницы расписания.
    :return: Список предметов.
    """
    if not schedule_json:
        return

    subjects = []

    schedule_json.pop("group")
    for schedule_date, schedule_data in schedule_json.items():
        for subject in schedule_data["pairs"].values():
            subject: dict
            if "name" not in subject:
                name, subject = list(subject.items())[0]
            else:
                name = subject["name"]
            time_start = subject["time_start"]
            time_end = subject["time_end"]

            datetime_start = datetime.strptime(f"{schedule_date} {time_start}", "%d.%m.%Y %H:%M:%S")
            datetime_end = datetime.strptime(f"{schedule_date} {time_end}", "%d.%m.%Y %H:%M:%S")

            teacher = list(subject["lector"].values())[0]
            subject_type = list(subject["type"].keys())[0]
            classroom = list(subject["room"].values())[0]
            subjects.append(SubjectData(name, datetime_start, datetime_end, teacher, subject_type, classroom))
    return subjects


async def create_subject(subject: SubjectData, group: str):
    async with get_session_generator() as db_fetch_session:
        group_id = (await crud_group.get_by_name(db_fetch_session, group)).id
        week = await crud_week.get_by_datetime(db_fetch_session, subject.datetime_start)
        if not week:
            logger.error(f"Дата и время пары не попадает в учебные недели: {subject.datetime_start} {group}")
            return

    async with get_session_generator() as db_subject_session:
        subject_data = SubjectCreate(name=subject.name)
        subject_id = (await crud_subject.create_or_update(db_subject_session, subject_data)).id

    async with get_session_generator() as db_type_session:
        type_data = TypeCreate(short_name=subject.type if subject.type != "Экзамен" else "ЭКЗ")
        type_id = (await crud_type.create_or_update(db_type_session, type_data)).id

    async with get_session_generator() as db_classroom_session:
        classroom_data = ClassroomCreate(name=subject.classroom)
        classroom_id = (await crud_classroom.create_or_update(db_classroom_session, classroom_data)).id

        if subject.teacher:
            async with get_session_generator() as db_teacher_session:
                teacher_data = TeacherCreate(full_name=subject.teacher)
                teacher_id = (await crud_teacher.create_or_update(db_teacher_session, teacher_data)).id
        else:
            teacher_id = None

    async with get_session_generator() as db_entry_session:
        entry_data = EntryCreate(start_datetime=subject.datetime_start, end_datetime=subject.datetime_end,
                                 subject_id=subject_id, type_id=type_id, classroom_id=classroom_id,
                                 teacher_id=teacher_id, group_id=group_id, week_id=week.id)
        subject = await crud_entry.create_or_update(db_entry_session, entry_data)
        logger.success(subject)


async def populate_database():
    tasks = []
    async with get_session_generator() as db_session:
        target_groups = await crud_group.get_all_names(db_session)
    async for schedule_json, context in scrape_schedule_api_pages(target_groups):
        if not context:
            continue
        logger.info(f"Получение расписания группы {context['group']}")
        subjects = extract_subjects(schedule_json)

        for subject in subjects:
            await create_subject(subject, context['group'])

