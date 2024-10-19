from typing import List

from rapidfuzz.distance import Levenshtein
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from parser.database.crud.base import CRUDWithName
from parser.database.models import Group, Week, Teacher, Classroom
from parser.schemas import ClassroomCreate


class CRUDGroup(CRUDWithName[Group]):
    async def find_closest(self, session: AsyncSession, group_name: str) -> str:
        names = await self.get_all_names(session)
        return min(names, key=lambda value: Levenshtein.distance(group_name, value))


class CRUDWeek(CRUDWithName[Week]):
    async def get_all_numbers(self, session: AsyncSession) -> List[int]:
        query = select(self.model.number)
        result = await session.execute(query)
        return list(result.scalars().all())


class CRUDTeacher(CRUDWithName[Teacher]):
    pass


class CRUDClassroom(CRUDWithName[Classroom]):
    async def create(self, session: AsyncSession, data: ClassroomCreate) -> Classroom:
        existing_classroom = await self.get_by_name(session, data.name)
        if existing_classroom:
            raise ValueError(f"Кабинет '{data.name}' уже существует")
        return await super().create(session, data)


crud_group = CRUDGroup(Group)
crud_week = CRUDWeek(Week)
crud_teacher = CRUDTeacher(Teacher)
crud_classroom = CRUDClassroom(Classroom)
