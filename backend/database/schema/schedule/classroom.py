from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class ClassroomBase(BaseModel):
    """
    Схема базы данных для записи.
    """
    name: str


class ClassroomCreate(ClassroomBase):
    """
    Схема базы данных для создания записи.
    """
    pass


class ClassroomCreateBatch(BaseModel):
    """
    Схема базы данных для создания нескольких записей.
    """
    classrooms: List[ClassroomCreate]


class ClassroomUpdate(ClassroomBase):
    """
    Схема базы данных для обновления записи.
    """
    name: Optional[str] = None


class ClassroomResponse(ClassroomBase):
    """
    Схема базы данных для ответа на запрос по ID записи.
    """
    id: UUID

    class Config:
        from_attributes = True
