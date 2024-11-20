from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class TypeBase(BaseModel):
    """
    Схема базы данных для записи.
    """
    short_name: str
    full_name: Optional[str]


class TypeCreate(TypeBase):
    """
    Схема базы данных для создания записи.
    """
    pass


class TypeCreateBatch(BaseModel):
    """
    Схема базы данных для создания нескольких записей.
    """
    types: List[TypeCreate]


class TypeUpdate(TypeBase):
    """
    Схема базы данных для обновления записи.
    """
    short_name: Optional[str] = None
    full_name: Optional[str] = None


class TypeResponse(TypeBase):
    """
    Схема базы данных для ответа на запрос по ID записи.
    """
    id: UUID

    class Config:
        from_attributes = True
