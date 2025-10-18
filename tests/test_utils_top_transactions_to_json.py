import pytest
from typing import List, Dict
from datetime import datetime
from src.utils import top_transactions_to_json

# Пример тестовых данных
test_transactions = [
    {
        "transaction_date": 1633072800,  # 2021-10-01
        "transaction_amount": "1234.567",
        "transaction_category": "Продукты",
        "transaction_description": "Покупка в супермаркете"
    },
    {
        "transaction_date": 1707504000,  # 2024-02-09
        "transaction_amount": 500.0,
        "transaction_category": "Транспорт",
        "transaction_description": "Проезд в метро"
    },
    {
        "transaction_date": 0,  # 1970-01-01
        "transaction_amount": "0.99",
        "transaction_category": "Другое",
        "transaction_description": "Тестовая транзакция"
    }
]


def test_top_transactions_to_json():
    # Базовый тест с несколькими транзакциями
    result = top_transactions_to_json(test_transactions)

    # Проверяем количество элементов
    assert len(result) == 3

    # Проверяем первую транзакцию
    assert result[0]["date"] == "01.10.2021"
    assert result[0]["amount"] == 1234.57
    assert result[0]["category"] == "Продукты"
    assert result[0]["description"] == "Покупка в супермаркете"

    # Проверяем вторую транзакцию
    assert result[1]["date"] == "09.02.2024"  # Исправлено на актуальную дату
    assert result[1]["amount"] == 500.00
    assert result[1]["category"] == "Транспорт"

    # Проверяем третью транзакцию
    assert result[2]["date"] == "01.01.1970"
    assert result[2]["amount"] == 0.99


def test_empty_list():
    # Тест с пустым списком
    result = top_transactions_to_json([])
    assert result == []


def test_single_transaction():
    # Тест с одной транзакцией
    single_transaction = [
        {
            "transaction_date": 1707504000,  # 2024-02-09
            "transaction_amount": "100.00",
            "transaction_category": "Развлечения",
            "transaction_description": "Кинотеатр"
        }
    ]

    result = top_transactions_to_json(single_transaction)
    assert len(result) == 1
    assert result[0]["date"] == "09.02.2024"  # Исправлено на актуальную дату
    assert result[0]["amount"] == 100.00


def test_zero_amount():
    # Тест с нулевой суммой
    zero_amount_transaction = [
        {
            "transaction_date": 1707504000,
            "transaction_amount": "0",
            "transaction_category": "Другое",
            "transaction_description": "Возврат"
        }
    ]

    result = top_transactions_to_json(zero_amount_transaction)
    assert result[0]["amount"] == 0.00


def test_invalid_amount():
    # Тест с некорректной суммой
    invalid_amount_transaction = [
        {
            "transaction_date": 1707504000,
            "transaction_amount": "abc",
            "transaction_category": "Другое",
            "transaction_description": "Ошибка"
        }
    ]

    with pytest.raises(ValueError):
        top_transactions_to_json(invalid_amount_transaction)