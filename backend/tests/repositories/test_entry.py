from typing import List

import pytest
from datetime import datetime
from sqlalchemy import exc

from database.models import Entry
from database.repositories import (
    EntryRepository,
    SubjectRepository,
    TypeRepository,
    ClassroomRepository,
    TeacherRepository,
    GroupRepository
)

from repository_fixtures import entries_data


@pytest.fixture
async def repository(database_session) -> EntryRepository:
    return EntryRepository(database_session)


def check_entry(entry: Entry, entry_data: dict):
    assert entry is not None
    assert entry.start_datetime == entry_data["start_datetime"]
    assert entry.end_datetime == entry_data["end_datetime"]
    assert entry.subject.name == entry_data["subject_name"]
    assert entry.type.short_name == entry_data["type_short_name"]
    assert entry.classroom.name == entry_data["classroom"]
    assert entry.teacher.full_name == entry_data["teacher_full_name"]
    assert entry.group.name == entry_data["group_name"]


class TestEntryRepository:
    async def test_create_entry(self, database_session, repository: EntryRepository, entries_data: List[dict]):
        entry_data = entries_data[0]

        subject = await SubjectRepository(database_session).create(entry_data["subject_name"])
        entry_type = await TypeRepository(database_session).create(entry_data["type_short_name"])
        classroom = await ClassroomRepository(database_session).create(entry_data["classroom"])
        teacher = await TeacherRepository(database_session).create(entry_data["teacher_full_name"])
        group = await GroupRepository(database_session).create(entry_data["group_name"])

        created_entry = await repository.create(
            entry_data["start_datetime"], entry_data["end_datetime"], subject.id, entry_type.id, group.id, classroom.id,
            teacher.id
        )
        received_entry = await repository.get_by_id(created_entry.id)

        check_entry(received_entry, entry_data)

    async def test_create_entry_with_relations(self, database_session, repository: EntryRepository,
                                               entries_data: List[dict]):
        entry_data = entries_data[0]
        created_entry = await repository.create_with_relations(**entry_data)
        received_entry = await repository.get_by_id(created_entry.id)

        check_entry(received_entry, entry_data)

    async def test_create_all_entries(self, database_session, repository: EntryRepository, entries_data: List[dict]):
        relation_parameters = await repository.parse_relations(entries_data)
        relations = await repository.create_all_relations(**relation_parameters)

        entries_data_with_ids = [
            {
                "start_datetime": entry_data["start_datetime"],
                "end_datetime": entry_data["end_datetime"],
                "subject_id": subject_id,
                "type_id": entry_type_id,
                "classroom_id": classroom_id,
                "teacher_id": teacher_id,
                "group_id": group_id
            }
            for entry_data, subject_id, entry_type_id, classroom_id, teacher_id, group_id in zip(
                entries_data, relations["subject_ids"], relations["type_ids"], relations["classroom_ids"],
                relations["teacher_ids"], relations["group_ids"]
            )
        ]

        entries = await repository.create_all(entries_data_with_ids)
        assert len(entries) == len(entries_data)

    async def test_create_all_entries_with_relations(self, database_session, repository: EntryRepository,
                                                     entries_data: List[dict]):
        entries = await repository.create_all_with_relations(entries_data)

        assert len(entries) == len(entries_data)
        for entry in entries:
            assert entry is not None

    async def test_create_entry_duplicate(self, database_session, repository: EntryRepository, entries_data: List[dict]):
        await repository.create_with_relations(**entries_data[0])

        with pytest.raises(ValueError):
            await repository.create_with_relations(**entries_data[0])

    async def test_parse_relations(self, repository: EntryRepository, entries_data: List[dict]):
        custom_entries_data = [
            {
                "subject_name": "Программирование на языках высокого уровня",
                "type_short_name": "ПЗ",
                "classroom": "3-435",
                "teacher_full_name": "Ширяева Виктория Валерьевна",
                "group_name": "М14О-105БВ-24",
            },
            {
                "subject_name": "Дифференциальные уравнения",
                "type_short_name": "Дифуры",
                "classroom": "3-435",
                "teacher_full_name": "Ширяева Виктория Валерьевна",
                "group_name": "М14О-105БВ-24",
            }
        ]
        relation_parameters = await repository.parse_relations(custom_entries_data)

        assert relation_parameters["subject_names"] == ["Программирование на языках высокого уровня",
                                                         "Дифференциальные уравнения"]
        assert relation_parameters["type_short_names"] == ["ПЗ", "Дифуры"]
        assert relation_parameters["classroom_names"] == ["3-435", "3-435"]
        assert relation_parameters["teacher_full_names"] == ["Ширяева Виктория Валерьевна",
                                                             "Ширяева Виктория Валерьевна"]
        assert relation_parameters["group_names"] == ["М14О-105БВ-24", "М14О-105БВ-24"]

    async def test_get_entry_by_id(self, database_session, repository: EntryRepository, entries_data: List[dict]):
        entry_data = entries_data[0]

        # TODO: Refactor повторения кода, вынести сравнение объектов в отдельный метод

        created_entry = await repository.create_with_relations(**entry_data)
        received_entry = await repository.get_by_id(created_entry.id)

        check_entry(received_entry, entry_data)

    async def test_get_entries_by_group_id(self, database_session, repository: EntryRepository, entries_data: List[dict]):
        entry_data = entries_data[0]

        created_entry = await repository.create_with_relations(**entry_data)
        received_entries = await repository.get_by_group_id(created_entry.group_id)

        assert len(received_entries) == 1
        assert received_entries[0] is created_entry
