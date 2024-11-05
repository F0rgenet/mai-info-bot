import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


class Abbreviation(Base):
    __tablename__ = "abbreviations"
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    short_name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    subjects: Mapped[List["Subject"]] = relationship(back_populates="abbreviation")


class Subject(Base):
    __tablename__ = "subjects"
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    abbreviation_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("abbreviations.id"))

    abbreviation: Mapped[Optional["Abbreviation"]] = relationship(back_populates="subjects")
    entries: Mapped[List["Entry"]] = relationship(back_populates="subject")


class Classroom(Base):
    __tablename__ = "classrooms"
    name: Mapped[str] = mapped_column(String(25), nullable=False, unique=True)

    entries: Mapped[List["Entry"]] = relationship(back_populates="classroom")


class Teacher(Base):
    __tablename__ = "teachers"
    full_name: Mapped[str] = mapped_column(String(50), unique=True)

    entries: Mapped[List["Entry"]] = relationship(back_populates="teacher")


class Type(Base):
    __tablename__ = "types"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    short_name: Mapped[str] = mapped_column(String(5), nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(String(25), nullable=False, unique=True)

    entries: Mapped[List["Entry"]] = relationship(back_populates="type")


class Group(Base):
    __tablename__ = "groups"
    name: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    department: Mapped[str] = mapped_column(String(15))
    level: Mapped[str] = mapped_column(String(40))
    course: Mapped[int] = mapped_column(Integer())

    entries: Mapped[List["Entry"]] = relationship(back_populates="group")


class Entry(Base):
    __tablename__ = "entries"
    start_datetime: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    end_datetime: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    subject_id: Mapped[uuid] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    type_id: Mapped[uuid] = mapped_column(ForeignKey("types.id"), nullable=False)
    group_id: Mapped[Optional[uuid]] = mapped_column(ForeignKey("groups.id"))
    classroom_id: Mapped[Optional[uuid]] = mapped_column(ForeignKey("classrooms.id"))
    teacher_id: Mapped[Optional[uuid]] = mapped_column(ForeignKey("teachers.id"))

    subject: Mapped["Subject"] = relationship(back_populates="entries")
    group: Mapped["Group"] = relationship(back_populates="entries")
    classroom: Mapped["Classroom"] = relationship(back_populates="entries")
    teacher: Mapped["Teacher"] = relationship(back_populates="entries")
    type: Mapped["Type"] = relationship(back_populates="entries")