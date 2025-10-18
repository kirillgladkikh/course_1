import pytest
from datetime import datetime
from decimal import Decimal
from typing import List, Dict
from src.utils import read_transactions_from_excel


# Пример тестового Excel файла (создать в тестовой директории)
# Для реальных тестов нужно создать файл operations_test.xlsx с тестовыми данными

def test_read_transactions_from_excel_valid_file():
    # Проверяем чтение валидного файла
    result = read_transactions_from_excel("tests/data/operations_test.xlsx")
    assert isinstance(result, list)
    assert len(result) > 0  # Предполагаем, что в тестовом файле есть данные

    # Проверяем структуру первой транзакции
    first_transaction = result[0]
    assert isinstance(first_transaction, dict)
    assert isinstance(first_transaction["transaction_date"], datetime)
    assert isinstance(first_transaction["transaction_amount"], Decimal)
    assert isinstance(first_transaction["card_number"], str)


def test_read_transactions_from_excel_missing_file():
    # Проверяем обработку отсутствующего файла
    result = read_transactions_from_excel("non_existent_file.xlsx")
    assert result == []


def test_read_transactions_from_excel_missing_columns():
    import pandas as pd
    import os
    from pathlib import Path

    # Создаем временный файл с неполными данными
    temp_df = pd.DataFrame({
        "Дата операции": ["01.01.2025"],
        "Сумма операции": [100.00]
    })

    # Создаем путь к тестовому файлу
    test_file_path = Path("tests/data/missing_columns.xlsx")
    temp_df.to_excel(test_file_path, index=False)

    try:
        # Читаем файл
        result = read_transactions_from_excel(str(test_file_path))

        # Проверяем, что результат пустой
        assert result == []

        # Проверяем, что все обязательные столбцы отсутствуют
        missing_columns = [
            "Дата платежа",
            "Номер карты",
            "Статус",
            "Валюта операции",
            "Сумма платежа",
            "Валюта платежа",
            "Кэшбэк",
            "Категория",
            "MCC",
            "Описание",
            "Бонусы (включая кэшбэк)",
            "Округление на инвесткопилку",
            "Сумма операции с округлением"
        ]

        # Проверяем отсутствие каждого столбца
        for column in missing_columns:
            assert column not in temp_df.columns

    finally:
        # Удаляем созданный тестовый файл
        if test_file_path.exists():
            os.remove(test_file_path)


def test_read_transactions_from_excel_empty_file():
    # Создаем пустой DataFrame
    import pandas as pd

    # Создаем пустой файл
    temp_df = pd.DataFrame()
    temp_df.to_excel("tests/data/empty_file.xlsx", index=False)

    result = read_transactions_from_excel("tests/data/empty_file.xlsx")
    assert result == []


def test_read_transactions_from_excel_invalid_data():
    # Создаем файл с некорректными данными
    import pandas as pd

    temp_df = pd.DataFrame({
        "Дата операции": ["некорректная дата"],
        "Сумма операции": ["abc"],
        "Номер карты": ["1234"],
        # Остальные обязательные колонки
    })
    temp_df.to_excel("tests/data/invalid_data.xlsx", index=False)

    result = read_transactions_from_excel("tests/data/invalid_data.xlsx")
    assert len(result) == 0  # Все строки должны быть пропущены из-за ошибок


def test_read_transactions_from_excel_correct_types():
    # Создаем файл с корректными данными
    import pandas as pd

    temp_df = pd.DataFrame({
        "Дата операции": ["01.01.2025"],
        "Дата платежа": ["02.01.2025"],
        "Номер карты": ["1234"],
        "Статус": ["OK"],
        "Сумма операции": [100.50],
        "Валюта операции": ["RUB"],
        "Сумма платежа": [100.50],
        "Валюта платежа": ["RUB"],
        "Кэшбэк": [5.00],
        "Категория": ["Продукты"],
        "MCC": ["5411"],
        "Описание": ["Покупка в магазине"],
        "Бонусы (включая кэшбэк)": [10.00],
        "Округление на инвесткопилку": [0.50],
        "Сумма операции с округлением": [101.00]
    })
    temp_df.to_excel("tests/data/correct_types.xlsx", index=False)

    result = read_transactions_from_excel("tests/data/correct_types.xlsx")
    transaction = result[0]