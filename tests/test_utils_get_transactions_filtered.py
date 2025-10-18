import pytest
from datetime import datetime
from pandas import Timestamp
from typing import List, Dict, Union
from src.utils import get_transactions_filtered

# Обновленные тестовые данные
test_transactions = [
{
    "transaction_date": Timestamp('2021-12-15 10:00:00'),
    "amount": 1000,
    "description": "Покупка 1"
},
{
    "transaction_date": Timestamp('2021-12-31 16:44:00'),
    "amount": 2000,
    "description": "Покупка 2"
},
{
    "transaction_date": Timestamp('2021-12-25 14:30:00'),
    "amount": 1500,
    "description": "Покупка 3"
},
{
    "transaction_date": Timestamp('2021-11-30 23:59:59'),
    "amount": 500,
    "description": "Покупка 4"  # Не должна попасть в фильтр
},
{
    "transaction_date": Timestamp('2022-01-01 00:00:00'),
    "amount": 3000,
    "description": "Покупка 5"  # Не должна попасть в фильтр
}
]

def test_get_transactions_filtered_default_date():
    # Проверяем фильтрацию по дате по умолчанию
    result = get_transactions_filtered(test_transactions)
    assert len(result) == 3  # Только 3 транзакции попадают под фильтр
    for transaction in result:
        assert transaction["transaction_date"].month == 12


def test_get_transactions_filtered_string_date():
    # Проверяем фильтрацию при передаче строки
    target_date_str = '2021-12-31 16:44:00'
    result = get_transactions_filtered(test_transactions, target_date_str)
    assert len(result) == 3  # Все валидные декабрьские транзакции


def test_get_transactions_filtered_empty_list():
    # Проверяем обработку пустого списка транзакций
    result = get_transactions_filtered([])
    assert result == []

    # Проверяем обработку None
    result = get_transactions_filtered(None)
    assert result == []


# ==========================================
def test_get_transactions_filtered_single_transaction():
    # Тест с одной транзакцией
    single_transaction = [
        {
            "transaction_date": Timestamp('2021-12-15 10:00:00'),
            "amount": 1000,
            "description": "Покупка 1"
        }
    ]
    result = get_transactions_filtered(single_transaction)
    assert len(result) == 1
    assert result[0]["amount"] == 1000

def test_get_transactions_filtered_no_matching_transactions():
    # Тест с транзакциями из другого месяца
    other_month_transactions = [
        {
            "transaction_date": Timestamp('2021-11-15 10:00:00'),
            "amount": 1000,
            "description": "Покупка 1"
        },
        {
            "transaction_date": Timestamp('2022-01-15 10:00:00'),
            "amount": 2000,
            "description": "Покупка 2"
        }
    ]
    result = get_transactions_filtered(other_month_transactions)
    assert len(result) == 0

def test_get_transactions_filtered_exact_target_date():
    # Тест с точной датой
    target_date = Timestamp('2021-12-25 14:30:00')
    result = get_transactions_filtered(test_transactions, target_date)
    assert len(result) == 2  # Должны попасть транзакции до 25 декабря включительно
    assert result[-1]["description"] == "Покупка 3"

def test_get_transactions_filtered_early_target_date():
    # Тест с ранней датой
    target_date = Timestamp('2021-12-10 00:00:00')
    result = get_transactions_filtered(test_transactions, target_date)
    assert len(result) == 0  # Нет транзакций до 10 декабря

def test_get_transactions_filtered_missing_transaction_date():
    # Тест с транзакцией без даты
    transactions = [
        {
            "amount": 1000,
            "description": "Покупка без даты"
        },
        test_transactions[0]  # Добавляем валидную транзакцию
    ]
    result = get_transactions_filtered(transactions)
    assert len(result) == 1  # Должна пройти только валидная транзакция

def test_get_transactions_filtered_invalid_timestamp():
    # Тест с некорректным Timestamp
    invalid_transactions = [
        {
            "transaction_date": "2021-12-15 10:00:00",  # Строка вместо Timestamp
            "amount": 1000,
            "description": "Покупка 1"
        },
        test_transactions[1]  # Добавляем валидную транзакцию
    ]
    result = get_transactions_filtered(invalid_transactions)
    assert len(result) == 1  # Должна пройти только валидная транзакция

def test_get_transactions_filtered_different_time():
    # Тест с разными временными отметками
    target_date = Timestamp('2021-12-15 09:00:00')  # Время раньше транзакции
    result = get_transactions_filtered(test_transactions, target_date)
    assert len(result) == 0  # Транзакция в 10:00 не должна попасть

    target_date = Timestamp('2021-12-15 11:00:00')  # Время позже транзакции
    result = get_transactions_filtered(test_transactions, target_date)
    assert len(result) == 1  # Транзакция в 10:00 должна попасть