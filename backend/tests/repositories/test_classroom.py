from typing import List

import pytest
from sqlalchemy import exc

from database.repositories import ClassroomRepository

from repository_fixtures import classrooms_data


@pytest.fixture
async def repository(database_session) -> ClassroomRepository:
    return ClassroomRepository(database_session)


class TestClassroomRepository:
    async def test_create_classroom(self, database_session, repository: ClassroomRepository,
                                    classrooms_data: List[dict]):
        classroom_data = classrooms_data[0]
        created_classroom = await repository.create(**classroom_data)

        assert created_classroom is not None
        assert created_classroom.name == classroom_data["name"]

    async def test_create_all_classrooms(self, database_session, repository: ClassroomRepository,
                                         classrooms_data: List[dict]):
        created_classrooms = await repository.create_all(classrooms_data)

        assert len(created_classrooms) == len(classrooms_data)
        # TODO: Добавить проверку полей созданных объектов

    async def test_create_classroom_duplicate(self, database_session, repository: ClassroomRepository,
                                              classrooms_data: List[dict]):
        await repository.create(**classrooms_data[0])

        with pytest.raises(exc.IntegrityError):
            await repository.create(**classrooms_data[0])

    async def test_get_classroom_by_id(self, database_session, repository: ClassroomRepository,
                                       classrooms_data: List[dict]):
        classroom_data = classrooms_data[0]

        created_classroom = await repository.create(**classroom_data)
        received_classroom = await repository.get_by_id(created_classroom.id)

        assert received_classroom is created_classroom
        assert received_classroom.name == classroom_data["name"]

    async def test_get_classroom_by_name(self, database_session, repository: ClassroomRepository,
                                         classrooms_data: List[dict]):
        name = "ГУК Б-419"

        await repository.create_all(classrooms_data)
        received_classroom = await repository.get_by_name(name)

        assert received_classroom is not None
        assert received_classroom.name == name

    async def test_get_all_classrooms(self, database_session, repository: ClassroomRepository,
                                      classrooms_data: List[dict]):
        await repository.create_all(classrooms_data)
        received_classrooms = await repository.get_all()

        assert len(received_classrooms) == len(classrooms_data)

    async def test_get_or_create_classroom(self, database_session, repository: ClassroomRepository,
                                           classrooms_data: List[dict]):
        classroom_data = classrooms_data[0]
        created_classroom = await repository.get_or_create(**classroom_data)

        assert created_classroom is not None
        assert created_classroom.name == classroom_data["name"]

        received_classroom = await repository.get_or_create(**classroom_data)
        assert received_classroom is not None
        assert received_classroom is created_classroom
        assert received_classroom.name == classroom_data["name"]

    async def test_get_or_create_all_classrooms(self, database_session, repository: ClassroomRepository,
                                                classrooms_data: List[dict]):
        created_classrooms = await repository.get_or_create_all(classrooms_data)

        assert len(created_classrooms) == len(classrooms_data)

        received_classrooms = await repository.get_all()
        previously_created_classrooms = await repository.get_or_create_all(classrooms_data)

        assert len(received_classrooms) == len(previously_created_classrooms)

    async def test_update_classroom_name(self, database_session, repository: ClassroomRepository,
                                         classrooms_data: List[dict]):
        new_classroom_name = "ГУК Б-420"

        created_classroom = await repository.create(**classrooms_data[0])
        await repository.update(uuid=created_classroom.id, name=new_classroom_name)
        received_classroom = await repository.get_by_id(created_classroom.id)

        assert received_classroom is not None
        assert received_classroom.name == new_classroom_name

    async def test_delete_classroom(self, database_session, repository: ClassroomRepository,
                                    classrooms_data: List[dict]):
        created_classroom = await repository.create(**classrooms_data[0])
        await repository.delete(created_classroom.id)
        received_classroom = await repository.get_by_id(created_classroom.id)

        assert received_classroom is None
