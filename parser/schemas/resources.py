from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .base import NamedEntityBase, NamedEntityUpdate, NamedEntity


class GroupBase(NamedEntityBase):
    pass


class GroupCreate(GroupBase):
    pass


class GroupUpdate(NamedEntityUpdate):
    pass


class Group(GroupBase, NamedEntity):
    pass


class WeekBase(BaseModel):
    number: int
    start_date: datetime
    end_date: datetime


class WeekCreate(WeekBase):
    pass


class WeekUpdate(BaseModel):
    number: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class Week(WeekBase):
    class Config:
        from_attributes = True


class TeacherBase(BaseModel):
    full_name: str


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    full_name: Optional[str] = None


class Teacher(TeacherBase):
    class Config:
        from_attributes = True


class ClassroomBase(NamedEntityBase):
    pass


class ClassroomCreate(ClassroomBase):
    pass


class ClassroomUpdate(NamedEntityUpdate):
    pass


class Classroom(ClassroomBase):
    pass
