from collections.abc import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db_session
from database.repositories import (SubjectRepository, GroupRepository, TypeRepository, ClassroomRepository,
                                   TeacherRepository, EntryRepository)


def get_subject_repository(session: AsyncSession = Depends(get_db_session)) -> SubjectRepository:
    """
    Получение репозитория для объектов типа Subject.
    :param session: Сессия БД.
    :return: Репозиторий для объектов типа Subject.
    """
    return SubjectRepository(session)


def get_group_repository(session: AsyncSession = Depends(get_db_session)) -> GroupRepository:
    """
    Получение репозитория для объектов типа Group.
    :param session: Сессия БД.
    :return: Репозиторий для объектов типа Group.
    """
    return GroupRepository(session)


def get_type_repository(session: AsyncSession = Depends(get_db_session)) -> TypeRepository:
    """
    Получение репозитория для объектов типа Type.
    :param session: Сессия БД.
    :return: Репозиторий для объектов типа Type.
    """
    return TypeRepository(session)


def get_classroom_repository(session: AsyncSession = Depends(get_db_session)) -> ClassroomRepository:
    """
    Получение репозитория для объектов типа Classroom.
    :param session: Сессия БД.
    :return: Репозиторий для объектов типа Classroom.
    """
    return ClassroomRepository(session)


def get_teacher_repository(session: AsyncSession = Depends(get_db_session)) -> TeacherRepository:
    """
    Получение репозитория для объектов типа Teacher.
    :param session: Сессия БД.
    :return: Репозиторий для объектов типа Teacher.
    """
    return TeacherRepository(session)


def get_entry_repository(session: AsyncSession = Depends(get_db_session)) -> EntryRepository:
    """
    Получение репозитория для объектов типа Entry.
    :param session: Сессия БД.
    :return: Репозиторий для объектов типа Entry.
    """
    return EntryRepository(session)
