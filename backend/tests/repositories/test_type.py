from typing import List

import pytest

from database.models import Type
from database.repositories import TypeRepository

from sqlalchemy import exc


@pytest.fixture
def types_data():
    return [{"short_name": "ПЗ", "full_name": "Практическое занятие"},
            {"short_name": "ЛК", "full_name": "Лекция"},
            {"short_name": "ЛР", "full_name": "Лабораторная работа"},
            {"short_name": "ЭК", "full_name": "Экзамен"}]


@pytest.fixture
async def repository(database_session) -> TypeRepository:
    return TypeRepository(database_session)


class TestTypeRepository:
    async def test_create_type(self, database_session, repository: TypeRepository, types_data: List[dict]):
        type_data = types_data[0]
        created_type = await repository.create(**type_data)

        assert created_type is not None
        assert created_type.short_name == type_data["short_name"]
        assert created_type.full_name == type_data["full_name"]

    async def test_create_type_without_full_name(self, database_session, repository: TypeRepository, types_data: List[dict]):
        type_data = types_data[0]
        type_data.pop("full_name")
        created_type = await repository.create(**type_data, full_name=None)

        assert created_type is not None
        assert created_type.short_name == type_data["short_name"]
        assert created_type.full_name is None

    async def test_create_all_types(self, database_session, repository: TypeRepository, types_data: List[dict]):
        created_types = await repository.create_all(types_data)

        assert len(created_types) == len(types_data)

    async def test_create_type_duplicate(self, database_session, repository: TypeRepository, types_data: List[dict]):
        await repository.create(**types_data[0])

        with pytest.raises(exc.IntegrityError):
            await repository.create(**types_data[0])

    async def test_get_type_by_id(self, database_session, repository: TypeRepository, types_data: List[dict]):
        type_data = types_data[0]

        created_type = await repository.create(**type_data)
        received_type = await repository.get_by_id(created_type.id)

        assert received_type is created_type
        assert received_type.short_name == type_data["short_name"]
        assert received_type.full_name == type_data["full_name"]

    async def test_get_type_by_short_name(self, database_session, repository: TypeRepository, types_data: List[dict]):
        short_name = "ПЗ"

        await repository.create_all(types_data)
        received_type = await repository.get_by_short_name(short_name)

        assert received_type is not None
        assert received_type.short_name == short_name

    async def test_get_type_by_full_name(self, database_session, repository: TypeRepository, types_data: List[dict]):
        full_name = "Практическое занятие"

        await repository.create_all(types_data)
        received_type = await repository.get_by_full_name(full_name)

        assert received_type is not None
        assert received_type.full_name == full_name

    async def test_get_all_types(self, database_session, repository: TypeRepository, types_data: List[dict]):
        await repository.create_all(types_data)
        received_types = await repository.get_all()

        assert len(received_types) == len(types_data)

    async def test_update_type_data(self, database_session, repository: TypeRepository, types_data: List[dict]):
        new_short_name = "ЛМК"
        new_full_name = "Лекция по математике"

        created_type = await repository.create(**types_data[0])
        await repository.update(uuid=created_type.id, short_name=new_short_name, full_name=new_full_name)
        received_type = await repository.get_by_id(created_type.id)

        assert received_type is not None
        assert received_type.short_name == new_short_name
        assert received_type.full_name == new_full_name

    async def test_delete_type(self, database_session, repository: TypeRepository, types_data: List[dict]):
        created_type = await repository.create(**types_data[0])
        await repository.delete(created_type.id)
        received_type = await repository.get_by_id(created_type.id)

        assert received_type is None
