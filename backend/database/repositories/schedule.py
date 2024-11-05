from datetime import datetime
from typing import Optional, List, Type
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Abbreviation, Subject, Classroom, Teacher, Type, Group, Entry
from database.repositories.base import BaseRepository, NamedBaseRepository


class AbbreviationRepository(NamedBaseRepository[Abbreviation]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Abbreviation)

    async def get_by_short_name(self, short_name: str) -> Optional[Abbreviation]:
        query = select(self._model).where(self._model.short_name == short_name)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()


class SubjectRepository(NamedBaseRepository[Subject]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Subject)

    def create_or_update(self, name: str, abbreviation_id: Optional[int]) -> Subject:
        data = {"name": name, "abbreviation_id": abbreviation_id}
        selector = (self._model.name == name)
        instance = super()._create_or_update_base(data, selector)
        return instance


class ClassroomRepository(NamedBaseRepository[Classroom]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Classroom)


class TeacherRepository(BaseRepository[Teacher]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Teacher)

    async def get_by_full_name(self, full_name: str) -> Optional[Teacher]:
        query = select(self._model).where(self._model.full_name == full_name)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()


class TypeRepository(BaseRepository[Type]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Type)

    async def get_by_short_name(self, short_name: str) -> Optional[Type]:
        query = select(self._model).where(self._model.short_name == short_name)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()


class GroupRepository(NamedBaseRepository[Group]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Group)

    async def get_by_department(self, department: str) -> List[Group]:
        query = select(self._model).where(self._model.department == department)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_by_course(self, course: int) -> List[Group]:
        query = select(self._model).where(self._model.course == course)
        result = await self._session.execute(query)
        return list(result.scalars().all())


class EntryRepository(BaseRepository[Entry]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Entry)

    async def get_by_subject_id(self, subject_id: UUID) -> List[Entry]:
        query = select(self._model).where(self._model.subject_id == subject_id)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_by_group_id(self, group_id: UUID) -> List[Entry]:
        query = select(self._model).where(self._model.group_id == group_id)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_by_teacher_id(self, teacher_id: UUID) -> List[Entry]:
        query = select(self._model).where(self._model.teacher_id == teacher_id)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_by_day(self, day: datetime.date):
        pass

    async def get_by_week(self, study_week_number: int):
        # TODO: Postgres week метод для получения текущей недели
        pass
