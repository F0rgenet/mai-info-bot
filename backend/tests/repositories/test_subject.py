from typing import List

import pytest

from database.repositories import SubjectRepository

from sqlalchemy import exc

from repository_fixtures import subjects_data


@pytest.fixture
async def repository(database_session) -> SubjectRepository:
    return SubjectRepository(database_session)


class TestSubjectRepository:
    async def test_create_subject(self, database_session, repository: SubjectRepository, subjects_data: List[dict]):
        subject_data = subjects_data[0]
        created_subject = await repository.create(**subject_data)

        assert created_subject is not None
        assert created_subject.name == subject_data["name"]
        assert created_subject.short_name == subject_data["short_name"]

    async def test_create_all_subjects(self, database_session, repository: SubjectRepository, subjects_data: List[dict]):
        created_subjects = await repository.create_all(subjects_data)

        assert len(created_subjects) == len(subjects_data)

    async def test_create_subject_duplicate(self, database_session, repository: SubjectRepository, subjects_data: List[dict]):
        await repository.create(**subjects_data[0])
        with pytest.raises(exc.IntegrityError):
            await repository.create(**subjects_data[0])

    async def test_get_subject_by_id(self, database_session, repository: SubjectRepository, subjects_data: List[dict]):
        subject_data = subjects_data[0]

        created_subject = await repository.create(**subject_data)
        received_subject = await repository.get_by_id(created_subject.id)

        assert received_subject is created_subject
        assert received_subject.name == subject_data["name"]
        assert received_subject.short_name == subject_data["short_name"]

    async def test_get_subject_by_name(self, database_session, repository: SubjectRepository, subjects_data: List[dict]):
        name = "Программирование на языках высокого уровня"

        await repository.create_all(subjects_data)
        received_subject = await repository.get_by_name(name)

        assert received_subject is not None
        assert received_subject.name == name

    async def test_get_all_subjects(self, database_session, repository: SubjectRepository, subjects_data: List[dict]):
        await repository.create_all(subjects_data)
        received_subjects = await repository.get_all()

        assert len(received_subjects) == len(subjects_data)

    async def test_update_subject_data(self, database_session, repository: SubjectRepository, subjects_data: List[dict]):
        new_name = "Программирование на языках низкого уровня"
        new_short_name = "ПНЯНУ"

        created_subject = await repository.create(**subjects_data[0])
        updated_subject = await repository.update(uuid=created_subject.id, name=new_name, short_name=new_short_name)

        assert updated_subject is not None
        assert updated_subject.name == new_name
        assert updated_subject.short_name == new_short_name

    async def test_delete_subject(self, database_session, repository: SubjectRepository, subjects_data: List[dict]):
        created_subject = await repository.create(**subjects_data[0])
        await repository.delete(created_subject.id)
        received_subject = await repository.get_by_id(created_subject.id)

        assert received_subject is None
