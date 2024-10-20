from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from backend.database.database import Base


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)

    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    subject = relationship("Subject", back_populates="entry", lazy="selectin")

    type_id = Column(Integer, ForeignKey("types.id"), nullable=False)
    type = relationship("Type", back_populates="entry", lazy="selectin")

    classroom_id = Column(Integer, ForeignKey("classrooms.id"))
    classroom = relationship("Classroom", back_populates="entry", lazy="selectin")

    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="entry", lazy="selectin")

    week_id = Column(Integer, ForeignKey("weeks.id"), nullable=False)
    week = relationship("Week", back_populates="entry")

    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    group = relationship("Group", back_populates="entry", lazy="selectin")


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    subject = Column(String(50), nullable=False)

    abbreviation_id = Column(Integer, ForeignKey("abbreviations.id"))
    abbreviation = relationship("Abbreviation", back_populates="entry", lazy="selectin")

    entry = relationship("Entry", back_populates="subject")


class Abbreviation(Base):
    __tablename__ = "abbreviations"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)

    entry = relationship("Subject", back_populates="abbreviation")


class Type(Base):
    __tablename__ = 'types'
    id = Column(Integer, primary_key=True)
    short_name = Column(String(25), nullable=False, unique=True)
    full_name = Column(String(25))

    entry = relationship("Entry", back_populates="type")


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    department = Column(String(30))

    entry = relationship("Entry", back_populates="group")


class Week(Base):
    __tablename__ = 'weeks'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    entry = relationship("Entry", back_populates="week")


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(50), nullable=False)

    entry = relationship("Entry", back_populates="teacher")


class Classroom(Base):
    __tablename__ = 'classrooms'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)

    entry = relationship("Entry", back_populates="classroom")
