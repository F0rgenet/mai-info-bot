from typing import Optional, List, Dict, Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Teacher
from database.repositories.base import BaseRepository


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

    async def create_all(self, parameters: List[Dict[str, Any]]) -> List[Teacher]:
        """
        Создаёт несколько преподавателей по заданным параметрам.

        :param parameters: Список словарей с параметрами для каждого создаваемого объекта
        Каждый словарь должен содержать следующие ключи:
            - **full_name** (*str*): Полное имя преподавателя.
        """
        return await super().create_all(parameters)

    async def update(self, uuid: UUID, full_name: Optional[str] = ...) -> Teacher:
        """
        Обновляет преподавателя по ID.

        :param uuid: ID преподавателя для обновления.
        :param full_name: (Необязательно) Новое полное имя преподавателя. Не может быть None.
        :raises ValueError: Если full_name=None
        :returns: Обновлённый объект Teacher.
        """
        return await super().update(uuid, full_name=full_name)

    async def get_by_filters(self, full_name: Optional[str] = None) -> Optional[Teacher]:
        """
        Возвращает преподавателя по фильтрам.

        :param full_name: Полное имя преподавателя.
        :returns: Экземпляр Teacher.
        """
        return await super().get_by_filters(full_name=full_name)

    async def get_or_create(self, full_name: str) -> Teacher:
        """
        Возвращает экземпляр преподавателя по полному имени, если он существует, иначе создаёт новый.

        :param full_name: Полное имя преподавателя.
        :returns: Экземпляр Teacher.
        """
        return await super().get_or_create(full_name=full_name)

    async def get_or_create_all(self, parameters: List[Dict[str, Any]]) -> List[Teacher]:
        """
        Возвращает список экземпляров преподавателя по заданным параметрам, если они существуют, иначе создаёт новые.

        :param parameters: Список словарей с параметрами для каждого создаваемого объекта
        Каждый словарь должен содержать следующие ключи:
            - **full_name** (*str*): Полное имя преподавателя.
        :returns: Список экземпляров Teacher.
        """
        return await super().get_or_create_all(parameters)
