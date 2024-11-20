from typing import Optional, List, Type, Dict, Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Type
from database.repositories.base import BaseRepository


class TypeRepository(BaseRepository[Type]):
    def __init__(self, session: AsyncSession):
        self._session = session
        super().__init__(session, Type)

    async def create(self, short_name: str, full_name: Optional[str] = None) -> Type:
        """
        Создаёт новый тип занятия.

        :param short_name: Краткое название типа.
        :param full_name: (Необязательно) Полное название типа.
        :returns: Экземпляр Type.
        """
        return await super().create(short_name=short_name, full_name=full_name)

    async def create_all(self, parameters: List[Dict[str, Any]]) -> List[Type]:
        """
        Создаёт несколько типов занятий по заданным параметрам.

        :param parameters: Список словарей с параметрами для каждого создаваемого объекта
        Каждый словарь должен содержать следующие ключи:
            - **short_name** (*str*): Краткое название типа.
            - **full_name** (*str*): Полное название типа.
        """
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

    async def get_by_filters(self, short_name: Optional[str] = ..., full_name: Optional[str] = ...) -> Optional[Type]:
        """
        Возвращает тип по фильтрам.

        :param short_name: Краткое название.
        :param full_name: Полное название.
        :returns: Экземпляр Type или None.
        """
        if not any([short_name, full_name]):
            raise ValueError("Необходимо указать хотя бы один из параметров фильтрации")
        return await super().get_by_filters(short_name=short_name, full_name=full_name)

    async def get_or_create(self, short_name: str, full_name: Optional[str] = None) -> Type:
        """
        Возвращает экземпляр типа по краткому названию, если он существует, иначе создаёт новый.

        :param short_name: Краткое название.
        :param full_name: (Необязательно) Полное название.
        :returns: Экземпляр Type.
        """
        return await super().get_or_create(short_name=short_name, full_name=full_name)

    async def get_or_create_all(self, parameters: List[Dict[str, Any]]) -> List[Type]:
        """
        Возвращает список экземпляров типа по заданным параметрам, если они существуют, иначе создаёт новые.

        :param parameters: Список словарей с параметрами для каждого создаваемого объекта
        Каждый словарь должен содержать следующие ключи:
            - **short_name** (*str*): Краткое название типа.
            - **full_name** (*str*): Полное название типа.
        :returns: Список экземпляров Type.
        """
        return await super().get_or_create_all(parameters)
