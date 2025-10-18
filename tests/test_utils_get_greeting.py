import pytest
from datetime import datetime, time
from src.utils import get_greeting


def test_get_greeting_morning():
    # Проверяем утреннее время
    test_time = datetime(2025, 10, 18, 5, 0)  # 05:00
    assert get_greeting(test_time) == "Доброе утро"

    test_time = datetime(2025, 10, 18, 11, 59)  # 11:59
    assert get_greeting(test_time) == "Доброе утро"


def test_get_greeting_day():
    # Проверяем дневное время
    test_time = datetime(2025, 10, 18, 12, 0)  # 12:00
    assert get_greeting(test_time) == "Добрый день"

    test_time = datetime(2025, 10, 18, 17, 59)  # 17:59
    assert get_greeting(test_time) == "Добрый день"


def test_get_greeting_evening():
    # Проверяем вечернее время
    test_time = datetime(2025, 10, 18, 18, 0)  # 18:00
    assert get_greeting(test_time) == "Добрый вечер"

    test_time = datetime(2025, 10, 18, 22, 59)  # 22:59
    assert get_greeting(test_time) == "Добрый вечер"


def test_get_greeting_night():
    # Проверяем ночное время
    test_time = datetime(2025, 10, 18, 23, 0)  # 23:00
    assert get_greeting(test_time) == "Доброй ночи"

    test_time = datetime(2025, 10, 18, 4, 59)  # 04:59
    assert get_greeting(test_time) == "Доброй ночи"


def test_get_greeting_invalid_type():
    # Проверяем обработку неверного типа данных
    assert get_greeting("неверное значение") == "Ошибка: передан неверный тип данных. Ожидается объект datetime"
    assert get_greeting(12345) == "Ошибка: передан неверный тип данных. Ожидается объект datetime"
    assert get_greeting([1, 2, 3]) == "Ошибка: передан неверный тип данных. Ожидается объект datetime"


def test_get_greeting_edge_cases():
    # Проверяем граничные случаи
    test_time = datetime(2025, 10, 18, 4, 59)  # 04:59 - ночь
    assert get_greeting(test_time) == "Доброй ночи"

    test_time = datetime(2025, 10, 18, 5, 0)  # 05:00 - утро
    assert get_greeting(test_time) == "Доброе утро"

    test_time = datetime(2025, 10, 18, 11, 59)  # 11:59 - утро
    assert get_greeting(test_time) == "Доброе утро"

    test_time = datetime(2025, 10, 18, 12, 0)  # 12:00 - день
    assert get_greeting(test_time) == "Добрый день"

    test_time = datetime(2025, 10, 18, 17, 59)  # 17:59 - день
    assert get_greeting(test_time) == "Добрый день"

    test_time = datetime(2025, 10, 18, 18, 0)  # 18:00 - вечер
    assert get_greeting(test_time) == "Добрый вечер"