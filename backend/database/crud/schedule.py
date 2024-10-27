from datetime import datetime

from loguru import logger

from .base import CRUDBase
from typing import List, Any, Sequence

from rapidfuzz.distance import Levenshtein
from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Entry, Subject, Type
from database.crud.base import CRUDWithName
from database.models import Group, Week, Teacher, Classroom


class CRUDEntry(CRUDBase):
    async def get_anomalies(self, session: AsyncSession) -> Sequence[Row[Any] | RowMapping | Any]:
        query = select(self.model).where(self.model.type_id > 4)
        result = await session.execute(query)
        return result.scalars().all()


class CRUDSubject(CRUDBase):
    pass


class CRUDType(CRUDBase):
    async def get_by_short_name(self, session: AsyncSession, short_name: str) -> Type:
        query = select(self.model).where(self.model.short_name == short_name)
        result = await session.execute(query)
        data = result.scalars().first()
        if not data:
            logger.warning(f"В базе данных не найден тип сокращения: {short_name}")
        return data

    async def get_by_full_name(self, session: AsyncSession, full_name: str) -> Type:
        query = select(self.model).where(self.model.full_name == full_name)
        result = await session.execute(query)
        data = result.scalars().first()
        if not data:
            logger.warning(f"В базе данных не найден тип: {full_name}")
        return data


class CRUDGroup(CRUDWithName[Group]):
    async def find_closest(self, session: AsyncSession, group_name: str) -> str:
        names = await self.get_all_names(session)
        return min(names, key=lambda value: Levenshtein.distance(group_name, value))


class CRUDWeek(CRUDWithName[Week]):
    async def get_all_numbers(self, session: AsyncSession) -> List[int]:
        query = select(self.model.number)
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_by_number(self, session: AsyncSession, number: int) -> Week:
        query = select(self.model).where(self.model.number == number)
        result = await session.execute(query)
        return result.scalars().first()

    async def get_by_datetime(self, session: AsyncSession, target_datetime: datetime):
        query = select(self.model).where(
            self.model.start_date <= target_datetime.date(),
            self.model.end_date >= target_datetime.date()
        )
        result = await session.execute(query)
        return result.scalars().first()


class CRUDTeacher(CRUDWithName[Teacher]):
    pass


class CRUDClassroom(CRUDWithName[Classroom]):
    pass


crud_entry = CRUDEntry(Entry)
crud_subject = CRUDSubject(Subject)
crud_type = CRUDType(Type)
crud_group = CRUDGroup(Group)
crud_week = CRUDWeek(Week)
crud_teacher = CRUDTeacher(Teacher)
crud_classroom = CRUDClassroom(Classroom)
