from typing import Generic, Optional, List, TypeVar
from uuid import UUID

from sqlalchemy import select, ColumnExpressionArgument
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.base import Base

Model = TypeVar("Model", bound=Base)


class BaseRepository(Generic[Model]):
    def __init__(self, session: AsyncSession, model: type[Model]):
        self._session = session
        self._model = model

    async def create(self, **data: dict) -> Model:
        instance = self._model(**data)
        self._session.add(instance)
        await self._session.commit()
        await self._session.refresh(instance)
        return instance

    async def create_or_update_base(self, *selectors: ColumnExpressionArgument[bool], **data) -> Model:
        query = select(self._model).where(selectors)
        instance = await self._session.execute(query)
        if instance:
            await self.update(instance, **data)
            return instance
        await self.create(**data)

    async def get_by_id(self, uuid: UUID) -> Optional[Model]:
        query = select(self._model).where(self._model.id == uuid)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Model]:
        query = select(self._model)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def update(self, uuid: UUID, **data: dict) -> Optional[Model]:
        instance = await self.get_by_id(uuid)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
        await self._session.commit()
        await self._session.refresh(instance)
        return instance

    async def delete(self, uuid: UUID) -> bool:
        instance = await self.get_by_id(uuid)
        if instance:
            await self._session.delete(instance)
            await self._session.refresh(instance)
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
