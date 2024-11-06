from typing import Generic, Optional, List, TypeVar
from uuid import UUID

from loguru import logger
from sqlalchemy import select, ColumnExpressionArgument
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.base import Base

Model = TypeVar("Model", bound=Base)


class BaseRepository(Generic[Model]):
    def __init__(self, session: AsyncSession, model: type[Model]):
        self._session = session
        self._model = model

    async def create(self, **data: dict) -> Model:
        """
        Создает новый экземпляр модели.

        :param data: Параметры для создания экземпляра.
        :returns: Новый экземпляр модели.
        """
        instance = self._model(**data)
        self._session.add(instance)
        await self._session.commit()
        await self._session.refresh(instance)
        return instance

    async def get_by_id(self, uuid: UUID) -> Optional[Model]:
        """
        Возвращает экземпляр модели по UUID.

        :param uuid: UUID экземпляра.
        :returns: Экземпляр модели или None.
        """
        query = select(self._model).where(self._model.id == uuid)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Model]:
        """
        Возвращает список всех экземпляров модели.

        :returns: Список экземпляров модели.
        """
        query = select(self._model)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def update(self, uuid: UUID, **data: dict) -> Optional[Model]:
        """
        Обновляет экземпляр модели по UUID.

        Аргументы, переданные со значением `Ellipsis`, будут проигнорированы, и соответствующие
        поля останутся неизменными в базе данных.

        :param uuid: UUID экземпляра.
        :param data: Данные для обновления, где ключи - имена полей модели, а значения - новые значения.
                     Если значение равно `Ellipsis`, поле в базе данных останется без изменений.
        :returns: Обновленный экземпляр модели или None.
        """
        data = {key: parameter for key, parameter in data.items() if parameter is not Ellipsis}
        instance = await self.get_by_id(uuid)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            await self._session.commit()
            await self._session.refresh(instance)
        else:
            logger.warning(f"Объект {self._model.__name__} для обновления не найден")
        return instance

    async def delete(self, uuid: UUID) -> bool:
        """
        Удаляет экземпляр модели по UUID.

        :param uuid: UUID экземпляра.
        :returns: True, если удаление успешно, иначе False.
        """
        instance = await self.get_by_id(uuid)
        if instance:
            await self._session.delete(instance)
            await self._session.commit()
            return True
        return False


class NamedBaseRepository(Generic[Model], BaseRepository[Model]):
    def __init__(self, session: AsyncSession, model: type[Model]):
        super().__init__(session, model)
        self._session = session
        self._model = model

    async def get_by_name(self, name: str) -> Optional[Model]:
        query = select(self._model).where(self._model.name == name)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()
