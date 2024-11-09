import typing
from datetime import datetime, date
from typing import Optional, List, Type
from uuid import UUID

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Subject, Classroom, Teacher, Type, Group, Entry
from database.repositories.base import BaseRepository, NamedBaseRepository, Model


class SubjectRepository(NamedBaseRepository[Subject]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Subject)

    async def create(self, name: str, short_name: Optional[str] = None) -> Subject:
        """
        Создаёт новый предмет с сокращением, если оно указано.

        :param name: Название предмета.
        :param short_name: (Необязательно) Сокращённое название предмета.
        :returns: Созданный объект Subject.
        """
        return await super().create(name=name, short_name=short_name)

    async def create_all(self, names: List[str], short_names: Optional[List[str]] = None) -> List[Subject]:
        """
        Создаёт несколько предметов с сокращениями, если такие есть.

        :param names: Список названий предметов.
        :param short_names: Опциональный список сокращений для предметов, должен соответствовать длине names.
        :returns: Список созданных объектов Subject.
        :raises ValueError: Если длина short_names не соответствует длине names.
        """
        if short_names is not None and len(names) != len(short_names):
            raise ValueError("Длина списка сокращений должна соответствовать длине списка названий")

        parameters = [
            {"name": name, "short_name": short_name}
            for name, short_name in zip(names, short_names or [None] * len(names))
        ]
        return await super().create_all(parameters)

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
        Создаёт новый объект аудитории.

        :param name: Название аудитории.
        :returns: Экземпляр Classroom.
        """
        return await super().create(name=name)

    async def create_all(self, names: List[str]) -> List[Classroom]:
        """
        Создаёт несколько аудиторий.

        :param names: Список названий аудиторий.
        :returns: Список созданных объектов Classroom.
        """
        parameters = [{"name": name} for name in names]
        return await super().create_all(parameters)

    async def update(self, uuid: UUID, name: Optional[str] = ...):
        """
        Обновляет аудиторию по ID.

        :param uuid: ID аудитории для обновления.
        :param name: (Необязательно) Новое название аудитории. Не может быть None.
        :raises ValueError: Если name=None
        :returns: Обновлённый объект Classroom.
        """
        return await super().update(uuid, name=name)


class TeacherRepository(BaseRepository[Teacher]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Teacher)

    async def create(self, full_name: str) -> Teacher:
        """
        Создаёт нового преподавателя.

        :param full_name: Полное имя преподавателя.
        :returns: Экземпляр Teacher.
        """
        return await super().create(full_name=full_name)

    async def create_all(self, full_names: List[str]) -> List[Teacher]:
        """
        Создаёт несколько преподавателей.

        :param full_names: Список полных имён преподавателей.
        :returns: Список созданных объектов Teacher.
        """
        parameters = [{"full_name": name} for name in full_names]
        return await super().create_all(parameters)

    async def update(self, uuid: UUID, full_name: Optional[str] = ...):
        """
        Обновляет преподавателя по ID.

        :param uuid: ID преподавателя для обновления.
        :param full_name: (Необязательно) Новое полное имя преподавателя. Не может быть None.
        :raises ValueError: Если full_name=None
        :returns: Обновлённый объект Teacher.
        """
        return await super().update(uuid, full_name=full_name)

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
        Создаёт новый тип занятия.

        :param short_name: Краткое название типа.
        :param full_name: (Необязательно) Полное название типа.
        :returns: Экземпляр Type.
        """
        return await super().create(short_name=short_name, full_name=full_name)

    async def create_all(
            self,
            short_names: List[str],
            full_names: Optional[List[str]] = None
    ) -> List[Type]:
        """
        Создаёт несколько типов занятий.

        :param short_names: Список кратких названий типов.
        :param full_names: Опциональный список полных названий типов, должен соответствовать длине short_names.
        :returns: Список созданных объектов Type.
        :raises ValueError: Если длина full_names не соответствует длине short_names.
        """
        if full_names is not None and len(short_names) != len(full_names):
            raise ValueError("Длина списка полных названий должна соответствовать длине списка кратких названий")

        parameters = [
            {"short_name": short_name, "full_name": full_name}
            for short_name, full_name in zip(short_names, full_names or [None] * len(short_names))
        ]
        return await super().create_all(parameters)

    async def update(self, uuid: UUID, short_name: Optional[str] = ..., full_name: Optional[str] = ...):
        """
        Обновляет тип занятия по ID.

        :param uuid: ID типа для обновления.
        :param short_name: (Необязательно) Новое краткое название типа. Не может быть None.
        :param full_name: (Необязательно) Новое полное название типа.
        :raises ValueError: Если short_name=None
        :returns: Обновлённый объект Type.
        """
        return await super().update(uuid, short_name=short_name, full_name=full_name)

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
        Создаёт новый объект группы.

        :param name: Название группы.
        :param department: (Необязательно) Название кафедры.
        :param level: (Необязательно) Уровень образования.
        :param course: (Необязательно) Номер курса.
        :returns: Экземпляр Group.
        """
        return await super().create(name=name, department=department, level=level, course=course)

    async def create_all(
            self,
            names: List[str],
            departments: Optional[List[str]] = None,
            levels: Optional[List[str]] = None,
            courses: Optional[List[int]] = None
    ) -> List[Group]:
        """
        Создаёт несколько групп.

        :param names: Список названий групп.
        :param departments: Опциональный список кафедр, должен соответствовать длине names.
        :param levels: Опциональный список уровней образования, должен соответствовать длине names.
        :param courses: Опциональный список номеров курсов, должен соответствовать длине names.
        :returns: Список созданных объектов Group.
        :raises ValueError: Если длина любого из опциональных списков не соответствует длине names.
        """
        n = len(names)
        if (departments is not None and len(departments) != n) or \
                (levels is not None and len(levels) != n) or \
                (courses is not None and len(courses) != n):
            raise ValueError("Длина всех списков параметров должна соответствовать длине списка названий")

        parameters = [
            {
                "name": name,
                "department": dept,
                "level": level,
                "course": course
            }
            for name, dept, level, course in zip(
                names,
                departments or [None] * n,
                levels or [None] * n,
                courses or [None] * n
            )
        ]
        return await super().create_all(parameters)
    
    async def update(self, uuid: UUID, name: Optional[str] = ..., department: Optional[str] = ...,
                     level: Optional[str] = ..., course: Optional[int] = ...):
        """
        Обновляет группу по ID.

        :param uuid: ID группы для обновления.
        :param name: (Необязательно) Новое название группы. Не может быть None.
        :param department: (Необязательно) Новое название кафедры.
        :param level: (Необязательно) Новый уровень образования.
        :param course: (Необязательно) Новый номер курса.
        :raises ValueError: Если name=None
        :returns: Обновлённый объект Group.
        """
        return await super().update(uuid, name=name, department=department, level=level, course=course)

    async def get_by_department(self, department: str) -> List[Group]:
        """
        Возвращает группы по кафедре.

        :param department: Название кафедры.
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
        Создаёт новую запись.

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

    async def create_all(
            self,
            start_datetimes: List[datetime],
            end_datetimes: List[datetime],
            subject_ids: List[int],
            type_ids: List[int],
            classroom_ids: Optional[List[int]] = None,
            teacher_ids: Optional[List[int]] = None,
            group_ids: Optional[List[int]] = None
    ) -> List[Entry]:
        """
        Создаёт несколько записей расписания.

        :param start_datetimes: Список времён начала.
        :param end_datetimes: Список времён окончания.
        :param subject_ids: Список ID предметов.
        :param type_ids: Список ID типов занятий.
        :param classroom_ids: Опциональный список ID аудиторий.
        :param teacher_ids: Опциональный список ID преподавателей.
        :param group_ids: Опциональный список ID групп.
        :returns: Список созданных объектов Entry.
        :raises ValueError: Если длины списков не совпадают.
        """
        n = len(start_datetimes)
        if len(end_datetimes) != n or len(subject_ids) != n or len(type_ids) != n or \
                (classroom_ids is not None and len(classroom_ids) != n) or \
                (teacher_ids is not None and len(teacher_ids) != n) or \
                (group_ids is not None and len(group_ids) != n):
            raise ValueError("Длина всех списков параметров должна быть одинаковой")

        parameters = [
            {
                "start_datetime": start,
                "end_datetime": end,
                "subject_id": subject_id,
                "type_id": type_id,
                "classroom_id": classroom_id,
                "teacher_id": teacher_id,
                "group_id": group_id
            }
            for start, end, subject_id, type_id, classroom_id, teacher_id, group_id in zip(
                start_datetimes,
                end_datetimes,
                subject_ids,
                type_ids,
                classroom_ids or [None] * n,
                teacher_ids or [None] * n,
                group_ids or [None] * n
            )
        ]
        return await super().create_all(parameters)

    async def update(self, uuid: UUID, start_datetime: Optional[datetime] = ..., end_datetime: Optional[datetime] = ...,
                     subject_id: Optional[int] = ..., type_id: Optional[int] = ...,
                     classroom_id: Optional[int] = ..., teacher_id: Optional[int] = ..., group_id: Optional[int] = ...):
        """
        Обновляет запись по ID.

        :param uuid: ID записи для обновления.
        :param start_datetime: (Необязательно) Новое время начала.
        :param end_datetime: (Необязательно) Новое время окончания.
        :param subject_id: (Необязательно) Новый ID предмета.
        :param type_id: (Необязательно) Новый ID типа занятия.
        :param classroom_id: (Необязательно) Новый ID аудитории.
        :param teacher_id: (Необязательно) Новый ID преподавателя.
        :param group_id: (Необязательно) Новый ID группы.
        :returns: Обновлённый объект Entry.
        """
        return await super().update(
            uuid, start_datetime=start_datetime, end_datetime=end_datetime,
            subject_id=subject_id, type_id=type_id, classroom_id=classroom_id,
            teacher_id=teacher_id, group_id=group_id
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
