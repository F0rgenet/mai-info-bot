from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Subject(BaseModel):
    id: UUID
    name: str
    short_name: str

    class Config:
        from_attributes = True


class SubjectInDB(Subject):
    id: UUID


class SubjectPayload(BaseModel):
    name: str = Field(..., max_length=255)
    short_name: str = Field(..., max_length=255)
