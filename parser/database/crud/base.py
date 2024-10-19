from typing import List, Union, Any, TypeVar, Generic

from loguru import logger
from sqlalchemy import update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

T = TypeVar('T')


class CRUDBase(Generic[T]):
    def __init__(self, model: T):
        self.model = model

    async def create(self, session: AsyncSession, data: Any) -> Union[T, None]:
        """
        Создает объект в базе данных.

        :param session: Асинхронная сессия SQLAlchemy
        :param data: Данные для создания объекта (обычно схемы Pydantic)
        :return: Созданный объект или None в случае ошибки
        """
        try:
            db_object = self.model(**data.model_dump())
            session.add(db_object)
            await session.commit()
            await session.refresh(db_object)
            logger.success(f"Объект {self.model.__name__} успешно создан: {data.dict()}")
            return db_object
        except Exception as e:
            logger.error(f"Ошибка при создании объекта {self.model.__name__}: {e}")
            await session.rollback()
            return None

    async def safe_create(self, session: AsyncSession, data: Any) -> T:
        try:
            return await self.create(session, data)
        except IntegrityError:
            await session.rollback()
            # TODO: Возвращать объект найденный по совпадению параметров
            # return await self.get(session, data.id)

    async def get(self, session: AsyncSession, object_id: int) -> Union[T, None]:
        """
        Получает объект по его ID.

        :param session: Асинхронная сессия SQLAlchemy
        :param object_id: ID объекта для поиска
        :return: Найденный объект или None, если не найден
        """
        try:
            logger.info(f"Поиск объекта {self.model.__name__} с ID: {object_id}")
            query = select(self.model).filter(self.model.id == object_id)
            result = await session.execute(query)
            db_object = result.scalar_one_or_none()
            if db_object:
                logger.success(f"Объект найден: {db_object}")
            else:
                logger.warning(f"Объект с ID {object_id} не найден")
            return db_object
        except Exception as e:
            logger.error(f"Ошибка при получении объекта с ID {object_id}: {e}")
            return None

    async def get_all(self, session: AsyncSession, skip: int = 0, limit: int = -1) -> List[T]:
        """
        Получает все объекты модели с учетом пагинации.

        :param session: Асинхронная сессия SQLAlchemy
        :param skip: Количество объектов для пропуска (для пагинации)
        :param limit: Количество объектов для получения (для пагинации)
        :return: Список объектов
        """
        try:
            logger.info(f"Получение объектов {self.model.__name__} с пропуском {skip} и лимитом {limit}")
            query = select(self.model).offset(skip).limit(limit)
            result = await session.execute(query)
            objects = result.scalars().all()
            logger.success(f"Найдено объектов: {len(objects)}")
            return objects
        except Exception as e:
            logger.error(f"Ошибка при получении объектов: {e}")
            return []

    async def update(self, session: AsyncSession, object_id: int, updated_data: Any) -> Union[T, None]:
        """
        Обновляет объект по его ID.

        :param session: Асинхронная сессия SQLAlchemy
        :param object_id: ID объекта для обновления
        :param updated_data: Обновленные данные для объекта
        :return: Обновленный объект или None в случае ошибки
        """
        try:
            query = update(self.model).where(self.model.id == object_id).values(**updated_data.dict(exclude_unset=True))
            result = await session.execute(query)
            await session.commit()

            if result.rowcount > 0:
                logger.success(f"Объект с ID {object_id} успешно обновлен")
                return await self.get(session, object_id)
            else:
                logger.warning(f"Объект с ID {object_id} не был обновлен (может не существовать)")
                return None
        except Exception as e:
            logger.error(f"Ошибка при обновлении объекта с ID {object_id}: {e}")
            await session.rollback()
            return None

    async def delete(self, session: AsyncSession, object_id: int) -> bool:
        """
        Удаляет объект по его ID.

        :param session: Асинхронная сессия SQLAlchemy
        :param object_id: ID объекта для удаления
        :return: True, если удаление прошло успешно, иначе False
        """
        try:
            query = delete(self.model).where(self.model.id == object_id)
            result = await session.execute(query)
            await session.commit()

            if result.rowcount > 0:
                logger.success(f"Объект с ID {object_id} успешно удален")
                return True
            else:
                logger.warning(f"Объект с ID {object_id} не найден для удаления")
                return False
        except Exception as exception:
            logger.error(f"Ошибка при удалении объекта с ID {object_id}: {exception}")
            await session.rollback()
            return False


NameType = TypeVar('NameType')


class CRUDWithName(CRUDBase[NameType], Generic[NameType]):
    async def get_all_names(self, session: AsyncSession) -> List[str]:
        query = select(self.model.name)
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_by_name(self, session: AsyncSession, name: str) -> Union[NameType, None]:
        query = select(self.model).filter(self.model.name == name)
        result = await session.execute(query)
        return result.scalar_one_or_none()
