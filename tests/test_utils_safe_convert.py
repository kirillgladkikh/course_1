from decimal import Decimal
from src.utils import safe_convert
import pytest


def test_safe_convert_multiple_dots() -> None:
    assert safe_convert("1.2.3.4.56") == Decimal('1234.56')
    assert safe_convert("123.45.67.89") == Decimal('1234567.89')

# Тесты для проверки корректных преобразований
def test_safe_convert_normal_number() -> None:
    assert safe_convert("1234.56") == Decimal('1234.56')

def test_safe_convert_comma_separator() -> None:
    assert safe_convert("1234,56") == Decimal('1234.56')

# def test_safe_convert_thousands_separator():
#     assert safe_convert("1.234.567") == Decimal('1234567.00')
#     assert safe_convert("1.234") == Decimal('1234.00')

def test_safe_convert_integer() -> None:
    assert safe_convert("1234") == Decimal('1234.00')

def test_safe_convert_one_decimal_digit() -> None:
    assert safe_convert("1234.5") == Decimal('1234.50')

def test_safe_convert_more_than_two_decimal_digits() -> None:
    assert safe_convert("1234.567") == Decimal('1234.57')

# Тесты для проверки граничных случаев
def test_safe_convert_empty_string() -> None:
    assert safe_convert("   ") == Decimal('0.00')
    assert safe_convert("") == Decimal('0.00')

def test_safe_convert_nan() -> None:
    assert safe_convert("NaN") == Decimal('0.00')
    assert safe_convert("nan") == Decimal('0.00')
    assert safe_convert("NAN") == Decimal('0.00')

def test_safe_convert_mixed_separators() -> None:
    assert safe_convert("1.234,56") == Decimal('1234.56')
    assert safe_convert("1,234.56") == Decimal('1234.56')
    assert safe_convert("1.234.567,89") == Decimal('1234567.89')
    assert safe_convert("123.456.789,01") == Decimal('123456789.01')

# Тесты для проверки округления
def test_safe_convert_rounding() -> None:
    assert safe_convert("1.995") == Decimal('2.00')  # округление вверх
    assert safe_convert("1.994") == Decimal('1.99')  # округление вниз
    assert safe_convert("1.9950") == Decimal('2.00')  # точное округление

# Тесты для проверки сложных случаев
def test_safe_convert_complex_cases() -> None:
    assert safe_convert("0.00") == Decimal('0.00')
    assert safe_convert("0") == Decimal('0.00')
    assert safe_convert("000.000") == Decimal('0.00')
    assert safe_convert("123.450") == Decimal('123.45')