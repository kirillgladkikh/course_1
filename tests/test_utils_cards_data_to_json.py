import pytest
from decimal import Decimal
from src.utils import cards_data_to_json

@pytest.fixture
def basic_card_data():
    return [
        {
            "last_digits": "1234",
            "total_spent": "1000.50",
            "cashback": "50.25"
        }
    ]

@pytest.fixture
def multiple_cards_data():
    return [
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

@pytest.fixture
def float_input_data():
    return [
        {
            "last_digits": "1234",
            "total_spent": 1000.501,
            "cashback": 50.254
        }
    ]

@pytest.fixture
def decimal_input_data():
    return [
        {
            "last_digits": "1234",
            "total_spent": Decimal('1000.50'),
            "cashback": Decimal('50.25')
        }
    ]

@pytest.fixture
def empty_list_data():
    return []

@pytest.fixture
def zero_values_data():
    return [
        {
            "last_digits": "1234",
            "total_spent": "0.00",
            "cashback": "0.00"
        }
    ]

def test_basic_conversion(basic_card_data) -> None:
    expected = [{"last_digits": "1234", "total_spent": 1000.50, "cashback": 50.25}]
    result = cards_data_to_json(basic_card_data)
    assert result == expected

def test_multiple_cards(multiple_cards_data) -> None:
    expected = [
        {"last_digits": "1234", "total_spent": 1000.50, "cashback": 50.25},
        {"last_digits": "5678", "total_spent": 200.00, "cashback": 10.00}
    ]
    result = cards_data_to_json(multiple_cards_data)
    assert result == expected

def test_float_input(float_input_data) -> None:
    expected = [{"last_digits": "1234", "total_spent": 1000.50, "cashback": 50.25}]
    result = cards_data_to_json(float_input_data)
    assert result == expected

def test_decimal_input(decimal_input_data) -> None:
    expected = [{"last_digits": "1234", "total_spent": 1000.50, "cashback": 50.25}]
    result = cards_data_to_json(decimal_input_data)
    assert result == expected

def test_empty_list(empty_list_data) -> None:
    expected = []
    result = cards_data_to_json(empty_list_data)
    assert result == expected
