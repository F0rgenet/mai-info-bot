from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Database


class Teacher(Database.BASE):
    __tablename__ = 'teachers'
    teacher_id = Column(Integer, primary_key=True)
    teacher = Column(String(50), nullable=False)

    entries = relationship("Entry", back_populates="teacher")