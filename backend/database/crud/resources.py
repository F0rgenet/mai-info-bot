from typing import List

from rapidfuzz.distance import Levenshtein
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.crud.base import CRUDWithName
from backend.database.models import Group, Week, Teacher, Classroom


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
    pass


crud_group = CRUDGroup(Group)
crud_week = CRUDWeek(Week)
crud_teacher = CRUDTeacher(Teacher)
crud_classroom = CRUDClassroom(Classroom)
