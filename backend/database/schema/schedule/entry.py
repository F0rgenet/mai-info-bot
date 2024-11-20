from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


class EntryBase(BaseModel):
    """
    Схема базы данных для записи.
    """
    start_datetime: datetime = Field(default_factory=datetime.now)
    end_datetime: datetime = Field(default_factory=datetime.now)

    subject_id: UUID
    type_id: UUID
    group_id: UUID
    classroom_id: Optional[UUID]
    teacher_id: Optional[UUID]


class EntryCreate(EntryBase):
    """
    Схема базы данных для создания записи.
    """
    pass


class EntryUpdate(EntryBase):
    """
    Схема базы данных для обновления записи.
    """
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    subject_id: Optional[int] = None
    type_id: Optional[int] = None
    classroom_id: Optional[int] = None
    teacher_id: Optional[int] = None
    group_id: Optional[int] = None


class EntryRelationsCreate(BaseModel):
    """
    Схема базы данных для создания записи с указанными отношениями.
    """
    start_datetime: datetime = Field(default_factory=datetime.now)
    end_datetime: datetime = Field(default_factory=datetime.now)
    subject_name: str
    type_short_name: str
    group_name: str
    classroom: Optional[str]
    teacher_full_name: Optional[str]


class EntryRelationsCreateBatch(BaseModel):
    """
    Схема базы данных для создания нескольких записей с указанными отношениями.
    """
    entries: List[EntryRelationsCreate]


class EntryResponse(EntryBase):
    """
    Схема базы данных для ответа на запрос по ID записи.
    """
    id: UUID

    class Config:
        from_attributes = True
