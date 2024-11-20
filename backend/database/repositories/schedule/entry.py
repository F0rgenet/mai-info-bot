from datetime import datetime, date
from typing import Optional, List, Dict, Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Entry
from database.repositories.base import BaseRepository

from . import SubjectRepository, TypeRepository, ClassroomRepository, TeacherRepository, GroupRepository


class EntryRepository(BaseRepository[Entry]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Entry)

    async def create(self, start_datetime: datetime, end_datetime: datetime, subject_id: int, type_id: int,
                     group_id: int, classroom_id: Optional[int] = None, teacher_id: Optional[int] = None) -> Entry:
        """
        Создаёт новую запись.

        :param start_datetime: Время начала.
        :param end_datetime: Время окончания.
        :param subject_id: ID предмета.
        :param type_id: ID типа занятия.
        :param group_id: ID группы.
        :param classroom_id: (Необязательно) ID аудитории.
        :param teacher_id: (Необязательно) ID преподавателя.
        :returns: Экземпляр Entry.
        """
        unique_selector_query = (select(Entry).where(self._model.start_datetime == start_datetime)
                                 .where(self._model.group_id == group_id))
        unique_selector_result = await self._session.execute(unique_selector_query)
        if unique_selector_result.scalars().all():
            group = await GroupRepository(self._session).get_by_id(group_id)
            raise ValueError(f"Запись с параметрами (группа: {group.name}, дата: {start_datetime}) уже существует")

        return await super().create(
            start_datetime=start_datetime, end_datetime=end_datetime, subject_id=subject_id, type_id=type_id,
            classroom_id=classroom_id, teacher_id=teacher_id, group_id=group_id
        )

    async def create_all(self, parameters: List[Dict[str, Any]]) -> List[Entry]:
        """
        Создаёт несколько записей по заданным параметрам.
        Каждый словарь должен содержать следующие ключи:
            - **start_datetime** (*datetime*): Время начала.
            - **end_datetime** (*datetime*): Время окончания.
            - **subject_id** (*int*): ID предмета.
            - **type_id** (*int*): ID типа занятия.
            - **classroom_id** (*int*): ID аудитории.
            - **teacher_id** (*int*): ID преподавателя.
            - **group_id** (*int*): ID группы.

        :param parameters: Список словарей с параметрами для каждого создаваемого объекта
        :returns: Список созданных объектов Entry.
        """
        return await super().create_all(parameters)

    async def create_with_relations(self, start_datetime: datetime, end_datetime: datetime,
                                    subject_name: str, type_short_name: str, group_name: str,
                                    classroom: Optional[str] = None, teacher_full_name: Optional[str] = None) -> Entry:
        """
        Создаёт новую запись с указанными отношениями.

        :param start_datetime: Время начала.
        :param end_datetime: Время окончания.
        :param subject_name: Название предмета.
        :param type_short_name: Краткое название типа.
        :param classroom: Название аудитории.
        :param teacher_full_name: Полное имя преподавателя.
        :param group_name: Название группы.
        :returns: Экземпляр Entry.
        """
        subject = await SubjectRepository(self._session).get_by_name(subject_name)
        if not subject:
            subject = await SubjectRepository(self._session).create(subject_name)

        entry_type = await TypeRepository(self._session).get_by_short_name(type_short_name)
        if not entry_type:
            entry_type = await TypeRepository(self._session).create(type_short_name)

        if classroom:
            database_classroom = await ClassroomRepository(self._session).get_by_name(classroom)
            if not database_classroom:
                database_classroom = await ClassroomRepository(self._session).create(classroom)
            database_classroom_id = database_classroom.id
        else:
            database_classroom_id = None

        if teacher_full_name:
            database_teacher = await TeacherRepository(self._session).get_by_full_name(teacher_full_name)
            if not database_teacher:
                database_teacher = await TeacherRepository(self._session).create(teacher_full_name)
            database_teacher_id = database_teacher.id
        else:
            database_teacher_id = None

        group = await GroupRepository(self._session).get_by_name(group_name)
        if not group:
            group = await GroupRepository(self._session).create(group_name)

        await self._session.flush()

        return await self.create(start_datetime, end_datetime, subject.id,
                                 entry_type.id, group.id, database_classroom_id, database_teacher_id)

    async def create_all_relations(self, subject_names: List[str], type_short_names: List[str],
                                   classroom_names: List[str], teacher_full_names: List[str],
                                   group_names: List[str]) -> Dict[str, List[UUID]]:
        """
        Создаёт несколько записей с указанными отношениями по заданным параметрам.

        Словарь результата содержит следующие ключи:
            - **subjects** (*List[UUID]*): Список ID предметов.
            - **types** (*List[UUID]*): Список ID типов занятий.
            - **classrooms** (*List[UUID]*): Список ID аудиторий.
            - **teachers** (*List[UUID]*): Список ID преподавателей.
            - **groups** (*List[UUID]*): Список ID групп.

        :param subject_names: Список названий предметов.
        :param type_short_names: Список кратких названий типов занятий.
        :param classroom_names: Список названий аудиторий.
        :param teacher_full_names: Список полных названий преподавателей.
        :param group_names: Список названий групп.

        :returns: Словарь с ключом имени отношения и списком ID объектов в базе данных в том же порядке,
        что и были переданы.
        """
        subjects = await SubjectRepository(self._session).get_or_create_all(
            [{"name": subject_name} for subject_name in subject_names]
        )
        subject_ids = [subject.id for subject in subjects if subject]

        types = await TypeRepository(self._session).get_or_create_all(
            [{"short_name": type_short_name} for type_short_name in type_short_names]
        )
        type_ids = [entry_type.id for entry_type in types if type]

        classroom_ids = []
        for classroom_name in classroom_names:
            if classroom_name:
                classroom = await ClassroomRepository(self._session).get_or_create(name=classroom_name)
                classroom_ids.append(classroom.id if classroom else None)
            else:
                classroom_ids.append(None)

        teacher_ids = []
        for teacher_full_name in teacher_full_names:
            if teacher_full_name:
                teacher = await TeacherRepository(self._session).get_or_create(full_name=teacher_full_name)
                teacher_ids.append(teacher.id if teacher else None)
            else:
                teacher_ids.append(None)

        groups = await GroupRepository(self._session).get_or_create_all(
            [{"name": group_name} for group_name in group_names]
        )
        group_ids = [group.id for group in groups if group]

        return {
            "subject_ids": subject_ids,
            "type_ids": type_ids,
            "classroom_ids": classroom_ids,
            "teacher_ids": teacher_ids,
            "group_ids": group_ids
        }

    @staticmethod
    async def parse_relations(parameters: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
        """
        Парсит список параметров.

        :param parameters: Список словарей с параметрами для каждого создаваемого объекта
        Каждый словарь должен содержать следующие ключи:
            - **subject_name** (*str*): Название предмета.
            - **type_short_name** (*str*): Краткое название типа занятия.
            - **classroom** (*str*): Название аудитории.
            - **teacher_full_name** (*str*): Полное имя преподавателя.
            - **group_name** (*str*): Название группы.

        :returns: Словарь с ключом имени отношения и списком параметров.
        """
        subject_names = [entry_data["subject_name"] for entry_data in parameters]
        type_short_names = [entry_data["type_short_name"] for entry_data in parameters]
        group_names = [entry_data["group_name"] for entry_data in parameters]
        classroom_names = [entry_data.get("classroom") for entry_data in parameters]
        teacher_full_names = [entry_data.get("teacher_full_name") for entry_data in parameters]
        return {
            "subject_names": subject_names,
            "type_short_names": type_short_names,
            "classroom_names": classroom_names,
            "teacher_full_names": teacher_full_names,
            "group_names": group_names
        }

    async def create_all_with_relations(self, parameters: List[Dict[str, Any]]) -> List[Entry]:
        """
        Создаёт несколько записей с указанными отношениями по заданным параметрам.

        :param parameters: Список словарей с параметрами для каждого создаваемого объекта
        Каждый словарь должен содержать следующие ключи:
            - **subject_name** (*str*): Название предмета.
            - **type_short_name** (*str*): Краткое название типа занятия.
            - **classroom** (*str*): Название аудитории.
            - **teacher_full_name** (*str*): Полное имя преподавателя.
            - **group_name** (*str*): Название группы.

        :returns: Список созданных объектов Entry.
        """
        relation_parameters = await self.parse_relations(parameters)
        relations = await self.create_all_relations(**relation_parameters)

        all_start_datetimes = [entry_data["start_datetime"] for entry_data in parameters]
        all_end_datetimes = [entry_data["end_datetime"] for entry_data in parameters]

        entry_parameters = [
            {"start_datetime": start_datetime, "end_datetime": end_datetime, "subject_id": subject_id,
             "type_id": type_id,
             "classroom_id": classroom_id, "teacher_id": teacher_id, "group_id": group_id}
            for start_datetime, end_datetime, subject_id, type_id, classroom_id, teacher_id, group_id in zip(
                all_start_datetimes, all_end_datetimes, relations["subject_ids"], relations["type_ids"],
                relations["classroom_ids"], relations["teacher_ids"], relations["group_ids"]
            )
        ]

        return await self.create_all(entry_parameters)

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

    # TODO: Добавить фильтры по которым можно получить записи

    async def get_or_create(self, start_datetime: datetime, end_datetime: datetime, subject_id: int, type_id: int,
                            classroom_id: Optional[int] = None, teacher_id: Optional[int] = None,
                            group_id: int = None) -> Entry:
        """
        Возвращает экземпляр записи по начальной дате, если она существует, иначе создаёт новую.

        :param start_datetime: Время начала.
        :param end_datetime: Время окончания.
        :param subject_id: ID предмета.
        :param type_id: ID типа занятия.
        :param classroom_id: (Необязательно) ID аудитории.
        :param teacher_id: (Необязательно) ID преподавателя.
        :param group_id: ID группы.
        :returns: Экземпляр Entry.
        """
        return await super().get_or_create(
            start_datetime=start_datetime, end_datetime=end_datetime, subject_id=subject_id, type_id=type_id,
            classroom_id=classroom_id, teacher_id=teacher_id, group_id=group_id
        )

    async def get_or_create_all(self, parameters: List[Dict[str, Any]]) -> List[Entry]:
        """
        Возвращает список экземпляров записи по заданным параметрам, если они существуют, иначе создаёт новые.

        :param parameters: Список словарей с параметрами для каждого создаваемого объекта
        Каждый словарь должен содержать следующие ключи:
            - **start_datetime** (*datetime*): Время начала.
            - **end_datetime** (*datetime*): Время окончания.
            - **subject_id** (*int*): ID предмета.
            - **type_id** (*int*): ID типа занятия.
            - **classroom_id** (*int*): ID аудитории.
            - **teacher_id** (*int*): ID преподавателя.
            - **group_id** (*int*): ID группы.

        :returns: Список экземпляров Entry.
        """
        return await super().get_or_create_all(parameters)

    async def get_by_week(self, study_week_number: int) -> List[Entry]:
        """
        Возвращает записи по номеру учебной недели.

        :param study_week_number: Номер учебной недели.
        :returns: Список экземпляров Entry.
        """
        # TODO: Реализовать метод для получения записей по номеру учебной недели
        raise NotImplementedError()
