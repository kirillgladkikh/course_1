import pytest
from decimal import Decimal
from typing import List, Dict
from src.utils import get_cards_data

# Пример тестовых данных
test_transactions = [
    {
        "card_number": "4111111111111111",
        "transaction_status": "SUCCESS",
        "transaction_amount": Decimal('1000.50'),
        "cashback_amount": Decimal('50.25')
    },
    {
        "card_number": "4222222222222222",
        "transaction_status": "SUCCESS",
        "transaction_amount": Decimal('500.00'),
        "cashback_amount": Decimal('25.00')
    },
    {
        "card_number": "4111111111111111",  # та же карта
        "transaction_status": "SUCCESS",
        "transaction_amount": Decimal('200.00'),
        "cashback_amount": Decimal('10.00')
    },
    {
        "card_number": "4333333333333333",
        "transaction_status": "FAILED",  # неудачная транзакция
        "transaction_amount": Decimal('300.00'),
        "cashback_amount": Decimal('15.00')
    },
    {
        "card_number": "",  # пустая карта
        "transaction_status": "SUCCESS",
        "transaction_amount": Decimal('400.00'),
        "cashback_amount": Decimal('20.00')
    }
]


def test_get_cards_data_basic():
    result = get_cards_data(test_transactions)
    assert len(result) == 2  # должны пройти только 2 карты

    # Проверяем данные первой карты
    card1 = next(item for item in result if item["last_digits"] == "1111")
    assert card1["total_spent"] == Decimal('1200.50')
    assert card1["cashback"] == Decimal('60.25')

    # Проверяем данные второй карты
    card2 = next(item for item in result if item["last_digits"] == "2222")
    assert card2["total_spent"] == Decimal('500.00')
    assert card2["cashback"] == Decimal('25.00')


def test_get_cards_data_empty_list():
    result = get_cards_data([])
    assert result == []


def test_get_cards_data_single_transaction():
    single_transaction = [test_transactions[0]]
    result = get_cards_data(single_transaction)
    assert len(result) == 1
    assert result[0]["last_digits"] == "1111"
    assert result[0]["total_spent"] == Decimal('1000.50')
    assert result[0]["cashback"] == Decimal('50.25')


def test_get_cards_data_failed_transactions():
    failed_transactions = [test_transactions[3]]
    result = get_cards_data(failed_transactions)
    assert result == []


def test_get_cards_data_missing_card_number():
    missing_card = [test_transactions[4]]
    result = get_cards_data(missing_card)
    assert result == []


def test_get_cards_data_multiple_transactions_same_card():
    same_card_transactions = [
        {
            "card_number": "4111111111111111",
            "transaction_status": "SUCCESS",
            "transaction_amount": Decimal('100.00'),
            "cashback_amount": Decimal('5.00')
        },
        {
            "card_number": "4111111111111111",
            "transaction_status": "SUCCESS",
            "transaction_amount": Decimal('200.00'),
            "cashback_amount": Decimal('10.00')
        },
        {
            "card_number": "4111111111111111",
            "transaction_status": "SUCCESS",
            "transaction_amount": Decimal('300.00'),
            "cashback_amount": Decimal('15.00')
        }
    ]

    result = get_cards_data(same_card_transactions)
    assert len(result) == 1  # Должна быть только одна карта

    card = result[0]
    assert card["last_digits"] == "1111"
    assert card["total_spent"] == Decimal('600.00')  # 100 + 200 + 300
    assert card["cashback"] == Decimal('30.00')  # 5 + 10 + 15


# def test_get_cards_data_invalid_amount():
#     invalid_transactions = [
#         {
#             "card_number": "4111111111111111",
#             "transaction_status": "SUCCESS",
#             "transaction_amount": "не число",  # Некорректное значение
#             "cashback_amount": Decimal('5.00')
#         },
#         {
#             "card_number": "4222222222222222",
#             "transaction_status": "SUCCESS",
#             "transaction_amount": Decimal('100.00'),
#             "cashback_amount": Decimal('5.00')
#         }
#     ]
#
#     result = get_cards_data(invalid_transactions)
#     assert len(result) == 1  # Должна пройти только вторая транзакция
#     assert result[0]["last_digits"] == "2222"


def test_get_cards_data_mixed_statuses():
    mixed_transactions = [
        {
            "card_number": "4111111111111111",
            "transaction_status": "SUCCESS",
            "transaction_amount": Decimal('100.00'),
            "cashback_amount": Decimal('5.00')
        },
        {
            "card_number": "4111111111111111",
            "transaction_status": "FAILED",
            "transaction_amount": Decimal('200.00'),
            "cashback_amount": Decimal('10.00')
        },
        {
            "card_number": "4111111111111111",
            "transaction_status": "SUCCESS",
            "transaction_amount": Decimal('300.00'),
            "cashback_amount": Decimal('15.00')
        }
    ]

    result = get_cards_data(mixed_transactions)
    assert len(result) == 1
    card = result[0]
    assert card["total_spent"] == Decimal('400.00')  # Только успешные транзакции
    assert card["cashback"] == Decimal('20.00')


# ================================================
def test_get_cards_data_invalid_amount():
    invalid_transactions = [
        {
            "card_number": "4111111111111111",
            "transaction_status": "SUCCESS",
            "transaction_amount": "не число",  # Некорректное значение
            "cashback_amount": Decimal('5.00')
        },
        {
            "card_number": "4222222222222222",
            "transaction_status": "SUCCESS",
            "transaction_amount": Decimal('100.00'),
            "cashback_amount": Decimal('5.00')
        },
        {
            "card_number": "4333333333333333",
            "transaction_status": "SUCCESS",
            "transaction_amount": None,  # None значение
            "cashback_amount": Decimal('10.00')
        }
    ]

    result = get_cards_data(invalid_transactions)
    assert len(result) == 1  # Должна пройти только вторая транзакция
    assert result[0]["last_digits"] == "2222"
    assert result[0]["total_spent"] == Decimal('100.00')
    assert result[0]["cashback"] == Decimal('5.00')

def test_get_cards_data_float_amount():
    float_transactions = [
        {
            "card_number": "4111111111111111",
            "transaction_status": "SUCCESS",
            "transaction_amount": 100.50,  # float значение
            "cashback_amount": Decimal('5.00')
        }
    ]

    result = get_cards_data(float_transactions)
    assert len(result) == 1
    assert result[0]["last_digits"] == "1111"
    assert result[0]["total_spent"] == Decimal('100.50')
    assert result[0]["cashback"] == Decimal('5.00')