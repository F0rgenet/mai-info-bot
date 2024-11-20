import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


class Subject(Base):
    __tablename__ = "subjects"
    name: Mapped[str] = mapped_column(String(150), unique=True)
    short_name: Mapped[str] = mapped_column(String(25), nullable=True)

    entries: Mapped[List["Entry"]] = relationship(back_populates="subject", lazy="subquery")


class Classroom(Base):
    __tablename__ = "classrooms"
    name: Mapped[str] = mapped_column(String(25), unique=True)

    entries: Mapped[List["Entry"]] = relationship(back_populates="classroom", lazy="subquery")


class Teacher(Base):
    __tablename__ = "teachers"
    full_name: Mapped[str] = mapped_column(String(50), unique=True)

    entries: Mapped[List["Entry"]] = relationship(back_populates="teacher", lazy="subquery")


class Type(Base):
    __tablename__ = "types"
    short_name: Mapped[str] = mapped_column(String(5), unique=True)
    full_name: Mapped[str] = mapped_column(String(25), unique=True, nullable=True)

    entries: Mapped[List["Entry"]] = relationship(back_populates="type", lazy="subquery")


class Group(Base):
    __tablename__ = "groups"
    name: Mapped[str] = mapped_column(String(20), unique=True)
    department: Mapped[str] = mapped_column(String(15), nullable=True)
    level: Mapped[str] = mapped_column(String(40), nullable=True)
    course: Mapped[int] = mapped_column(Integer(), nullable=True)

    entries: Mapped[List["Entry"]] = relationship(back_populates="group", lazy="subquery")


class Entry(Base):
    __tablename__ = "entries"
    start_datetime: Mapped[datetime] = mapped_column(DateTime())
    end_datetime: Mapped[datetime] = mapped_column(DateTime())

    subject_id: Mapped[uuid] = mapped_column(ForeignKey("subjects.id"))
    type_id: Mapped[uuid] = mapped_column(ForeignKey("types.id"))
    group_id: Mapped[Optional[uuid]] = mapped_column(ForeignKey("groups.id"))
    classroom_id: Mapped[Optional[uuid]] = mapped_column(ForeignKey("classrooms.id"), nullable=True)
    teacher_id: Mapped[Optional[uuid]] = mapped_column(ForeignKey("teachers.id"), nullable=True)

    subject: Mapped["Subject"] = relationship(back_populates="entries", lazy="subquery")
    group: Mapped["Group"] = relationship(back_populates="entries", lazy="subquery")
    classroom: Mapped["Classroom"] = relationship(back_populates="entries", lazy="subquery")
    teacher: Mapped["Teacher"] = relationship(back_populates="entries", lazy="subquery")
    type: Mapped["Type"] = relationship(back_populates="entries", lazy="subquery")
