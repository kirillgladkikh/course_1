import pytest
from decimal import Decimal
from src.utils import cards_data_to_json


def test_basic_conversion():
    input_data = [
        {
            "last_digits": "1234",
            "total_spent": "1000.50",
            "cashback": "50.25"
        }
    ]

    expected = [
        {
            "last_digits": "1234",
            "total_spent": 1000.50,
            "cashback": 50.25
        }
    ]

    result = cards_data_to_json(input_data)
    assert result == expected


def test_multiple_cards():
    input_data = [
        {
            "last_digits": "1234",
            "total_spent": "1000.50",
            "cashback": "50.25"
        },
        {
            "last_digits": "5678",
            "total_spent": "200.00",
            "cashback": "10.00"
        }
    ]

    expected = [
        {
            "last_digits": "1234",
            "total_spent": 1000.50,
            "cashback": 50.25
        },
        {
            "last_digits": "5678",
            "total_spent": 200.00,
            "cashback": 10.00
        }
    ]

    result = cards_data_to_json(input_data)
    assert result == expected


def test_float_input():
    input_data = [
        {
            "last_digits": "1234",
            "total_spent": 1000.501,
            "cashback": 50.254
        }
    ]

    expected = [
        {
            "last_digits": "1234",
            "total_spent": 1000.50,
            "cashback": 50.25
        }
    ]

    result = cards_data_to_json(input_data)
    assert result == expected


def test_decimal_input():
    input_data = [
        {
            "last_digits": "1234",
            "total_spent": Decimal('1000.50'),
            "cashback": Decimal('50.25')
        }
    ]

    expected = [
        {
            "last_digits": "1234",
            "total_spent": 1000.50,
            "cashback": 50.25
        }
    ]

    result = cards_data_to_json(input_data)
    assert result == expected


def test_empty_list():
    input_data = []
    expected = []

    result = cards_data_to_json(input_data)
    assert result == expected


def test_zero_values():
    input_data = [
        {
            "last_digits": "1234",
            "total_spent": "0.00",
            "cashback": "0.00"
        }
    ]

    expected = [
        {
            "last_digits": "1234",
            "total_spent": 0.00,
            "cashback": 0.00
        }
    ]

    result = cards_data_to_json(input_data)
    assert result == expected