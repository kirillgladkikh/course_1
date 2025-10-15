import os
import json
import pandas as pd
import time
import math
from decimal import Decimal
from typing import Dict, List
from datetime import datetime  #, Timestamp


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

        # Замена запятой на точку для корректного преобразования
        value = value.replace(',', '.')

        # Удаление лишних пробелов
        value = value.strip()

        # Обработка случая с разделителем тысяч
        if '.' in value:
            # Разделяем целую и дробную части
            parts = value.split('.')
            # Если после точки только нули или одна цифра, считаем это разделителем тысяч
            if len(parts) == 2 and (len(parts[1]) == 1 or parts[1] == '00'):
                value = parts[0].replace('.', '') + '.' + parts[1]

        # Проверка на пустую строку после обработки
        if not value:
            return Decimal('0.00')

        # Преобразование в Decimal
        decimal_value = Decimal(value)

        # Форматирование до двух знаков после запятой
        return decimal_value.quantize(Decimal('0.00'))

    except (ValueError, TypeError):
        # Обработка ошибок преобразования
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

    Пример использования:
    >>> transactions = read_transactions_from_excel('data/operations.xlsx')
    >>> print(transactions[0])
    {
        'transaction_date': datetime.datetime(2023, 10, 15, 0, 0),
        'payment_date': datetime.datetime(2023, 10, 15, 0, 0),
        'card_number': '1234',
        'transaction_status': 'OK',
        'transaction_amount': Decimal('1000.00'),
        ...
    }
    """
    try:
        # Получаем путь к корню проекта
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        # Формируем полный путь
        full_path = os.path.join(project_root, file_path)
        print(full_path)
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


# Чтение из JSON-файла в ===============================================================список словарей
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

    Пример использования:
    >>> settings = read_user_settings_json('config/user_settings.json')
    >>> print(settings)
    {'username': 'admin', 'theme': 'dark', 'notifications': True}

    Примечание:
    Файл должен быть валидным JSON-документом. При некорректном формате файла
    произойдет ошибка парсинга и будет возвращен пустой список.
    """
    try:
        # Получаем путь к корню проекта
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        # Формируем полный путь
        full_path = os.path.join(project_root, user_settings_json)
        print(full_path)

        # Читаем JSON файл
        with open(full_path, 'r', encoding='utf-8') as file:
            user_settings = json.load(file)

        return user_settings

    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден")
        return []

    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {str(e)}")
        return []


# Утилиты для модуля views.py


def convert_date_format(date_str: str = "31.12.2021 16:44:00") -> str:
    """
    Конвертирует строку с датой из формата DD.MM.YYYY HH:MM:SS в формат YYYY-MM-DD HH:MM:SS.

    Функция принимает строку с датой в определённом формате и возвращает её же, но в другом формате.
    Используется для преобразования дат между популярными форматами записи.

    Параметры:
    date_str (str): Строка с датой в формате DD.MM.YYYY HH:MM:SS.
        По умолчанию используется значение "31.12.2021 16:44:00".

    Возвращаемое значение:
    str: Строка с датой в формате YYYY-MM-DD HH:MM:SS
        или сообщение об ошибке при некорректном вводе.

    Форматы дат:
    Исходный формат (original_format):
    - %d: день месяца (с ведущими нулями)
    - %m: месяц (с ведущими нулями)
    - %Y: год (4 цифры)
    - %H: часы (24-часовой формат)
    - %M: минуты
    - %S: секунды

    Новый формат (new_format):
    - %Y: год (4 цифры)
    - %m: месяц (с ведущими нулями)
    - %d: день месяца (с ведущими нулями)
    - %H: часы (24-часовой формат)
    - %M: минуты
    - %S: секунды

    Обработка ошибок:
    При некорректном формате входной строки возвращается сообщение об ошибке.

    Примеры использования:
    >>> convert_date_format("31.12.2021 16:44:00")
    '2021-12-31 16:44:00'

    >>> convert_date_format("01.01.2022 00:00:00")
    '2022-01-01 00:00:00'

    >>> convert_date_format("30.02.2021 12:30:45")  # Некорректная дата
    'Ошибка: некорректный формат даты'
    """
    try:
        # Парсим исходную дату
        original_format = "%d.%m.%Y %H:%M:%S"
        new_format = "%Y-%m-%d %H:%M:%S"
        # Преобразуем строку DD.MM.YYYY HH:MM:SS в объект datetime
        date_obj = datetime.strptime(date_str, original_format)
        # Форматируем объект datetime в строку формата YYYY-MM-DD HH:MM:SS
        return date_obj.strftime(new_format)
    except ValueError:
        return "Ошибка: некорректный формат даты"





# Функции для utils.py
# Основные категории функций
# Utils.py — это файл для хранения вспомогательных функций, которые можно повторно использовать в проекте.
# Вот основные категории функций, которые стоит включить:
#
# 1. Работа с данными
# Загрузка данных:
#
# load_data() — загрузка данных из файлов или баз данных
#
# read_csv() — чтение CSV-файлов
#
# read_json() — чтение JSON-файлов
#
# read_excel() — чтение Excel-файлов
#
# Парсинг данных:
#
# parse_data() — преобразование данных в стандартный формат
#
# extract_values() — извлечение определенных значений
#
# clean_data() — очистка данных от мусора
#
# 2. Валидация
# Проверка данных:
#
# validate_input() — валидация пользовательского ввода
#
# check_data_type() — проверка типов данных
#
# validate_format() — проверка формата данных
#
# check_constraints() — проверка на соответствие ограничениям
#
# 3. Математические операции
# Статистические функции:
#
# calculate_mean() — вычисление среднего значения
#
# calculate_median() — вычисление медианы
#
# calculate_mode() — вычисление моды
#
# calculate_std() — вычисление стандартного отклонения
#
# 4. Утилиты для работы с файлами
# Операции с файлами:
#
# save_to_file() — сохранение данных в файл
#
# delete_file() — удаление файла
#
# check_file_exists() — проверка существования файла
#
# get_file_size() — получение размера файла
#
# 5. Строковые операции
# Обработка строк:
#
# format_string() — форматирование строк
#
# clean_string() — очистка строк от лишних символов
#
# convert_case() — преобразование регистра
#
# truncate_string() — обрезка строк
#
# 6. Сетевые функции
# Работа с сетью:
#
# make_request() — выполнение HTTP-запросов
#
# check_connection() — проверка сетевого подключения
#
# download_file() — загрузка файлов
#
# upload_file() — загрузка файлов на сервер
#
# Рекомендации по организации
# Используйте понятные и описательные имена функций
#
# Добавляйте докстринги к каждой функции
#
# Обрабатывайте исключения внутри функций
#
# Группируйте функции по категориям
#
# Добавляйте комментарии к сложным функциям
#
# Пример структуры файла


# def load_data(file_path):
#     """Загрузка данных из файла"""
#     try:
#         # код загрузки
#         pass
#     except Exception as e:
#         print(f"Ошибка: {e}")
#         return None
#
# def validate_input(data):
#     """Валидация входных данных"""
#     # код валидации
#     return True
#
# def calculate_mean(values):
#     """Вычисление среднего значения"""
#     try:
#         return sum(values) / len(values)
#     except Exception as e:
#         print(f"Ошибка: {e}")
#         return None
# Такой подход к организации utils.py поможет сделать ваш код более структурированным, поддерживаемым и масштабируемым.
