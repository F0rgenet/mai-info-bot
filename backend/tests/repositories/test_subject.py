import pytest

from database.repositories import SubjectRepository

from sqlalchemy import exc


class TestSubjectRepository:
    async def test_create_subject(self, database_session):
        repository = SubjectRepository(database_session)
        subject_name = "Тестовый предмет"

        created_subject = await repository.create(subject_name)

        assert created_subject is not None
        assert created_subject.name == subject_name

    async def test_create_subject_duplicate(self, database_session):
        repository = SubjectRepository(database_session)
        subject_name = "Тестовый предмет"

        await repository.create(subject_name)
        with pytest.raises(exc.IntegrityError):
            await repository.create(subject_name)

    async def test_create_subject_with_short_name(self, database_session):
        subjects_repository = SubjectRepository(database_session)
        subject_name = "Программирование на языках высокого уровня"
        short_name = "ПНЯВУ"
        
        created_subject = await subjects_repository.create(subject_name, short_name)

        assert created_subject is not None
        assert created_subject.name == subject_name
        assert created_subject.short_name == short_name

    # TODO: test_create_all
    # TODO: test_create_all_with_short_names

    async def test_get_subject_by_id(self, database_session):
        subjects_repository = SubjectRepository(database_session)
        subject_name = "Программирование на языках высокого уровня"
        short_name = "ПНЯВУ"

        created_subject = await subjects_repository.create(subject_name, short_name)

        received_subject = await subjects_repository.get_by_id(created_subject.id)
        assert received_subject is created_subject
        assert received_subject.short_name == short_name

    async def test_get_subject_by_name(self, database_session):
        subjects_repository = SubjectRepository(database_session)
        subject_name = "Программирование на языках высокого уровня"
        short_name = "ПНЯВУ"

        created_subject = await subjects_repository.create(subject_name, short_name)

        received_subject = await subjects_repository.get_by_name(subject_name)
        assert received_subject is created_subject
        assert received_subject.short_name == short_name

    async def test_get_subjects_by_short_name(self, database_session):
        subjects_repository = SubjectRepository(database_session)
        subject_names = ["Программирование на языках высокого уровня", "Программирование на языках верхнего уровня"]
        short_name = "ПНЯВУ"

        for name in subject_names:
            await subjects_repository.create(name, short_name)
        received_subjects = await subjects_repository.get_by_short_name(short_name)

        assert len(received_subjects) == len(subject_names)
        for subject in received_subjects:
            assert subject.short_name == short_name

    async def test_get_all_subjects(self, database_session):
        subjects_repository = SubjectRepository(database_session)
        subject_names = ["Программирование на языках высокого уровня", "Программирование на языках верхнего уровня"]

        for name in subject_names:
            await subjects_repository.create(name)
        received_subjects = await subjects_repository.get_all()

        assert len(received_subjects) == len(subject_names)

    async def test_update_subject_name(self, database_session):
        subjects_repository = SubjectRepository(database_session)
        subject_name = "Программирование на языках высокого уровня"
        short_name = "ПНЯВУ"
        new_subject_name = "Программирование"

        created_subject = await subjects_repository.create(subject_name, short_name)
        updated_subject = await subjects_repository.update(uuid=created_subject.id, name=new_subject_name)

        assert updated_subject is not None
        assert updated_subject is created_subject
        assert updated_subject.name == new_subject_name
        assert updated_subject.short_name == short_name

    async def test_delete_subject_short_name(self, database_session):
        subjects_repository = SubjectRepository(database_session)
        subject_name = "Программирование на языках высокого уровня"
        short_name = "ПНЯВУ"

        created_subject = await subjects_repository.create(subject_name, short_name)
        updated_subject = await subjects_repository.update(created_subject.id, short_name=None)

        assert updated_subject is not None
        assert updated_subject is created_subject
        assert updated_subject.name == subject_name
        assert updated_subject.short_name is None

    async def test_delete_subject(self, database_session):
        subjects_repository = SubjectRepository(database_session)
        subject_name = "Программирование на языках высокого уровня"

        created_subject = await subjects_repository.create(subject_name)
        await subjects_repository.delete(created_subject.id)
        received_subject = await subjects_repository.get_by_id(created_subject.id)

        assert received_subject is None
