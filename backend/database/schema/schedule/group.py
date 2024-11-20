from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class GroupBase(BaseModel):
    """
    Схема базы данных для записи.
    """
    name: str
    department: Optional[str]
    level: Optional[str]
    course: Optional[int]


class GroupCreate(GroupBase):
    """
    Схема базы данных для создания записи.
    """
    pass


class GroupCreateBatch(BaseModel):
    """
    Схема базы данных для создания нескольких записей.
    """
    groups: List[GroupCreate]


class GroupUpdate(GroupBase):
    """
    Схема базы данных для обновления записи.
    """
    name: Optional[str] = None
    department: Optional[str] = None
    level: Optional[str] = None
    course: Optional[int] = None


class GroupResponse(GroupBase):
    """
    Схема базы данных для ответа на запрос по ID записи.
    """
    id: UUID

    class Config:
        from_attributes = True
