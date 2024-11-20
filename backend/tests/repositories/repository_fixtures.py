import pytest
from datetime import datetime


@pytest.fixture
def classrooms_data():
    return [{"name": "ГУК Б-419"}, {"name": "ГУК Б-420"}, {"name": "ГУК Б-430"}]


@pytest.fixture
def groups_data():
    return [
        {
            "name": "М14О-105БВ-24",
            "department": "Институт №14",
            "level": "Базовое высшее образование",
            "course": 1
        },
        {
            "name": "М14О-101БВ-24",
            "department": "Институт №14",
            "level": "Базовое высшее образование",
            "course": 1
        },
        {
            "name": "М14О-103БВ-24",
            "department": "Институт №15",
            "level": "Базовое высшее образование",
            "course": 2
        },
        {
            "name": "М14О-104БВ-24",
            "department": "Институт №16",
            "level": "Базовое высшее образование",
            "course": 2
        },
        {
            "name": "М14О-102БВ-24",
            "department": "Институт №17",
            "level": "Базовое высшее образование",
            "course": 3
        },
    ]


@pytest.fixture
def subjects_data():
    return [{"name": "Программирование на языках высокого уровня", "short_name": "ПНОП"},
            {"name": "Дифференциальные уравнения", "short_name": "Дифуры"},
            {"name": "Английский язык"}]


@pytest.fixture
def teachers_data():
    return [{"full_name": "Иванов Иван Иванович"}, {"full_name": "Петров Пётр Петрович"}]


@pytest.fixture
def types_data():
    return [{"short_name": "ПЗ", "full_name": "Практическое занятие"},
            {"short_name": "ЛК", "full_name": "Лекция"},
            {"short_name": "ЛР", "full_name": "Лабораторная работа"},
            {"short_name": "ЭК", "full_name": "Экзамен"}]


@pytest.fixture
def entries_data():
    current_year = datetime.now().year
    return [
        {
            "start_datetime": datetime(current_year, 11, 11, 10, 45),
            "end_datetime": datetime(current_year, 11, 11, 12, 15),
            "subject_name": "Основы психологии",
            "type_short_name": "ЛК",
            "group_name": "М14О-105БВ-24",
            "classroom": "3-435",
            "teacher_full_name": "Ширяева Виктория Валерьевна",
        },
        {
            "start_datetime": datetime(current_year, 11, 11, 13, 0),
            "end_datetime": datetime(current_year, 11, 11, 14, 30),
            "subject_name": "Основы психологии",
            "type_short_name": "ПЗ",
            "group_name": "М14О-105БВ-24",
            "classroom": "3-445",
            "teacher_full_name": "Ширяева Виктория Валерьевна",
        },
        {
            "start_datetime": datetime(current_year, 11, 11, 14, 45),
            "end_datetime": datetime(current_year, 11, 11, 16, 15),
            "subject_name": "Базы данных",
            "type_short_name": "ПЗ",
            "group_name": "М14О-105БВ-24",
            "classroom": "3-420",
            "teacher_full_name": "Склеймин Юрий Борисович",
        },
        {
            "start_datetime": datetime(current_year, 11, 11, 16, 30),
            "end_datetime": datetime(current_year, 11, 11, 18, 0),
            "subject_name": "Дифференциальные уравнения",
            "type_short_name": "ЛК",
            "group_name": "М14О-105БВ-24",
            "classroom": "ГУК В-221",
        },
        {
            "start_datetime": datetime(current_year, 11, 12, 9, 0),
            "end_datetime": datetime(current_year, 11, 12, 10, 30),
            "subject_name": "Базы данных",
            "type_short_name": "ЛК",
            "group_name": "М14О-105БВ-24",
        },
        {
            "start_datetime": datetime(current_year, 11, 12, 10, 45),
            "end_datetime": datetime(current_year, 11, 12, 12, 15),
            "subject_name": "Общая физика",
            "type_short_name": "ЛК",
            "group_name": "М14О-105БВ-24",
            "classroom": "ГУК В-228",
            "teacher_full_name": "Ширяева Виктория Валерьевна",
        },
        {
            "start_datetime": datetime(current_year, 11, 12, 13, 0),
            "end_datetime": datetime(current_year, 11, 12, 14, 30),
            "subject_name": "Физическая культура",
            "type_short_name": "ПЗ",
            "group_name": "М14О-105БВ-24",
            "classroom": "3-129а",
            "teacher_full_name": "Кан Игорь Давидович",
        },
        {
            "start_datetime": datetime(current_year, 11, 12, 14, 45),
            "end_datetime": datetime(current_year, 11, 12, 16, 15),
            "subject_name": "Иностранный язык",
            "type_short_name": "ПЗ",
            "group_name": "М14О-105БВ-24",
        },
        {
            "start_datetime": datetime(current_year, 11, 12, 16, 30),
            "end_datetime": datetime(current_year, 11, 12, 18, 0),
            "subject_name": "Основы сетевых технологий",
            "type_short_name": "ПЗ",
            "group_name": "М14О-105БВ-24",
            "classroom": "3-317",
            "teacher_full_name": "Минасян Виталий Борисович",
        },
    ]
