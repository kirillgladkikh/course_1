import pytest
import pandas as pd
from decimal import Decimal
from src.services import investment_bank

# Тестовые данные
test_transactions = [
    {
        "transaction_date": pd.Timestamp('2021-12-01 18:12:17'),
        "payment_amount": Decimal('1712.00')
    },
    {
        "transaction_date": pd.Timestamp('2021-12-05 18:12:17'),
        "payment_amount": Decimal('345.00')
    },
    {
        "transaction_date": pd.Timestamp('2021-12-10 18:12:17'),
        "payment_amount": Decimal('89.00')
    },
    {
        "transaction_date": pd.Timestamp('2022-01-01 18:12:17'),  # другая дата
        "payment_amount": Decimal('100.00')
    }
]


def test_investment_bank_basic():
    # Базовый тест с лимитом 50
    # Расчёт:
    # 1712.00 → 1750.00 (разница 38.00)
    # 345.00 → 350.00 (разница 5.00)
    # 89.00 → 100.00 (разница 11.00)
    # Итого: 38.00 + 5.00 + 11.00 = 54.00
    result = investment_bank(
        transactions=test_transactions,
        month='2021-12',
        limit=Decimal('50')
    )
    assert result == Decimal('54.00')


def test_investment_bank_limit_10():
    # Тест с лимитом 10
    # Расчёт:
    # 1712.00 → 1720.00 (разница 8.00)
    # 345.00 → 350.00 (разница 5.00)
    # 89.00 → 90.00 (разница 1.00)
    # Итого: 8.00 + 5.00 + 1.00 = 14.00
    result = investment_bank(
        transactions=test_transactions,
        month='2021-12',
        limit=Decimal('10')
    )
    assert result == Decimal('14.00')  # Исправлено ожидаемое значение


def test_investment_bank_limit_100():
    # Тест с лимитом 100
    # Расчёт:
    # 1712.00 → 1800.00 (разница 88.00)
    # 345.00 → 400.00 (разница 55.00)
    # 89.00 → 100.00 (разница 11.00)
    # Итого: 88.00 + 55.00 + 11.00 = 154.00
    result = investment_bank(
        transactions=test_transactions,
        month='2021-12',
        limit=Decimal('100')
    )
    assert result == Decimal('154.00')


def test_investment_bank_empty_month():
    # Тест с пустым месяцем
    result = investment_bank(
        transactions=test_transactions,
        month='2022-02',  # месяц без транзакций
        limit=Decimal('50')
    )
    assert result == Decimal('0.00')

def test_investment_bank_single_transaction():
    # Тест с одной транзакцией
    single_transaction = [
        {
            "transaction_date": pd.Timestamp('2021-12-01 18:12:17'),
            "payment_amount": Decimal('47.00')
        }
    ]
    result = investment_bank(
        transactions=single_transaction,
        month='2021-12',
        limit=Decimal('50')
    )
    assert result == Decimal('3.00')

def test_investment_bank_exact_limit():
    # Тест с суммой, кратной лимиту
    exact_transaction = [
        {
            "transaction_date": pd.Timestamp('2021-12-01 18:12:17'),
            "payment_amount": Decimal('100.00')
        }
    ]
    result = investment_bank(
        transactions=exact_transaction,
        month='2021-12',
        limit=Decimal('50')
    )
    assert result == Decimal('0.00')

def test_investment_bank_decimal_amount():
    # Тест с десятичной суммой
    decimal_transaction = [
        {
            "transaction_date": pd.Timestamp('2021-12-01 18:12:17'),
            "payment_amount": Decimal('47.50')
        }
    ]
    result = investment_bank(
        transactions=decimal_transaction,
        month='2021-12',
        limit=Decimal('50')
    )
    assert result == Decimal('2.50')