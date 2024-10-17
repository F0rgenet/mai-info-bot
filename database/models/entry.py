from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Database


class Entry(Database.BASE):
    __tablename__ = 'entries'
    entry_id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    week = Column(Integer, nullable=False)

    subject_id = Column(Integer, ForeignKey("subjects.subject_id"), nullable=False)
    subject = relationship("Subject", back_populates="entries", lazy="selectin")
    type_id = Column(Integer, ForeignKey("types.type_id"), nullable=False)
    type = relationship("Type", back_populates="entries", lazy="selectin")
    classroom_id = Column(Integer, ForeignKey("classrooms.classroom_id"))
    classroom = relationship("Classroom", back_populates="entries", lazy="selectin")
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id"), nullable=False)
    teacher = relationship("Teacher", back_populates="entries", lazy="selectin")
