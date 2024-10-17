from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Database


class Type(Database.BASE):
    __tablename__ = 'types'
    type_id = Column(Integer, primary_key=True)
    type = Column(String(25), nullable=False)

    entries = relationship("Entry", back_populates="type")