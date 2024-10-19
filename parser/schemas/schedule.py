from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from parser.schemas.base import NamedEntityBase, NamedEntityUpdate, NamedEntity


class SubjectBase(NamedEntityBase):
    abbreviation_id: int


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
    datetime: datetime
    subject_id: int
    type_id: int
    classroom_id: int
    teacher_id: int
    group_id: int


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
