from typing import List, Union, Any, TypeVar, Generic, Dict, Callable
from loguru import logger
from sqlalchemy import delete, inspect, UniqueConstraint, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.database.utils import handle_db_exceptions


T = TypeVar('T')


class CRUDBase(Generic[T]):
    def __init__(self, model: T):
        self.model = model
        self.change_handlers: List[Callable[[str, Dict[str, tuple]], None]] = []

    def add_change_handler(self, handler: Callable[[str, Dict[str, tuple]], None]):
        self.change_handlers.append(handler)

    def notify_changes(self, operation: str, changes: Dict[str, tuple]):
        for handler in self.change_handlers:
            handler(operation, changes)

    @staticmethod
    def objects_diff(obj1: Any, obj2: Any) -> Dict[str, tuple]:
        obj1_dict = {k: v for k, v in obj1.__dict__.items() if not k.startswith('_') and k != 'id'}
        obj2_dict = {k: v for k, v in obj2.__dict__.items() if not k.startswith('_') and k != 'id'}
        return {key: (obj1_dict.get(key), obj2_dict.get(key)) for key in set(obj1_dict) | set(obj2_dict) if
                obj1_dict.get(key) != obj2_dict.get(key)}

    @staticmethod
    def get_diff_string(diff: Dict[str, tuple]) -> str:
        def quotes(value):
            return f'"{value}"' if isinstance(value, str) else value

        diff_string = ', '.join([f'{key}: ({quotes(value[0])} -> {quotes(value[1])})' for key, value in diff.items()])
        return f"[{diff_string}]"

    def get_unique_fields(self) -> List[str]:
        mapper = inspect(self.model)
        unique_fields = [column.name for column in mapper.columns if column.unique]
        unique_fields.extend([column.name for constraint in mapper.tables[0].constraints
                              if isinstance(constraint, UniqueConstraint) for column in constraint.columns])
        return unique_fields

    async def get_object_by_unique_fields(self, session: AsyncSession, data: Any) -> Union[T, None]:
        unique_fields = self.get_unique_fields()
        filters = [getattr(self.model, field) == getattr(data, field) for field in unique_fields]
        query = select(self.model).filter(*filters)
        return (await session.execute(query)).scalar_one_or_none()

    @handle_db_exceptions
    async def create(self, session: AsyncSession, data: Any) -> Union[T, None]:
        object_data = data.model_dump()
        db_object = self.model(**object_data)
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        logger.success(f"{self.model.__name__} создан: id={db_object.id} {object_data}")
        self.notify_changes("create", {k: (None, v) for k, v in data.model_dump().items() if k != 'id'})
        return db_object

    @handle_db_exceptions
    async def create_or_update(self, session: AsyncSession, data: Any) -> Union[T, None]:
        existing_object = await self.get_object_by_unique_fields(session, data)
        if existing_object:
            return await self.update(session, existing_object.id, data)
        return await self.create(session, data)

    @handle_db_exceptions
    async def get(self, session: AsyncSession, object_id: int) -> Union[T, None]:
        query = select(self.model).filter(self.model.id == object_id)
        result = await session.execute(query)
        db_object = result.scalar_one_or_none()
        return db_object

    @handle_db_exceptions
    async def get_all(self, session: AsyncSession, skip: int = 0, limit: int = -1) -> List[T]:
        query = select(self.model).offset(skip).limit(limit)
        result = await session.execute(query)
        objects = result.scalars().all()
        logger.success(f"Получено {self.model.__name__}: количество={len(objects)}")
        return objects

    @handle_db_exceptions
    async def update(self, session: AsyncSession, object_id: int, updated_data: Any) -> Union[T, None]:
        existing_object = await self.get(session, object_id)
        if not existing_object:
            logger.warning(f"Ошибка обновления {self.model.__name__}: id={object_id} не найден")
            return None

        diff = self.objects_diff(existing_object, updated_data)
        if not diff:
            logger.info(f"{self.model.__name__} не изменён: id={object_id}")
            return existing_object

        update_data = updated_data.dict(exclude_unset=True)
        query = update(self.model).where(self.model.id == object_id).values(**update_data)
        await session.execute(query)
        await session.commit()

        logger.success(f"{self.model.__name__} обновлён: id={object_id}, изменения: {self.get_diff_string(diff)}")
        self.notify_changes("update", diff)

        return await self.get(session, object_id)

    @handle_db_exceptions
    async def delete(self, session: AsyncSession, object_id: int) -> bool:
        query = delete(self.model).where(self.model.id == object_id)
        result = await session.execute(query)
        await session.commit()

        if result.rowcount > 0:
            logger.info(f"{self.model.__name__} удален: id={object_id}")
            self.notify_changes("delete", {"id": (object_id, None)})
            return True
        else:
            logger.warning(f"Ошибка удаления {self.model.__name__}: id={object_id} не найден")
            return False


# Расширение для работы с объектами, у которых есть поле "name"
NameType = TypeVar('NameType')


class CRUDWithName(CRUDBase[NameType], Generic[NameType]):
    @handle_db_exceptions
    async def get_all_names(self, session: AsyncSession) -> List[str]:
        query = select(self.model.name)
        result = await session.execute(query)
        return list(result.scalars().all())

    @handle_db_exceptions
    async def get_by_name(self, session: AsyncSession, name: str) -> Union[NameType, None]:
        query = select(self.model).filter(self.model.name == name)
        result = await session.execute(query)
        return result.scalar_one_or_none()
