import pytest
import json
import os
from pathlib import Path
from src.utils import read_user_settings_json

# Пример тестового JSON файла
TEST_SETTINGS = {
    "user_id": 12345,
    "language": "ru",
    "notifications": {
        "email": True,
        "sms": False
    },
    "theme": "dark"
}


def test_read_user_settings_json_valid_file():
    # Создаем временный тестовый файл
    test_file = Path("tests/data/test_settings.json")
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(TEST_SETTINGS, f)

    try:
        result = read_user_settings_json(str(test_file))
        assert isinstance(result, dict)
        assert result == TEST_SETTINGS
        assert result["user_id"] == 12345
        assert result["language"] == "ru"
        assert result["notifications"]["email"] is True

    finally:
        # Удаляем тестовый файл
        if test_file.exists():
            os.remove(test_file)


def test_read_user_settings_json_missing_file():
    # Проверяем обработку отсутствующего файла
    result = read_user_settings_json("non_existent_file.json")
    assert result == []


def test_read_user_settings_json_invalid_json():
    # Создаем файл с некорректным JSON
    test_file = Path("tests/data/invalid_settings.json")
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("{invalid json without quotes}")

    try:
        result = read_user_settings_json(str(test_file))
        assert result == []

    finally:
        # Удаляем тестовый файл
        if test_file.exists():
            os.remove(test_file)


def test_read_user_settings_json_empty_file():
    # Создаем пустой JSON файл
    test_file = Path("tests/data/empty_settings.json")
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("")

    try:
        result = read_user_settings_json(str(test_file))
        assert result == []

    finally:
        # Удаляем тестовый файл
        if test_file.exists():
            os.remove(test_file)


def test_read_user_settings_json_correct_types():
    # Создаем файл с корректными типами данных
    test_file = Path("tests/data/correct_types.json")
    test_data = {
        "integer": 123,
        "float": 123.45,
        "boolean": True,
        "string": "test",
        "array": [1, 2, 3],
        "object": {"key": "value"}
    }
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f)

    try:
        result = read_user_settings_json(str(test_file))
        assert isinstance(result["integer"], int)
        assert isinstance(result["float"], float)
        assert isinstance(result["boolean"], bool)
        assert isinstance(result["string"], str)
        assert isinstance(result["array"], list)
        assert isinstance(result["object"], dict)

    finally:
        # Удаляем тестовый файл
        if test_file.exists():
            os.remove(test_file)