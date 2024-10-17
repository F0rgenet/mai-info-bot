from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Database


class Classroom(Database.BASE):
    __tablename__ = 'classrooms'
    classroom_id = Column(Integer, primary_key=True)
    classroom = Column(String(25), nullable=False)

    entries = relationship("Entry", back_populates="classroom")
