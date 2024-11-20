from typing import Optional, List, Dict, Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Group
from database.repositories.base import NamedBaseRepository


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

    async def create_all(self, parameters: List[Dict[str, Any]]) -> List[Group]:
        """
        Создаёт несколько групп по заданным параметрам.

        :param parameters: Список словарей с параметрами для каждого создаваемого объекта
        Каждый словарь должен содержать следующие ключи:
            - **name** (*str*): Название группы.
            - **department** (*str*): Название кафедры.
            - **level** (*str*): Уровень образования.
            - **course** (*int*): Номер курса.
        """
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

    async def get_by_filters(self, name: Optional[str], department: Optional[str], level: Optional[str],
                             course: Optional[int]) -> Group:
        """
        Возвращает экземпляр группы по фильтрам.

        :param name: (Необязательно) Новое название группы.
        :param department: (Необязательно) Новое название департамента.
        :param level: (Необязательно) Новый уровень.
        :param course: (Необязательно) Новый номер курса.
        :raises ValueError: Если name=None
        :returns: Обновлённый объект Group.
        """
        return await super().get_by_filters(name=name, department=department, level=level, course=course)

    async def get_or_create(self, name: str, department: Optional[str] = None, level: Optional[str] = None,
                            course: Optional[int] = None) -> Group:
        """
        Возвращает экземпляр группы по названию, если он существует, иначе создаёт новый.

        :param name: Название группы.
        :param department: (Необязательно) Название кафедры.
        :param level: (Необязательно) Уровень образования.
        :param course: (Необязательно) Номер курса.
        :returns: Экземпляр Group.
        """
        return await super().get_or_create(name=name, department=department, level=level, course=course)

    async def get_or_create_all(self, parameters: List[Dict[str, Any]]) -> List[Group]:
        """
        Возвращает список экземпляров групп по заданным параметрам, если они существуют, иначе создаёт новые.

        :param parameters: Список словарей с параметрами для каждого создаваемого объекта
        Каждый словарь должен содержать следующие ключи:
            - **name** (*str*): Название группы.
            - **department** (*str*): Название кафедры.
            - **level** (*str*): Уровень образования.
            - **course** (*int*): Номер курса.
        :returns: Список экземпляров Group.
        """
        return await super().get_or_create_all(parameters)
