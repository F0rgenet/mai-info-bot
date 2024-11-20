from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from api.schedule.dependencies import get_subject_repository
from database.repositories import SubjectRepository
from api.schedule.model import Subject, SubjectInDB

router = APIRouter(prefix="/classrooms", tags=["classrooms"])


SubjectRepositoryDependency = Annotated[
    SubjectRepository,
    Depends(get_subject_repository)
]


@router.get("/{id}", response_model=Subject)
async def get_classroom(classroom_id: UUID, repository: SubjectRepositoryDependency):
    """
    Получение объекта Classroom по ID.
    """
    subject = await repository.get_by_id(classroom_id)
    if subject:
        return subject
    else:
        raise ValueError(f"Объект типа Classroom с ID {classroom_id} не найден")


@router.get("/", response_model=Subject)
async def get_classroom_by_filters(name: str, short_name: str, repository: SubjectRepositoryDependency):
    """
    Поиск объекта Classroom по названию.
    """
    # TODO: Переписать get в репозиториях, чтобы он принимал фильтры
    subject = await repository.get_by_name(name)
    if subject:
        return subject
    else:
        raise ValueError(f"Объект типа Classroom с названием {name} не найден")


@router.get("/", response_model=list[Subject])
async def get_all_classrooms(repository: SubjectRepositoryDependency):
    """
    Получение списка всех объектов Classroom.
    """
    subjects = await repository.get_all()
    return subjects


@router.post("/", response_model=SubjectInDB)
async def create_classroom(subject: SubjectInDB, repository: SubjectRepositoryDependency):
    """
    Создание объекта Classroom.
    """
    created_subject = await repository.create(subject.name, subject.short_name)
    return created_subject


@router.put("/", response_model=SubjectInDB)
async def get_or_create_classroom(subject: SubjectInDB, repository: SubjectRepositoryDependency):
    """
    Получение или создание объекта Classroom.
    """
    created_subject = await repository.get_or_create(subject.name, subject.short_name)
    return created_subject


@router.delete("/{id}", response_model=Subject)
async def delete_classroom(classroom_id: UUID, repository: SubjectRepositoryDependency):
    """
    Удаление объекта Classroom по ID.
    """
    subject = await repository.delete(classroom_id)
    if subject:
        return subject
    else:
        raise ValueError(f"Объект типа Classroom с ID {classroom_id} не найден")
