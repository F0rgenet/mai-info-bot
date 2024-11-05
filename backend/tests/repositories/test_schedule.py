from database.repositories.schedule import SubjectRepository, AbbreviationRepository


class TestSubjectRepository:
    async def test_create_subject(self, database_session):
        subject_name = "Тестовый предмет"
        repository = SubjectRepository(database_session)

        created_subject = await repository.create(subject_name)

        assert created_subject is not None
        assert created_subject.name == subject_name

    async def test_create_subject_with_abbreviation(self, database_session):
        subject_name = "Программирование на языках высокого уровня"
        abbreviation = "ПНЯВУ"
        subjects_repository = SubjectRepository(database_session)
        abbreviations_repository = AbbreviationRepository(database_session)

        abbreviation_id = (await abbreviations_repository.create(subject_name, abbreviation)).id
        created_subject = await subjects_repository.create(subject_name, abbreviation_id)

        # TODO: Исправить lazy loading в отношениях между моделями

        assert created_subject is not None
        assert created_subject.name == subject_name
        assert created_subject.abbreviation.name == abbreviation
        assert created_subject.abbreviation.id == abbreviation_id
