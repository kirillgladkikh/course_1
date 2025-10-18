import pytest
from typing import List, Dict
import heapq
from src.utils import get_top_transactions

# Пример тестовых данных
transactions_data = [
    {
        'transaction_id': '1',
        'payment_amount': 2000.00,  # Изменено для корректности
        'date': '2025-10-13',
        'description': 'Покупка 3'
    },
    {
        'transaction_id': '2',
        'payment_amount': 1500.00,  # Изменено для корректности
        'date': '2025-10-12',
        'description': 'Покупка 4'
    },
    {
        'transaction_id': '3',
        'payment_amount': 1000.00,  # Изменено для корректности
        'date': '2025-10-15',
        'description': 'Покупка 1'
    },
    {
        'transaction_id': '4',
        'payment_amount': 500.00,
        'date': '2025-10-14',
        'description': 'Покупка 2'
    },
    {
        'transaction_id': '5',
        'payment_amount': 2500.00,
        'date': '2025-10-11',
        'description': 'Покупка 5'
    },
    {
        'transaction_id': '6',
        'payment_amount': 50.00,
        'date': '2025-10-10',
        'description': 'Покупка 6'
    }
]


def test_top_transactions():
    result = get_top_transactions(transactions_data)
    expected_amounts = [2500.00, 2000.00, 1500.00, 1000.00, 500.00]

    # Проверяем количество элементов
    assert len(result) == 5

    # Проверяем суммы в правильном порядке
    for i, transaction in enumerate(result):
        assert transaction['payment_amount'] == expected_amounts[i]


def test_less_than_five_transactions():
    # Берем первые 3 элемента из тестовых данных
    small_data = transactions_data[:3]

    # Выводим для отладки (можно убрать после проверки)
    # print("Тестовые данные:", small_data)

    result = get_top_transactions(small_data)

    # Проверяем количество элементов
    assert len(result) == 3

    # Проверяем правильные значения для первых трех элементов
    # Согласно исходным данным:
    # Первый элемент имеет payment_amount = 2000.00
    # Второй элемент имеет payment_amount = 1500.00
    # Третий элемент имеет payment_amount = 1000.00
    assert result[0]['payment_amount'] == 2000.00  # Наибольшая сумма
    assert result[1]['payment_amount'] == 1500.00  # Вторая по величине
    assert result[2]['payment_amount'] == 1000.00  # Третья по величине


def test_empty_list():
    result = get_top_transactions([])
    assert result == []


def test_equal_amounts():
    equal_data = [
        {
            'transaction_id': '1',
            'payment_amount': 1000.00,
            'date': '2025-10-15',
            'description': 'Покупка 1'
        },
        {
            'transaction_id': '2',
            'payment_amount': 1000.00,
            'date': '2025-10-14',
            'description': 'Покупка 2'
        },
        {
            'transaction_id': '3',
            'payment_amount': 1000.00,
            'date': '2025-10-13',
            'description': 'Покупка 3'
        },
        {
            'transaction_id': '4',
            'payment_amount': 1000.00,
            'date': '2025-10-12',
            'description': 'Покупка 4'
        },
        {
            'transaction_id': '5',
            'payment_amount': 1000.00,
            'date': '2025-10-11',
            'description': 'Покупка 5'
        },
        {
            'transaction_id': '6',
            'payment_amount': 1000.00,
            'date': '2025-10-10',
            'description': 'Покупка 6'
        }
    ]

    result = get_top_transactions(equal_data)

    # Проверяем, что вернулось ровно 5 транзакций
    assert len(result) == 5

    # Проверяем, что все суммы равны 1000.00
    for transaction in result:
        assert transaction['payment_amount'] == 1000.00

    # Проверяем, что transaction_id соответствуют первым 5 элементам
    expected_ids = ['1', '2', '3', '4', '5']
    actual_ids = [transaction['transaction_id'] for transaction in result]
    assert actual_ids == expected_ids
