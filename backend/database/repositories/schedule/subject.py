from typing import Optional, List, Dict, Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Subject
from database.repositories.base import NamedBaseRepository


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

    async def create_all(self, parameters: List[Dict[str, Any]]) -> List[Subject]:
        """
        Создаёт несколько предметов по заданным параметрам.

        :param parameters: Список словарей с параметрами для каждого создаваемого объекта
        Каждый словарь должен содержать следующие ключи:
            - **name** (*str*): Название предмета.
            - **short_name** (*str*): Сокращённое название предмета.
        """
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

    async def get_by_filters(self, name: Optional[str] = ..., short_name: Optional[str] = ...) -> Optional[Subject]:
        """
        Возвращает экземпляр предмета по фильтрам.

        :param name: (Необязательно) Название предмета.
        :param short_name: (Необязательно) Сокращённое название предмета.
        :returns: Экземпляр Subject.
        """
        return await super().get_by_filters(name=name, short_name=short_name)

    async def get_or_create(self, name: str, short_name: Optional[str] = None) -> Subject:
        """
        Возвращает экземпляр предмета по названию, если он существует, иначе создаёт новый.

        :param name: Название предмета.
        :param short_name: (Необязательно) Сокращённое название предмета.
        :returns: Экземпляр Subject.
        """
        return await super().get_or_create(name=name, short_name=short_name)

    async def get_or_create_all(self, parameters: List[Dict[str, Any]]) -> List[Subject]:
        """
        Возвращает список экземпляров предметов по заданным параметрам, если они существуют, иначе создаёт новые.

        :param parameters: Список словарей с параметрами для каждого создаваемого объекта
        Каждый словарь должен содержать следующие ключи:
            - **name** (*str*): Название предмета.
            - **short_name** (*str*): Сокращённое название предмета.
        :returns: Список экземпляров Subject.
        """
        return await super().get_or_create_all(parameters)