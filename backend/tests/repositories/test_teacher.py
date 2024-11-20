from typing import List

import pytest

from database.repositories import TeacherRepository

from sqlalchemy import exc

from repository_fixtures import teachers_data

@pytest.fixture
async def repository(database_session) -> TeacherRepository:
    return TeacherRepository(database_session)


class TestTeacherRepository:
    async def test_create_teacher(self, database_session, repository: TeacherRepository, teachers_data: List[dict]):
        teacher_data = teachers_data[0]
        created_teacher = await repository.create(**teacher_data)

        assert created_teacher is not None
        assert created_teacher.full_name == teacher_data["full_name"]

    async def test_create_all_teachers(self, database_session, repository: TeacherRepository, teachers_data: List[dict]):
        created_teachers = await repository.create_all(teachers_data)

        assert len(created_teachers) == len(teachers_data)

    async def test_create_teacher_duplicate(self, database_session, repository: TeacherRepository, teachers_data: List[dict]):
        await repository.create(**teachers_data[0])
        with pytest.raises(exc.IntegrityError):
            await repository.create(**teachers_data[0])

    async def test_get_teacher_by_id(self, database_session, repository: TeacherRepository, teachers_data: List[dict]):
        teacher_data = teachers_data[0]

        created_teacher = await repository.create(**teacher_data)
        received_teacher = await repository.get_by_id(created_teacher.id)

        assert received_teacher is created_teacher
        assert received_teacher.full_name == teacher_data["full_name"]

    async def test_get_teacher_by_full_name(self, database_session, repository: TeacherRepository, teachers_data: List[dict]):
        full_name = "Иванов Иван Иванович"

        await repository.create_all(teachers_data)
        received_teacher = await repository.get_by_full_name(full_name)

        assert received_teacher is not None
        assert received_teacher.full_name == full_name

    async def test_get_all_teachers(self, database_session, repository: TeacherRepository, teachers_data: List[dict]):
        await repository.create_all(teachers_data)
        received_teachers = await repository.get_all()

        assert len(received_teachers) == len(teachers_data)

    async def test_update_teacher_data(self, database_session, repository: TeacherRepository, teachers_data: List[dict]):
        teacher_data = teachers_data[0]
        new_full_name = "Фёдоров Фёдор Фёдорович"

        created_teacher = await repository.create(**teacher_data)
        updated_teacher = await repository.update(uuid=created_teacher.id, full_name=new_full_name)

        assert updated_teacher is not None
        assert updated_teacher.full_name == new_full_name

    async def test_delete_teacher(self, database_session, repository: TeacherRepository, teachers_data: List[dict]):
        created_teacher = await repository.create(**teachers_data[0])
        await repository.delete(created_teacher.id)
        received_teacher = await repository.get_by_id(created_teacher.id)

        assert received_teacher is None
