import os
import json
import pandas as pd
import time
import math
from decimal import Decimal
from typing import Dict, List
from datetime import datetime  #, Timestamp
import os
import requests
import math
import heapq
from datetime import datetime, timedelta
from typing import List, Dict, Union
from pandas import Timestamp
from decimal import Decimal, InvalidOperation
from dotenv import load_dotenv
from pathlib import Path


def safe_convert(value: str) -> Decimal:
    """
    Безопасное преобразование строкового значения в Decimal с сохранением двух знаков после запятой.

    Функция обеспечивает надёжное преобразование различных строковых представлений чисел в тип Decimal,
    учитывая различные форматы записи чисел и возможные ошибки ввода.

    Параметры:
    value (str): входная строка для преобразования (может содержать числа в различных форматах)

    Возвращаемое значение:
    Decimal: преобразованное значение с двумя знаками после запятой
    или 0.00 при возникновении ошибки преобразования

    Поддерживаемые форматы входных данных:
    - Числа с точкой в качестве десятичного разделителя
    - Числа с запятой в качестве десятичного разделителя
    - Числа с разделителем тысяч (точки)
    - Пустые строки
    - Строки 'NaN' (в любом регистре)

    Алгоритм обработки:
    1. Проверка на пустые строки и 'NaN'
    2. Замена запятой на точку
    3. Удаление лишних пробелов
    4. Обработка разделителей тысяч
    5. Преобразование в Decimal
    6. Округление до двух знаков после запятой

    Примеры преобразования:
    - "1234.56" → Decimal('1234.56')
    - "1.234,56" → Decimal('1234.56')
    - "1.234.567" → Decimal('1234567.00')
    - "1234" → Decimal('1234.00')
    - "NaN" → Decimal('0.00')
    - "   " → Decimal('0.00')
    - "1234.5" → Decimal('1234.50')
    - "1234.567" → Decimal('1234.57')

    Обработка ошибок:
    При возникновении ошибок преобразования (ValueError, TypeError) возвращается Decimal('0.00')
    """
    try:
        # Проверка на пустые строки и NaN
        if not value.strip() or value.lower() == 'nan':
            return Decimal('0.00')

        # Замена запятой на точку
        value = value.replace(',', '.')

        # Удаление лишних пробелов
        value = value.strip()

        # Обработка разделителей тысяч
        # Находим последнюю точку как десятичный разделитель
        parts = value.rsplit('.', 1)

        # Проверка корректности разделения
        if len(parts) == 2:
            integer_part = parts[0].replace('.', '')
            decimal_part = parts[1]

            # Проверка на корректность числовых частей
            if not integer_part.isdigit() and not decimal_part.isdigit():
                return Decimal('0.00')

            value = f"{integer_part}.{decimal_part}"
        else:
            # Если нет явного десятичного разделителя
            value = value.replace('.', '')

        # Проверка на пустую строку после обработки
        if not value:
            return Decimal('0.00')

        # Проверка на корректность числового значения
        if not value.replace('.', '', 1).isdigit():
            return Decimal('0.00')

        # Преобразование в Decimal
        decimal_value = Decimal(value)

        # Форматирование до двух знаков после запятой
        return decimal_value.quantize(Decimal('0.00'))

    except (ValueError, TypeError):
        return Decimal('0.00')


# Чтение из XLS-файла в список словарей
def read_transactions_from_excel(file_path: str = "data/operations.xlsx") -> List[Dict]:
    """
    Считывает финансовые операции из Excel-файла и преобразует их в структурированный список словарей.

    Функция выполняет следующие действия:
    1. Определяет корневой каталог проекта
    2. Формирует полный путь к Excel-файлу
    3. Читает данные из файла
    4. Проверяет наличие обязательных столбцов
    5. Преобразует данные в список словарей с корректными типами

    Параметры:
    file_path (str): путь к Excel-файлу (по умолчанию "data/operations.xlsx")

    Возвращаемое значение:
    List[Dict]: список словарей, где каждый словарь представляет одну транзакцию

    Описание данных:
    transaction_date - Дата операции — дата, когда произошла транзакция.
    payment_date - Дата платежа — дата, когда был произведен платеж.
    card_number - Номер карты — последние 4 цифры номера карты.
    transaction_status - Статус — статус операции (например, OK, FAILED).
    transaction_amount - Сумма операции — сумма транзакции в оригинальной валюте.
    transaction_currency - Валюта операции — валюта, в которой была произведена транзакция.
    payment_amount - Сумма платежа — сумма транзакции в валюте счета.
    payment_currency - Валюта платежа — валюта счета.
    cashback_amount - Кешбэк — размер полученного кешбэка.
    transaction_category - Категория — категория транзакции.
    transaction_code - MCC — код категории транзакции (соответствует международной классификации).
    transaction_description - Описание — описание транзакции.
    total_bonus - Бонусы (включая кешбэк) — количество полученных бонусов (включая кешбэк).
    invest_amount_rounded - Округление на «Инвесткопилку» — сумма, которая была округлена и переведена на «Инвесткопилку».
    transaction_amount_rounded - Сумма операции с округлением — сумма транзакции, округленная до ближайшего целого числа.

        Структура каждой транзакции (поля и их описание):
    transaction_date (datetime): дата операции
    payment_date (datetime): дата платежа
    card_number (str): последние 4 цифры номера карты
    transaction_status (str): статус операции (OK, FAILED и т.д.)
    transaction_amount (Decimal): сумма операции в оригинальной валюте
    transaction_currency (str): валюта операции
    payment_amount (Decimal): сумма платежа в валюте счета
    payment_currency (str): валюта счета
    cashback_amount (Decimal): размер полученного кешбэка
    transaction_category (str): категория транзакции
    transaction_code (str): MCC-код категории транзакции
    transaction_description (str): описание транзакции
    total_bonus (Decimal): общее количество бонусов (включая кешбэк)
    invest_amount_rounded (Decimal): сумма округления на инвесткопилку
    transaction_amount_rounded (Decimal): сумма операции с округлением

    Обработка ошибок:
    - FileNotFoundError: если файл не найден, выводится сообщение и возвращается пустой список
    - ValueError: если в файле отсутствуют обязательные столбцы
    - Любые другие исключения: выводятся сообщения об ошибках

    Особенности обработки данных:
    - Даты преобразуются с учетом формата день-месяц-год
    - Пустые значения заменяются на пустые строки
    - Числовые значения конвертируются в Decimal
    - При ошибках в отдельных строках они пропускаются с выводом сообщения
    """
    try:
        # Получаем путь к корню проекта
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        # Формируем полный путь
        full_path = os.path.join(project_root, file_path)
        # print(full_path)

        # Читаем Excel файл
        df = pd.read_excel(full_path, engine="openpyxl", header=0)

        # Проверяем, что все необходимые столбцы присутствуют
        required_columns = [
            "Дата операции",
            "Дата платежа",
            "Номер карты",
            "Статус",
            "Сумма операции",
            "Валюта операции",
            "Сумма платежа",
            "Валюта платежа",
            "Кэшбэк",
            "Категория",
            "MCC",
            "Описание",
            "Бонусы (включая кэшбэк)",
            "Округление на инвесткопилку",
            "Сумма операции с округлением"
        ]

        if not all(column in df.columns for column in required_columns):
            # print(column)
            raise ValueError("Файл Excel не содержит все необходимые столбцы")

        transactions = []

        for _, row in df.iterrows():
            try:
                # Преобразуем данные с учетом типов
                transaction = {
                    "transaction_date": pd.to_datetime(row["Дата операции"], dayfirst=True, errors='coerce'),  # type: datetime  # указываем, что день идет первым  # для некорректных дат вернет NaT
                    "payment_date": pd.to_datetime(row["Дата платежа"], dayfirst=True, errors='coerce'),  # type: datetime  # указываем, что день идет первым  # для некорректных дат вернет NaT
                    "card_number": "" if str(row["Номер карты"]) == "nan" else str(row["Номер карты"]),  # type: str
                    "transaction_status": "" if str(row["Статус"]) == "nan" else str(row["Статус"]),  # type: str
                    "transaction_amount": safe_convert(str(row["Сумма платежа"])),  # type: Decimal
                    "transaction_currency": "" if str(row["Валюта операции"]) == "nan" else str(row["Валюта операции"]),  # type: str
                    "payment_amount": safe_convert(str(row["Сумма платежа"])),  # type: Decimal
                    "payment_currency": "" if str(row["Валюта платежа"]) == "nan" else str(row["Валюта платежа"]),  # type: str
                    "cashback_amount": safe_convert(str(row["Кэшбэк"])),  # type: Decimal
                    "transaction_category": "" if str(row["Категория"]) == "nan" else str(row["Категория"]),  # type: str
                    "transaction_code": "" if str(row["MCC"]) == "nan" else str(row["MCC"]),  # type: str
                    "transaction_description": "" if str(row["Описание"]) == "nan" else str(row["Описание"]),  # type: str
                    "total_bonus": safe_convert(str(row["Бонусы (включая кэшбэк)"])),  # type: Decimal
                    "invest_amount_rounded": safe_convert(str(row["Округление на инвесткопилку"])),  # type: Decimal
                    "transaction_amount_rounded": safe_convert(str(row["Сумма операции с округлением"])),  # type: Decimal
                }

                transactions.append(transaction)

            except Exception as e:
                print(f"Ошибка при обработке строки: {row}. Причина: {str(e)}")
                continue

        return transactions

    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден")
        return []

    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {str(e)}")
        return []


def read_user_settings_json(user_settings_json: str) -> dict:
    """
    Читает файл настроек пользователя в формате JSON и возвращает его содержимое в виде словаря.

    Функция определяет корневой каталог проекта, формирует полный путь к файлу настроек
    и пытается прочитать его содержимое. При успешном чтении возвращает словарь с настройками.

    Параметры:
    user_settings_json (str): Относительный путь к файлу настроек пользователя
    (например, 'config/settings.json').

    Возвращаемое значение:
    dict: Словарь с настройками пользователя при успешном чтении файла
    или пустой список в случае ошибки.

    Процесс выполнения:
    1. Определяет корневой каталог проекта
    2. Формирует полный путь к файлу настроек
    3. Открывает и читает файл в кодировке UTF-8
    4. Парсит JSON в Python-словарь

    Обработка ошибок:
    - FileNotFoundError: если файл не найден, выводится сообщение об ошибке
    - Любые другие исключения: выводится сообщение с описанием ошибки
    В обоих случаях возвращается пустой список

    Примечание:
    Файл должен быть валидным JSON-документом. При некорректном формате файла
    произойдет ошибка парсинга и будет возвращен пустой список.
    """
    try:
        # Получаем путь к корню проекта
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        # Формируем полный путь
        full_path = os.path.join(project_root, user_settings_json)
        # print(full_path)

        # Читаем JSON файл
        with open(full_path, 'r', encoding='utf-8') as file:
            user_settings = json.load(file)

        return user_settings

    except FileNotFoundError:
        print(f"Ошибка: файл {full_path} не найден")
        return []

    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {str(e)}")
        return []


# # Утилиты для модуля views.py
# def convert_date_format(date_str: str = "31.12.2021 16:44:00") -> str:
#     """
#     Конвертирует строку с датой из формата DD.MM.YYYY HH:MM:SS в формат YYYY-MM-DD HH:MM:SS.
#
#     Функция принимает строку с датой в определённом формате и возвращает её же, но в другом формате.
#     Используется для преобразования дат между популярными форматами записи.
#
#     Параметры:
#     date_str (str): Строка с датой в формате DD.MM.YYYY HH:MM:SS.
#         По умолчанию используется значение "31.12.2021 16:44:00".
#
#     Возвращаемое значение:
#     str: Строка с датой в формате YYYY-MM-DD HH:MM:SS
#         или сообщение об ошибке при некорректном вводе.
#
#     Форматы дат:
#     Исходный формат (original_format):
#     - %d: день месяца (с ведущими нулями)
#     - %m: месяц (с ведущими нулями)
#     - %Y: год (4 цифры)
#     - %H: часы (24-часовой формат)
#     - %M: минуты
#     - %S: секунды
#
#     Новый формат (new_format):
#     - %Y: год (4 цифры)
#     - %m: месяц (с ведущими нулями)
#     - %d: день месяца (с ведущими нулями)
#     - %H: часы (24-часовой формат)
#     - %M: минуты
#     - %S: секунды
#
#     Обработка ошибок:
#     При некорректном формате входной строки возвращается сообщение об ошибке.
#     """
#     try:
#         # Парсим исходную дату
#         original_format = "%d.%m.%Y %H:%M:%S"
#         new_format = "%Y-%m-%d %H:%M:%S"
#         # Преобразуем строку DD.MM.YYYY HH:MM:SS в объект datetime
#         date_obj = datetime.strptime(date_str, original_format)
#         # Форматируем объект datetime в строку формата YYYY-MM-DD HH:MM:SS
#         return date_obj.strftime(new_format)
#     except ValueError:
#         return "Ошибка: некорректный формат даты"


# FROM VIEWS.PY

# Основные функции для генерации JSON-ответа

def get_greeting(date: datetime) -> str:
    """
    Возвращает приветствие в зависимости от времени суток.

    Функция анализирует переданное время и возвращает соответствующее приветствие:
    "Доброе утро", "Добрый день", "Добрый вечер" или "Доброй ночи".

    Параметры:
    date (datetime): объект datetime, содержащий информацию о времени

    Возвращаемое значение:
    str: приветствие, соответствующее времени суток

    Логика определения приветствия:
    - 05:00 - 11:59: "Доброе утро"
    - 12:00 - 17:59: "Добрый день"
    - 18:00 - 22:59: "Добрый вечер"
    - 23:00 - 04:59: "Доброй ночи"

    Обработка ошибок:
    Если передан объект неверного типа (не datetime), возвращается сообщение об ошибке.
    """
    try:
        # Получаем час из объекта datetime
        hour = date.hour

        if 5 <= hour < 12:
            return "Доброе утро"
        elif 12 <= hour < 18:
            return "Добрый день"
        elif 18 <= hour < 23:
            return "Добрый вечер"
        else:
            return "Доброй ночи"

    except AttributeError:
        return "Ошибка: передан неверный тип данных. Ожидается объект datetime"


def get_transactions_filtered(transactions_full: List[Dict], target_datetime: Union[Timestamp, str] = Timestamp('2021-12-31 16:44:00'))-> List[Dict]:
    """
    Фильтрует список транзакций по заданному временному диапазону.

    Функция принимает полный список транзакций и целевую дату, затем возвращает
    отфильтрованный список транзакций, которые произошли в указанном месяце до
    указанной даты включительно.

    Параметры:
    transactions_full (List[Dict]): Полный список транзакций, где каждая транзакция
        представляет собой словарь с полями, включая "transaction_date".
    target_datetime (Union[Timestamp, str]): Целевая дата для фильтрации. Может быть
        передана как объект Timestamp или строка в формате 'YYYY-MM-DD HH:MM:SS'.
        По умолчанию используется дата '2021-12-31 16:44:00'.

    Возвращает:
    List[Dict]: Отфильтрованный список транзакций, содержащих только те транзакции,
        которые произошли в том же месяце, что и target_datetime, и не позже этой даты.

    Процесс фильтрации:
    1. Преобразует target_datetime в объект Timestamp, если переданная дата является строкой
    2. Определяет первый день месяца для target_datetime
    3. Фильтрует транзакции, оставляя только те, чья дата находится между первым днем месяца
        и target_datetime (включительно)

    Обработка ошибок:
    - Если transaction_date не является объектом Timestamp, транзакция пропускается
    - При возникновении ошибок KeyError или ValueError выводится сообщение об ошибке
    """
    # Обработка случая, когда transactions_full равен None
    if transactions_full is None:
        return []

    # Если target_datetime - строка, преобразуем её в Timestamp
    if isinstance(target_datetime, str):
        try:
            target_datetime = Timestamp(target_datetime)
        except Exception as e:
            print(f"Ошибка при преобразовании даты: {e}")
            return []

    # Получаем первый день месяца для указанной даты
    first_day_of_month = target_datetime.replace(day=1, hour=0, minute=0, second=0)
    input_day_of_month = target_datetime.replace(hour=0, minute=0, second=0)

    filtered_transactions = []

    for transaction in transactions_full:
        try:
            # Проверяем наличие и корректность transaction_date
            if not isinstance(transaction.get("transaction_date"), Timestamp):
                continue

            # Фильтруем по дате
            if (transaction["transaction_date"] >= first_day_of_month and
                    transaction["transaction_date"] <= target_datetime):
                filtered_transactions.append(transaction)

        except Exception as e:
            print(f"Ошибка при обработке транзакции: {e}")

    return filtered_transactions


def get_cards_data(transactions_filtered: List[Dict]) -> List[Dict]:
    """
    Анализирует список транзакций и формирует агрегированные данные по банковским картам.

    Функция обрабатывает отфильтрованные транзакции, группирует их по последним 4 цифрам карты
    и подсчитывает общую сумму потраченных средств и накопленный кешбэк для каждой карты.

    Параметры:
    transactions_filtered (List[Dict]): Список словарей с данными транзакций.
    Каждый словарь должен содержать следующие поля:
    - card_number (str): номер карты
    - transaction_status (str): статус транзакции
    - transaction_amount (float): сумма транзакции
    - cashback_amount (float): сумма кешбэка

    Возвращает:
    List[Dict]: Список словарей с агрегированными данными по картам, где:
    - last_digits (str): последние 4 цифры карты
    - total_spent (Decimal): общая сумма потраченных средств
    - cashback (Decimal): накопленный кешбэк

    Исключения:
    - Транзакции со статусом FAILED игнорируются
    - Транзакции без номера карты игнорируются
    - При ошибке преобразования числовых значений выводится предупреждение

    Пример структуры входной транзакции:
    {
        "card_number": "4111111111111111",
        "transaction_status": "SUCCESS",
        "transaction_amount": 1000.50,
        "cashback_amount": 50.25
    }

    Пример результата:
    [
        {
            "last_digits": "1111",
            "total_spent": 1500.75,
            "cashback": 75.38
        },
        ...
    ]
    """
    # Создаем словарь для хранения результатов по картам
    result = {}

    # Проходим по всем транзакциям
    for transaction in transactions_filtered:

        # Игнорируем:
        # - строки без данных карт
        # - строки со статусом FAILED
        # print(f'transaction["card_number"]: {transaction["card_number"]} {type(transaction["card_number"])}')
        if transaction["card_number"] != "" and transaction["transaction_status"] != "FAILED":

            # Извлекаем последние 4 цифры карты
            # print(f'transaction["card_number"]: {transaction["card_number"]} {type(transaction["card_number"])}')
            card_number = transaction["card_number"]
            last_digits = card_number[-4:]  # Берем последние 4 символа

            # Получаем сумму транзакции и кешбэк
            try:
                # Добавлена проверка на None
                if transaction["transaction_amount"] is None:
                    raise ValueError("Значение транзакции None")

                # Преобразование в Decimal осталось прежним
                transaction_amount = Decimal(str(transaction["transaction_amount"]))
                cashback_amount = Decimal(str(transaction["cashback_amount"]))

                # Добавлена проверка на отрицательные значения
                if transaction_amount < 0 or cashback_amount < 0:
                    raise ValueError("Отрицательные значения")

            except (ValueError, TypeError, InvalidOperation):  # Расширен список исключений
                print(f"Ошибка преобразования данных для карты {last_digits}")
                continue

            # Если карта еще не в результатах, добавляем её
            if last_digits not in result:
                result[last_digits] = {
                    "last_digits": last_digits,
                    "total_spent": Decimal('0.00'),
                    "cashback": Decimal('0.00')
                }

            # Накапливаем суммы
            result[last_digits]["total_spent"] += transaction_amount
            result[last_digits]["cashback"] += cashback_amount

        else:
            print(f"строка {transaction} не содержит данных карты")

    # Преобразуем словарь в список
    return list(result.values())


def cards_data_to_json(cards_data: List[Dict]) -> List[Dict]:
    """
    Преобразует данные банковских карт в стандартизированный JSON-формат.

    Функция принимает список словарей с данными о банковских картах и возвращает
    новый список, содержащий только необходимые поля в корректном формате.

    Параметры:
    cards_data (List[Dict]): Исходный список словарей с данными о картах.
        Каждый словарь должен содержать следующие поля:
        - last_digits (str): последние цифры номера карты
        - total_spent (str или float): общая сумма потраченных средств
        - cashback (str или float): накопленный кешбэк

    Возвращает:
    List[Dict]: Список словарей с преобразованными данными карт, где:
        - last_digits: последние цифры карты (str)
        - total_spent: общая сумма расходов (float, округленная до 2 знаков)
        - cashback: накопленный кешбэк (float, округленный до 2 знаков)

    Пример входного данных:
    [
        {
            "last_digits": "1234",
            "total_spent": "1000.50",
            "cashback": "50.25"
        },
        ...
    ]

    Пример выходного данных:
    [
        {
            "last_digits": "1234",
            "total_spent": 1000.50,
            "cashback": 50.25
        },
        ...
    ]
    """
    # Создаем новый список для транзакций
    result = []

    for card in cards_data:
        # Создаем новый список с нужными полями
        card_data = {
            "last_digits": card["last_digits"],
            "total_spent": round(float(card["total_spent"]), 2),
            "cashback": round(float(card["cashback"]), 2)
        }

        result.append(card_data)

    return result


def get_top_transactions(transactions_filtered: List[Dict]) -> List[Dict]:
    """
    Возвращает список топ-5 транзакций с наибольшими суммами платежей.

    Функция принимает отфильтрованный список транзакций и возвращает
    топ-5 транзакций, отсортированных по убыванию суммы платежа.

    Параметры:
    transactions_filtered (List[Dict]): Список словарей, где каждый словарь
    представляет собой транзакцию с различными полями, включая сумму платежа.

    Возвращает:
    List[Dict]: Список из 5 словарей с транзакциями, отсортированных по
    убыванию суммы платежа (payment_amount).

    Пример структуры входного словаря:
    {
        'transaction_id': '12345',
        'payment_amount': 1000.00,
        'date': '2025-10-15',
        'description': 'Покупка в магазине'
    }
    """
    # Используем heapq.nlargest для получения топ-5 элементов
    transactions_top = heapq.nlargest(
        5,
        transactions_filtered,
        key=lambda x: x['payment_amount']
    )

    return transactions_top


def timestamp_to_str(timestamp_date: Union[Timestamp, str]) -> str:
    """
    Преобразует временную метку (timestamp) в строку в формате даты.

    Функция принимает на вход объект Timestamp или строку, представляющую timestamp,
    и возвращает отформатированную строку с датой в формате 'ДД.ММ.ГГГГ'.

    Параметры:
    timestamp_date (Union[Timestamp, str]): Временная метка для преобразования.
        Может быть объектом Timestamp или строкой, содержащей значение timestamp.

    Возвращает:
    str: Строковое представление даты в формате 'ДД.ММ.ГГГГ'.
    """
    # Преобразуем Timestamp в datetime объект
    datetime_obj = datetime.fromtimestamp(timestamp_date.timestamp())
    formatted_date = datetime_obj.strftime('%d.%m.%Y')
    return formatted_date


def top_transactions_to_json(top_transactions: List[Dict]) -> List[Dict]:
    """
    Преобразует список транзакций в JSON-совместимый формат, выбирая и форматируя
    ключевые поля каждой транзакции.

    Параметры:
    top_transactions (List[Dict]): Список словарей с информацией о транзакциях.
        Каждый словарь должен содержать следующие ключи:
        - transaction_date (int/float): timestamp даты транзакции
        - transaction_amount (str/float): сумма транзакции
        - transaction_category (str): категория транзакции
        - transaction_description (str): описание транзакции

    Возвращает:
    List[Dict]: Новый список словарей с отформатированными данными транзакций,
        где каждый словарь содержит следующие поля:
        - date (str): отформатированная дата транзакции в формате 'YYYY-MM-DD'
        - amount (float): сумма транзакции, округленная до 2 знаков после запятой
        - category (str): категория транзакции
        - description (str): описание транзакции

    Пример входного параметра:
    [
        {
            "transaction_date": 1633072800,
            "transaction_amount": "1234.567",
            "transaction_category": "Продукты",
            "transaction_description": "Покупка в супермаркете"
        }
    ]

    Пример возвращаемого значения:
    [
        {
            "date": "2021-10-01",
            "amount": 1234.57,
            "category": "Продукты",
            "description": "Покупка в супермаркете"
        }
    ]
    """
    # Создаем новый список для транзакций
    result = []

    for transaction in top_transactions:
        # Создаем новый список с нужными полями
        top_transaction = {
            # "date": transaction["transaction_date"],  # convert_timestamp_to_date(transaction["transaction_date"]),  #.strftime('%Y-%m-%d') if transaction["transaction_date"] else "",
            "date": timestamp_to_str(transaction["transaction_date"]),
            "amount": round(float(transaction["transaction_amount"]), 2),
            "category": transaction["transaction_category"],
            "description": transaction["transaction_description"]
        }

        result.append(top_transaction)

    return result


# def get_top_transactions_test() -> List[Dict]:
#     # Пример данных с Decimal
#     transactions_sample = [
#         {'id': 1, 'payment_amount': Decimal('100.50')},
#         {'id': 2, 'payment_amount': Decimal('200.75')},
#         {'id': 3, 'payment_amount': Decimal('150.25')},
#         {'id': 4, 'payment_amount': Decimal('300.00')},
#         {'id': 5, 'payment_amount': Decimal('250.99')}
#     ]
#
#     # Использование heapq.nlargest с Decimal
#     top_transactions = heapq.nlargest(
#         5,
#         transactions_sample,
#         key=lambda x: x['payment_amount']
#     )
#
#     return top_transactions


# API
# ссылка на маркетплейс API-сервисов: https://marketplace.apilayer.com/

# На дату запроса забираем:
# курсы валют (валюты берем из файла user_settings.json)
# стоимость акций (акции берем из файла user_settings.json)

# Курсы валют (валюты берем из файла user_settings.json)
# Получаем текущую рабочую директорию
current_dir = Path().resolve()
# print(f"\nТекущая директория: {current_dir}")

# load_dotenv(".env")
# Загружаем .env
load_dotenv()

# Проверяем существование файла
dotenv_path = Path('.env')
# if not dotenv_path.is_file():
#     print(f"Файл .env не найден в директории: {current_dir}")

API_KEY_EXCHANGE_RATES = os.getenv("API_KEY_EXCHANGE_RATES")
if not API_KEY_EXCHANGE_RATES:
    raise ValueError("API ключ не найден!")

# # Выводим отладочную информацию
# print(f"load_dotenv() = {load_dotenv()}")
# print(f"dotenv_path = {dotenv_path}")
# print(f"===API_KEY_EXCHANGE_RATES = {API_KEY_EXCHANGE_RATES}")


def get_currency_rates(user_currencies: list) -> list:
    """
    Получает актуальные курсы валют по отношению к российскому рублю (RUB)
    для указанных валют через внешний API.

    Параметры:
    user_currencies (list): Список валютных кодов (например, ['USD', 'EUR', 'GBP'])

    Возвращает:
    list: Список словарей с информацией о курсах валют, где каждый словарь содержит:
        - currency (str): Код валюты
        - rate (float): Курс к RUB, округленный до 2 знаков после запятой

    Процесс работы функции:
    1. Для каждой валюты из входного списка выполняется запрос к API
    2. Используется фиксированный коэффициент конвертации (1 единица валюты)
    3. Результаты сохраняются в формате JSON
    4. Проводится проверка успешности HTTP-запроса

    Примечания:
    - Используется API: https://marketplace.apilayer.com/exchangerates_data-api
    - Конвертация производится из указанной валюты в RUB
    - В случае ошибки при получении данных для конкретной валюты,
      в результат будет записан статус с доступным значением
    - Все курсы округляются до 2 знаков после запятой
    """
    # Создаем список для хранения результатов по валютам
    result = []
    rate = "1.0"

    for item in user_currencies:
        currency = item

        # ссылка на сервис: https://marketplace.apilayer.com/exchangerates_data-api?utm_source=apilayermarketplace&utm_medium=featured
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={rate}"
        headers = {"apikey": API_KEY_EXCHANGE_RATES}


        # Выполняем GET-запрос к сайту и сохраняем ответ в переменную response
        response = requests.get(url, headers=headers)

        data = response.json()  # Преобразуем ответ в словарь

        # # Выводим отладочную информацию
        # print(f"url = {url}")
        # print(f"data = response.json() = {data}")

        if "result" in data:
            # Извлекаем из API-запроса обменный курс
            amount = data["result"]
            # # Выводим отладочную информацию
            # print(f"amount = {amount}")
        else:
            print("Предупреждение: операция без result")

        # Получаем статус-код из ответа и выводим его на экран
        status_code = response.status_code
        print(f"Статус код: {status_code}")

        # Проверяем, равен ли статус-код 200, то есть чтобы запрос был успешным
        if status_code == 200:
            # Выводим содержимое сайта на экран
            content = response.text
            print(f"Содержимое сайта:\n{content}")
        else:
            # Выводим сообщение об ошибке
            print(f"Запрос не был успешным. Возможная причина: {response.reason}")

        # Создаем новый список с нужными полями
        currency_rates = {
            "currency": currency,
            "rate": round(float(amount), 2)
        }

        result.append(currency_rates)
        print(result)

    return result


# стоимость акций (акции берем из файла user_settings.json)

API_KEY_STOCK_PRICES = os.getenv("API_KEY_STOCK_PRICES")
if not API_KEY_STOCK_PRICES:
    raise ValueError("API ключ не найден!")

# # Выводим отладочную информацию
# print(f"===API_KEY_STOCK_PRICES = {API_KEY_STOCK_PRICES}")


def get_stock_prices(user_stocks: list) -> dict:
    """
    Получает актуальные цены акций для указанных биржевых инструментов
    через API Financial Modeling Prep.

    Параметры:
    user_stocks (list): Список биржевых тикеров (например, ['AAPL', 'GOOGL', 'MSFT'])

    Возвращает:
    dict: Список словарей с информацией о ценах акций, где каждый словарь содержит:
        - stock (str): Биржевой тикер
        - price (float): Текущая цена акции, округленная до 2 знаков после запятой

    Используемый API:
    - Базовый эндпоинт: https://financialmodelingprep.com/stable/profile
    - Формат запроса: /profile?symbol={stock}&apikey={API_KEY}

    ДОКУМЕНТЫ:
    https://site.financialmodelingprep.com/developer/docs
    https://site.financialmodelingprep.com/developer/docs/pricing

    ИСПОЛЬЗУЙ ЭТО:
    https://site.financialmodelingprep.com/developer/docs/stable/peers
    https://financialmodelingprep.com/stable/profile?symbol=AAPL&apikey=...

    Пример ответа от API (сокращено):
    [
        {
            "symbol": "AAPL",
            "price": 232.8,
            "companyName": "Apple Inc.",
            "currency": "USD",
            "exchange": "NASDAQ",
            ...
        }
    ]

    Процесс работы функции:
    1. Для каждого тикера выполняется запрос к API
    2. Извлекается актуальная цена акции
    3. Проводится проверка успешности HTTP-запроса
    4. Результаты сохраняются в структурированном формате

    Примечания:
    - Функция возвращает только цену и тикер акции
    - Все цены округляются до 2 знаков после запятой
    - В случае отсутствия цены для конкретного тикера, выводится предупреждение
    - Проверяется статус-код ответа (ожидается 200)
    """
    # Создаем список для хранения результатов по валютам
    result = []

    for item in user_stocks:
        stock = item

        url_with_apikey = f"https://financialmodelingprep.com/stable/profile?symbol={stock}&apikey={API_KEY_STOCK_PRICES}"

        # Выполняем GET-запрос к сайту и сохраняем ответ в переменную response
        response = requests.get(url_with_apikey)
        data = response.json()  # Преобразуем ответ в словарь

        # # Выводим отладочную информацию
        # print(f"url_w_apikey = {url_with_apikey}")
        # print(f"response = {response}")
        # print(f"response.json() = {response.json()}")
        # print(f"data = {data}")

        if "price" in data[0]:
            # Извлекаем из API-запроса цену акции
            price = data[0]['price']  # получаем значение price

            # # Выводим отладочную информацию
            # print(f"price in 'if' = {price}")
        else:
            print("Предупреждение: операция без price")

        # Получаем статус-код из ответа и выводим его на экран
        status_code = response.status_code
        print(f"Статус код: {status_code}")

        # Проверяем, равен ли статус-код 200, то есть чтобы запрос был успешным
        if status_code == 200:
            # Выводим содержимое сайта на экран
            content = response.text
            print(f"Содержимое сайта:\n{content}")
        else:
            # Выводим сообщение об ошибке
            print(f"Запрос не был успешным. Возможная причина: {response.reason}")

        # Создаем новый список с нужными полями
        stock_prices = {
            "stock": stock,
            "price": round(float(price), 2)
        }

        result.append(stock_prices)

    return result
