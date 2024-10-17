from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Database


class Subject(Database.BASE):
    __tablename__ = 'subjects'
    subject_id = Column(Integer, primary_key=True)
    subject = Column(String(50), nullable=False)

    entries = relationship("Entry", back_populates="subject")
