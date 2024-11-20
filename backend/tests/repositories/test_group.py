from typing import List

import pytest

from database.models import Group
from database.repositories import GroupRepository

from sqlalchemy import exc

from repository_fixtures import groups_data


@pytest.fixture
def repository(database_session) -> GroupRepository:
    return GroupRepository(database_session)


class TestGroupRepository:
    async def test_create_group(self, database_session, repository: GroupRepository, groups_data: List[dict]):
        group_data = groups_data[0]
        created_group = await repository.create(**groups_data[0])

        assert created_group is not None
        assert created_group.name == group_data["name"]
        assert created_group.department == group_data["department"]
        assert created_group.level == group_data["level"]
        assert created_group.course == group_data["course"]

    async def test_create_all_groups(self, database_session, repository: GroupRepository, groups_data: List[dict]):
        created_groups = await repository.create_all(groups_data)

        assert len(created_groups) == len(groups_data)
        # TODO: Добавить проверку полей созданных объектов

    async def test_create_group_duplicate(self, database_session, repository: GroupRepository, groups_data: List[dict]):
        await repository.create(**groups_data[0])

        with pytest.raises(exc.IntegrityError):
            await repository.create(**groups_data[0])

    async def test_get_group_by_id(self, database_session, repository: GroupRepository, groups_data: List[dict]):
        group_data = groups_data[0]

        created_group = await repository.create(**group_data)
        received_group = await repository.get_by_id(created_group.id)

        assert received_group is not None
        assert received_group is created_group
        assert received_group.name == group_data["name"]
        assert received_group.department == group_data["department"]
        assert received_group.level == group_data["level"]
        assert received_group.course == group_data["course"]

    async def test_get_groups_by_department(self, database_session, repository: GroupRepository,
                                            groups_data: List[dict]):
        department = "Институт №14"
        expected_groups = [group for group in groups_data if group["department"] == department]

        await repository.create_all(groups_data)

        received_groups = await repository.get_by_department(department)
        assert len(received_groups) == len(expected_groups)
        for group in received_groups:
            assert group.department == department

    async def test_get_groups_by_course(self, database_session, repository: GroupRepository, groups_data: List[dict]):
        course = 1
        expected_groups = [group for group in groups_data if group["course"] == course]

        await repository.create_all(groups_data)

        received_groups = await repository.get_by_course(course)
        assert len(received_groups) == len(expected_groups)
        for group in received_groups:
            assert group.course == course

    async def test_update_group_data(self, database_session, repository: GroupRepository, groups_data: List[dict]):
        new_group_name = "Группа Б-420"
        new_group_department = "Институт №15"
        new_group_level = "Бакалавриат"
        new_group_course = 4

        created_group = await repository.create(**groups_data[0])
        updated_group = await repository.update(uuid=created_group.id, name=new_group_name,
                                                department=new_group_department,
                                                level=new_group_level, course=new_group_course)

        assert updated_group is not None
        assert updated_group.name == new_group_name
        assert updated_group.department == new_group_department
        assert updated_group.level == new_group_level
        assert updated_group.course == new_group_course

    async def test_delete_group(self, database_session, repository: GroupRepository, groups_data: List[dict]):
        created_group = await repository.create(**groups_data[0])
        await repository.delete(created_group.id)
        received_group = await repository.get_by_id(created_group.id)
        assert received_group is None
