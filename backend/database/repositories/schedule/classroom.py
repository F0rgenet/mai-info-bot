from typing import Optional, List, Dict, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Classroom
from database.repositories.base import NamedBaseRepository


class ClassroomRepository(NamedBaseRepository[Classroom]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Classroom)

    async def create(self, name: str) -> Classroom:
        """
        Создаёт новый объект аудитории.
        :returns: Экземпляр Classroom.
        """
        return await super().create(name=name)

    async def create_all(self, parameters: List[Dict[str, Any]]) -> List[Classroom]:
        """
        Создаёт несколько аудиторий по заданным параметрам.

        :param parameters: Список словарей с параметрами для каждого создаваемого объекта
        Каждый словарь должен содержать следующие ключи:
            - **name** (*str*): Название аудитории.
        """
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

    async def get_by_filters(self, name: Optional[str]) -> Classroom:
        """
        Возвращает экземпляр аудитории по фильтрам.

        :param name: (Необязательно) Новое название аудитории.
        :raises ValueError: Если name=None
        :returns: Обновлённый объект Classroom.
        """
        return await super().get_by_filters(name=name)

    async def get_or_create(self, name: str) -> Classroom:
        """
        Возвращает экземпляр аудитории по названию, если он существует, иначе создаёт новый.

        :param name: Название аудитории.
        :returns: Экземпляр Classroom.
        """
        return await super().get_or_create(name=name)
