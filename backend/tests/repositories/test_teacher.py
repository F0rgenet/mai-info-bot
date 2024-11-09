import pytest

from database.repositories import TeacherRepository


from sqlalchemy import exc


class TestSubjectRepository:
    async def test_create_teacher(self, database_session):
        repository = TeacherRepository(database_session)
        teacher_full_name = "Иванов Иван Иванович"

        created_teacher = await repository.create(teacher_full_name)

        assert created_teacher is not None
        assert created_teacher.full_name == teacher_full_name

    async def test_create_teacher_duplicate(self, database_session):
        repository = TeacherRepository(database_session)
        teacher_full_name = "Иванов Иван Иванович"

        await repository.create(teacher_full_name)

        with pytest.raises(exc.IntegrityError):
            await repository.create(teacher_full_name)

    async def test_get_teacher_by_id(self, database_session):
        repository = TeacherRepository(database_session)
        teacher_full_name = "Иванов Иван Иванович"

        created_teacher = await repository.create(teacher_full_name)

        received_teacher = await repository.get_by_id(created_teacher.id)

        assert received_teacher is created_teacher
        assert received_teacher.full_name == created_teacher.full_name

    async def test_get_teacher_by_full_name(self, database_session):
        repository = TeacherRepository(database_session)
        teacher_full_name = "Иванов Иван Иванович"

        created_teacher = await repository.create(teacher_full_name)

        received_teacher = await repository.get_by_full_name(teacher_full_name)

        assert received_teacher is created_teacher
        assert received_teacher.full_name == created_teacher.full_name

    async def test_get_all_teachers(self, database_session):
        repository = TeacherRepository(database_session)
        teacher_full_names = ["Иванов Иван Иванович", "Петров Пётр Петрович"]

        created_teacher = await repository.create_all(teacher_full_names)

