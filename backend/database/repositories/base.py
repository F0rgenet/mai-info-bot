from typing import Generic, Optional, List, TypeVar, Dict, Any, AsyncGenerator
from uuid import UUID

from loguru import logger
from sqlalchemy import select, ColumnExpressionArgument, inspect, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.base import Base

Model = TypeVar("Model", bound=Base)


class BaseRepository(Generic[Model]):
    def __init__(self, session: AsyncSession, model: type[Model]):
        self._session = session
        self._model = model

    async def create(self, **data) -> Model:
        """
        Создает новый экземпляр модели.

        :param data: Параметры для создания экземпляра.
        :returns: Новый экземпляр модели.
        """
        instance = self._model(**data)
        async with self._session.begin_nested() as nested:
            self._session.add(instance)
            await nested.commit()

        await self._session.refresh(instance)
        return instance

    async def create_all(self, parameters: List[Dict[str, Any]]) -> List[Model]:
        """
        Создаёт несколько экземпляров модели по заданным параметрам.

        :param parameters: Список словарей с параметрами для каждого создаваемого объекта
        :returns: Список созданных экземпляров модели.
        """
        instances = [self._model(**params) for params in parameters]
        async with self._session.begin_nested() as nested:
            self._session.add_all(instances)
            await nested.commit()
        for instance in instances:
            await self._session.refresh(instance)
        return instances

    async def get_by_id(self, uuid: UUID) -> Optional[Model]:
        """
        Возвращает экземпляр модели по UUID.

        :param uuid: UUID экземпляра.
        :returns: Экземпляр модели или None.
        """
        query = select(self._model).where(self._model.id == uuid)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_filters(self, **filters) -> Optional[Model]:
        """
        Возвращает экземпляр модели по фильтрам.

        :param filters: Фильтры для поиска.
        :returns: Экземпляр модели или None.
        """
        query_filter = and_(*[self._model.c[key] == value for key, value in filters.items()])
        query = select(self._model).where(query_filter)
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

    async def get_or_create(self, **data) -> Model:
        """
        Возвращает экземпляр модели по заданным параметрам, если он существует, иначе создаёт новый.

        :param data: Параметры для создания экземпляра.
        :returns: Экземпляр модели.
        """
        for key, value in data.items():
            # noinspection PyTypeChecker
            query = select(self._model).where(self._model.__dict__[key] == value)
            result = await self._session.execute(query)
            objects = result.scalars().all()
            if objects:
                if len(objects) > 1:
                    raise ValueError(f"Найдено несколько экземпляров модели с такими параметрами: {data}")
                return objects[0]
        return await self.create(**data)

    async def get_or_create_all(self, parameters: List[Dict[str, Any]]) -> List[Model]:
        """
        Возвращает список экземпляров модели по заданным параметрам, если он существует, иначе создаёт новый.

        :param parameters: Список словарей с параметрами для каждого создаваемого объекта
        Каждый словарь должен содержать следующие ключи:
            - **name** (*str*): Название предмета.
            - **short_name** (*str*): Сокращённое название предмета.
        :returns: Список экземпляров модели.
        """
        results = []
        for parameter in parameters:
            database_object = await self.get_or_create(**parameter)
            results.append(database_object)
        return results

    async def update(self, uuid: UUID, **data) -> Optional[Model]:
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
        """
        Repository for models with a name field.
        :param session: Database session.
        :param model: Model class.
        :raises TypeError: If model does not have a name field.
        """
        super().__init__(session, model)
        self._session = session
        self._model = model
        mapper = inspect(model)
        if not mapper.has_property("name"):
            raise TypeError("Модель должна иметь поле 'name'")

    async def get_by_name(self, name: str) -> Optional[Model]:
        """
        Get a model by its name.
        :param name: Name of the model.
        :returns: Model with the given name or None if not found.
        """
        query = select(self._model).where(self._model.name == name)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()
