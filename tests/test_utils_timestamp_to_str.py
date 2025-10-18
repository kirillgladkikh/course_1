import pytest
from datetime import datetime
from typing import Union
from src.utils import timestamp_to_str


def test_timestamp_to_str():
    # Создаем объект datetime и получаем из него timestamp
    dt = datetime(2025, 10, 18)
    timestamp_obj = dt.timestamp()
    result = timestamp_to_str(timestamp_obj)
    assert result == '18.10.2025'

def test_string_timestamp():
    # Создаем строку timestamp
    dt = datetime(2025, 10, 18)
    timestamp_str = str(dt.timestamp())
    result = timestamp_to_str(float(timestamp_str))
    assert result == '18.10.2025'

def test_current_timestamp():
    # Тест с текущим timestamp
    current_timestamp = datetime.now().timestamp()
    result = timestamp_to_str(current_timestamp)
    expected = datetime.now().strftime('%d.%m.%Y')
    assert result == expected

def test_past_date():
    # Тест с прошедшей датой
    dt = datetime(2023, 1, 1)
    past_timestamp = dt.timestamp()
    result = timestamp_to_str(past_timestamp)
    assert result == '01.01.2023'

def test_future_date():
    # Тест с будущей датой
    dt = datetime(2030, 12, 31)
    future_timestamp = dt.timestamp()
    result = timestamp_to_str(future_timestamp)
    assert result == '31.12.2030'

def test_invalid_input():
    # Тест с некорректным вводом
    with pytest.raises(ValueError):
        timestamp_to_str("неверный формат")

def test_zero_timestamp():
    # Тест с нулевым timestamp
    zero_timestamp = 0
    result = timestamp_to_str(zero_timestamp)
    assert result == '01.01.1970'  # 1 января 1970 года
