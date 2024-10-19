from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from parser.database.database import Base


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
