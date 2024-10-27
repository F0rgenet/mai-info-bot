from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel

from .base import NamedEntityBase, NamedEntityUpdate, NamedEntity


class SubjectBase(NamedEntityBase):
    abbreviation_id: Optional[int] = None


class Subject(SubjectBase, NamedEntity):
    pass


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(NamedEntityUpdate):
    abbreviation_id: Optional[int] = None


class AbbreviationBase(NamedEntityBase):
    short_name: str


class Abbreviation(AbbreviationBase):
    id: int

    class Config:
        from_attributes = True


class AbbreviationCreate(AbbreviationBase):
    pass


class AbbreviationUpdate(NamedEntityUpdate):
    short_name: Optional[str] = None


class TypeBase(BaseModel):
    short_name: str
    full_name: Optional[str] = None


class Type(TypeBase):
    id: int

    class Config:
        from_attributes = True


class TypeCreate(TypeBase):
    pass


class TypeUpdate(BaseModel):
    full_name: Optional[str] = None
    short_name: Optional[str] = None


class EntryBase(BaseModel):
    start_datetime: datetime
    end_datetime: datetime
    subject_id: int
    type_id: int
    classroom_id: int
    teacher_id: Optional[int] = None
    group_id: int
    week_id: int


class Entry(EntryBase):
    id: int

    class Config:
        from_attributes = True


class EntryCreate(EntryBase):
    pass


class EntryUpdate(BaseModel):
    datetime: Optional[datetime] = None
    subject_id: Optional[int] = None
    type_id: Optional[int] = None
    classroom_id: Optional[int] = None
    teacher_id: Optional[int] = None
    group_id: Optional[int] = None


class GroupBase(NamedEntityBase):
    department: str


class GroupCreate(GroupBase):
    pass


class GroupUpdate(NamedEntityUpdate):
    pass


class Group(GroupBase, NamedEntity):
    pass


class WeekBase(BaseModel):
    number: int
    start_date: date
    end_date: date


class WeekCreate(WeekBase):
    pass


class WeekUpdate(BaseModel):
    number: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


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
