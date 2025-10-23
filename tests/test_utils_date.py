from datetime import datetime
from src.utils import get_greeting


# Тесты для функции get_greeting
def test_get_greeting_morning() -> None:
    date = datetime(2025, 10, 8, 8, 0, 0)
    assert get_greeting(date) == "Доброе утро", "Ошибка для утреннего приветствия"


def test_get_greeting_day() -> None:
    date = datetime(2025, 10, 8, 14, 0, 0)
    assert get_greeting(date) == "Добрый день", "Ошибка для дневного приветствия"


def test_get_greeting_evening() -> None:
    date = datetime(2025, 10, 8, 19, 0, 0)
    assert get_greeting(date) == "Добрый вечер", "Ошибка для вечернего приветствия"


def test_get_greeting_night() -> None:
    date = datetime(2025, 10, 8, 2, 0, 0)
    assert get_greeting(date) == "Доброй ночи", "Ошибка для ночного приветствия"


def test_get_greeting_edge_hours() -> None:
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
