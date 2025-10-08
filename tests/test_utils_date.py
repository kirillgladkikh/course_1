from datetime import datetime
from src.utils import parse_datetime, calculate_period, get_greeting


# Тесты для функции parse_datetime
def test_parse_datetime_valid():
    date_str = "2025-10-08 15:41:00"
    expected = datetime(2025, 10, 8, 15, 41, 0)
    assert parse_datetime(date_str) == expected, "Ошибка при парсинге корректной даты"


def test_parse_datetime_invalid_format():
    try:
        parse_datetime("08-10-2025 15:41:00")  # Неверный формат даты
        assert False, "Должен быть вызван ValueError для неверного формата"
    except ValueError:
        pass


def test_parse_datetime_invalid_date():
    try:
        parse_datetime("2025-02-30 15:41:00")  # 30 февраля
        assert False, "Должен быть вызван ValueError для несуществующей даты"
    except ValueError:
        pass


def test_parse_datetime_edge_cases():
    assert parse_datetime("2025-10-01 00:00:00") == datetime(2025, 10, 1, 0, 0, 0), "Ошибка на минимальной дате"
    assert parse_datetime("2025-10-31 23:59:59") == datetime(2025, 10, 31, 23, 59, 59), "Ошибка на максимальной дате"


# Тесты для функции calculate_period
def test_calculate_period_first_day():
    date = datetime(2025, 10, 1, 12, 0, 0)
    assert calculate_period(date) == 0, "Ошибка для первого дня месяца"


def test_calculate_period_middle_month():
    date = datetime(2025, 10, 15, 12, 0, 0)
    assert calculate_period(date) == 14, "Ошибка для середины месяца"


def test_calculate_period_last_day():
    date = datetime(2025, 10, 31, 12, 0, 0)
    assert calculate_period(date) == 30, "Ошибка для последнего дня месяца"


def test_calculate_period_leap_year():
    date = datetime(2024, 2, 29, 12, 0, 0)
    assert calculate_period(date) == 28, "Ошибка для високосного года"


# Тесты для функции get_greeting
def test_get_greeting_morning():
    date = datetime(2025, 10, 8, 8, 0, 0)
    assert get_greeting(date) == "Доброе утро", "Ошибка для утреннего приветствия"


def test_get_greeting_day():
    date = datetime(2025, 10, 8, 14, 0, 0)
    assert get_greeting(date) == "Добрый день", "Ошибка для дневного приветствия"


def test_get_greeting_evening():
    date = datetime(2025, 10, 8, 19, 0, 0)
    assert get_greeting(date) == "Добрый вечер", "Ошибка для вечернего приветствия"


def test_get_greeting_night():
    date = datetime(2025, 10, 8, 2, 0, 0)
    assert get_greeting(date) == "Доброй ночи", "Ошибка для ночного приветствия"


def test_get_greeting_edge_hours():
    # Проверка граничных значений для утреннего приветствия
    assert (
        get_greeting(datetime(2025, 10, 8, 5, 0, 0)) == "Доброе утро"
    ), "Ошибка на границе утреннего приветствия (5:00)"
    assert (
        get_greeting(datetime(2025, 10, 8, 11, 59, 59)) == "Доброе утро"
    ), "Ошибка на границе утреннего приветствия (11:59:59)"

    # Проверка граничных значений для дневного приветствия
    assert (
        get_greeting(datetime(2025, 10, 8, 12, 0, 0)) == "Добрый день"
    ), "Ошибка на границе дневного приветствия (12:00)"
    assert (
        get_greeting(datetime(2025, 10, 8, 17, 59, 59)) == "Добрый день"
    ), "Ошибка на границе дневного приветствия (17:59:59)"

    # Проверка граничных значений для вечернего приветствия
    assert (
        get_greeting(datetime(2025, 10, 8, 18, 0, 0)) == "Добрый вечер"
    ), "Ошибка на границе вечернего приветствия (18:00)"
    assert (
        get_greeting(datetime(2025, 10, 8, 22, 59, 59)) == "Добрый вечер"
    ), "Ошибка на границе вечернего приветствия (22:59:59)"

    # Проверка граничных значений для ночного приветствия
    assert (
        get_greeting(datetime(2025, 10, 8, 0, 0, 0)) == "Доброй ночи"
    ), "Ошибка на границе ночного приветствия (00:00)"
    assert (
        get_greeting(datetime(2025, 10, 8, 4, 59, 59)) == "Доброй ночи"
    ), "Ошибка на границе ночного приветствия (04:59:59)"
    assert (
        get_greeting(datetime(2025, 10, 8, 23, 0, 0)) == "Доброй ночи"
    ), "Ошибка на границе ночного приветствия (23:00)"
