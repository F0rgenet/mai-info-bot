import typing
from datetime import datetime, date
from typing import Optional, List, Type
from uuid import UUID

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Subject, Classroom, Teacher, Type, Group, Entry
from database.repositories.base import BaseRepository, NamedBaseRepository


class SubjectRepository(NamedBaseRepository[Subject]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Subject)

    async def create(self, name: str, short_name: Optional[str] = None) -> Subject:
        """
        Создает новый предмет с сокращением, если оно указано.

        :param name: Название предмета.
        :param short_name: (Необязательно) Сокращённое название предмета.
        :returns: Созданный объект Subject.
        """
        subject = Subject(name=name, short_name=short_name)

        self._session.add(subject)
        await self._session.commit()
        await self._session.refresh(subject)

        return subject

    async def update(self, uuid: UUID, name: Optional[str] = ..., short_name: Optional[str] = ...):
        """
        Обновляет предмет по ID.

        :param uuid: ID предмета для обновления.
        :param name: (Необязательно) Новое название предмета. Не может быть None.
        :param short_name: (Необязательно) Новое сокращённое название предмета.
        :raises ValueError: Если name=None
        """
        return await super().update(uuid, name=name, short_name=short_name)

    async def get_by_short_name(self, short_name: str) -> List[Subject]:
        """
        Получает предметы по сокращению.

        :param short_name: Сокращение, по которому нужно найти предмет.
        :returns: Найденный объект Subject или None, если такой предмет не найден.
        """
        query = select(self._model).where(self._model.short_name == short_name)
        result = await self._session.execute(query)
        return list(result.scalars().all())


class ClassroomRepository(NamedBaseRepository[Classroom]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Classroom)

    async def create(self, name: str) -> Classroom:
        """
        Создает новый объект аудитории.

        :param name: Название аудитории.
        :returns: Экземпляр Classroom.
        """
        return await super().create(name=name)


class TeacherRepository(BaseRepository[Teacher]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Teacher)

    async def create(self, full_name: str) -> Teacher:
        """
        Создает нового преподавателя.

        :param full_name: Полное имя преподавателя.
        :returns: Экземпляр Teacher.
        """
        return await super().create(full_name=full_name)

    async def get_by_full_name(self, full_name: str) -> Optional[Teacher]:
        """
        Возвращает объект преподавателя по полному имени.

        :param full_name: Полное имя преподавателя.
        :returns: Экземпляр Teacher или None.
        """
        query = select(self._model).where(self._model.full_name == full_name)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()


class TypeRepository(BaseRepository[Type]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Type)

    async def create(self, short_name: str, full_name: Optional[str] = None) -> Type:
        """
        Создает новый тип занятия.

        :param short_name: Краткое название типа.
        :param full_name: (Необязательно) Полное название типа.
        :returns: Экземпляр Type.
        """
        return await super().create(short_name=short_name, full_name=full_name)

    async def get_by_short_name(self, short_name: str) -> Optional[Type]:
        """
        Возвращает тип по краткому названию.

        :param short_name: Краткое название.
        :returns: Экземпляр Type или None.
        """
        query = select(self._model).where(self._model.short_name == short_name)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()


class GroupRepository(NamedBaseRepository[Group]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Group)

    async def create(self, name: str, department: Optional[str] = None, level: Optional[str] = None,
                     course: Optional[int] = None) -> Group:
        """
        Создает новый объект группы.

        :param name: Название группы.
        :param department: (Необязательно) Название департамента.
        :param level: (Необязательно) Уровень образования.
        :param course: (Необязательно) Номер курса.
        :returns: Экземпляр Group.
        """
        return await super().create(name=name, department=department, level=level, course=course)

    async def get_by_department(self, department: str) -> List[Group]:
        """
        Возвращает группы по департаменту.

        :param department: Название департамента.
        :returns: Список экземпляров Group.
        """
        query = select(self._model).where(self._model.department == department)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_by_course(self, course: int) -> List[Group]:
        """
        Возвращает группы по номеру курса.

        :param course: Номер курса.
        :returns: Список экземпляров Group.
        """
        query = select(self._model).where(self._model.course == course)
        result = await self._session.execute(query)
        return list(result.scalars().all())


class EntryRepository(BaseRepository[Entry]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Entry)

    async def create(self, start_datetime: datetime, end_datetime: datetime, subject_id: int, type_id: int,
                     classroom_id: Optional[int] = None, teacher_id: Optional[int] = None,
                     group_id: int = None) -> Entry:
        """
        Создает новую запись.

        :param start_datetime: Время начала.
        :param end_datetime: Время окончания.
        :param subject_id: ID предмета.
        :param type_id: ID типа занятия.
        :param classroom_id: (Необязательно) ID аудитории.
        :param teacher_id: (Необязательно) ID преподавателя.
        :param group_id: ID группы.
        :returns: Экземпляр Entry.
        """
        return await super().create(
            start_datetime=start_datetime, end_datetime=end_datetime, subject_id=subject_id, type_id=type_id,
            classroom_id=classroom_id, teacher_id=teacher_id, group_id=group_id
        )

    async def get_by_subject_id(self, subject_id: int) -> List[Entry]:
        """
        Возвращает список записей по ID предмета.

        :param subject_id: ID предмета.
        :returns: Список экземпляров Entry.
        """
        query = select(self._model).where(self._model.subject_id == subject_id)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_by_group_id(self, group_id: int) -> List[Entry]:
        """
        Возвращает список записей по ID группы.

        :param group_id: ID группы.
        :returns: Список экземпляров Entry.
        """
        query = select(self._model).where(self._model.group_id == group_id)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_by_teacher_id(self, teacher_id: int) -> List[Entry]:
        """
        Возвращает список записей по ID преподавателя.

        :param teacher_id: ID преподавателя.
        :returns: Список экземпляров Entry.
        """
        query = select(self._model).where(self._model.teacher_id == teacher_id)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_by_day(self, day: date) -> List[Entry]:
        """
        Возвращает записи по указанной дате.

        :param day: Дата.
        :returns: Список экземпляров Entry.
        """
        query = select(self._model).where(self._model.start_datetime.cast(date) == day)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_by_week(self, study_week_number: int) -> List[Entry]:
        """
        Возвращает записи по номеру учебной недели.

        :param study_week_number: Номер учебной недели.
        :returns: Список экземпляров Entry.
        """
        # TODO: Реализовать метод для получения записей по номеру учебной недели
        raise NotImplementedError()
