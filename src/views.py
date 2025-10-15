import os
import requests
import math
import heapq
from datetime import datetime, timedelta
from typing import List, Dict, Union
from pandas import Timestamp
from decimal import Decimal
from dotenv import load_dotenv
from pathlib import Path
# from utils import convert_timestamp_to_date


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

    Примеры использования:
    >>> get_greeting(datetime(2025, 10, 15, 9, 0))
    'Доброе утро'

    >>> get_greeting(datetime(2025, 10, 15, 14, 30))
    'Добрый день'

    >>> get_greeting(datetime(2025, 10, 15, 19, 45))
    'Добрый вечер'

    >>> get_greeting(datetime(2025, 10, 15, 2, 15))
    'Доброй ночи'
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

    Пример использования:
    >>> transactions = [
    ...     {'transaction_date': Timestamp('2021-12-15 10:00:00'), 'amount': 100},
    ...     {'transaction_date': Timestamp('2021-12-30 15:00:00'), 'amount': 200},
    ...     {'transaction_date': Timestamp('2022-01-05 12:00:00'), 'amount': 300}
    ... ]
    >>> get_transactions_filtered(transactions, Timestamp('2021-12-31'))
    [
        {'transaction_date': Timestamp('2021-12-15 10:00:00'), 'amount': 100},
        {'transaction_date': Timestamp('2021-12-30 15:00:00'), 'amount': 200}
    ]
    """
    # Если target_datetime - строка, преобразуем её в Timestamp
    if isinstance(target_datetime, str):
        target_datetime = Timestamp(target_datetime)

    # Получаем первый день месяца для указанной даты
    first_day_of_month = target_datetime.replace(day=1, hour=0, minute=0, second=0)
    input_day_of_month = target_datetime.replace(hour=0, minute=0, second=0)

    filtered_transactions = []

    for transaction in transactions_full:

        try:
            # Получаем дату транзакции
            date_obj = transaction["transaction_date"]

            # Проверяем тип date_obj
            if not isinstance(date_obj, Timestamp):
                raise ValueError("transaction_date не является Timestamp")

            # print(f"\nfirst_day_of_month {first_day_of_month} <= date_obj {date_obj} <= input_day_of_month {input_day_of_month}")

            # Проверяем, попадает ли дата транзакции в нужный диапазон
            if first_day_of_month <= date_obj <= input_day_of_month:

                # print(f"transaction in transactions_full {transaction}")

                filtered_transactions.append(transaction)

                # print(f"transaction in filtered_transactions {filtered_transactions[-1]}")

        except (KeyError, ValueError) as e:
            print(f"Ошибка при обработке транзакции: {e}")
            continue

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
                # Преобразуем строки в числа, если они хранятся как строки
                # transaction_amount = float(transaction["transaction_amount"])

                transaction_amount = transaction["transaction_amount"]
                cashback_amount = transaction["cashback_amount"]

                # print(f'transaction["cashback_amount"]: {transaction["cashback_amount"]} {type(transaction["cashback_amount"])}')
                # print(f'cashback_amount: {cashback_amount} {type(cashback_amount)}')

            except ValueError:
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

    Пример использования:
    >>> transactions = [
    ...     {'payment_amount': 1000},
    ...     {'payment_amount': 5000},
    ...     {'payment_amount': 2000},
    ...     {'payment_amount': 3000},
    ...     {'payment_amount': 4000},
    ...     {'payment_amount': 1500}
    ... ]
    >>> get_top_transactions(transactions)
    [
        {'payment_amount': 5000},
        {'payment_amount': 4000},
        {'payment_amount': 3000},
        {'payment_amount': 2000},
        {'payment_amount': 1500}
    ]
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

    Пример использования:
    >>> timestamp_to_str(1609459200)
    '01.01.2021'
    >>> timestamp_to_str(Timestamp('2021-01-01'))
    '01.01.2021'
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


def get_top_transactions_test() -> List[Dict]:
    # Пример данных с Decimal
    transactions_sample = [
        {'id': 1, 'payment_amount': Decimal('100.50')},
        {'id': 2, 'payment_amount': Decimal('200.75')},
        {'id': 3, 'payment_amount': Decimal('150.25')},
        {'id': 4, 'payment_amount': Decimal('300.00')},
        {'id': 5, 'payment_amount': Decimal('250.99')}
    ]

    # Использование heapq.nlargest с Decimal
    top_transactions = heapq.nlargest(
        5,
        transactions_sample,
        key=lambda x: x['payment_amount']
    )

    return top_transactions


# API
# ссылка на маркетплейс API-сервисов: https://marketplace.apilayer.com/

# На дату запроса забираем:
# курсы валют (валюты берем из файла user_settings.json)
# стоимость акций (акции берем из файла user_settings.json)

# Курсы валют (валюты берем из файла user_settings.json)
# Получаем текущую рабочую директорию
current_dir = Path().resolve()
print(f"\nТекущая директория: {current_dir}")

# load_dotenv(".env")
# Загружаем .env
load_dotenv()
print(f"load_dotenv() = {load_dotenv()}")

# Проверяем существование файла
dotenv_path = Path('.env')
print(f"dotenv_path = {dotenv_path}")
if not dotenv_path.is_file():
    print(f"Файл .env не найден в директории: {current_dir}")

API_KEY_EXCHANGE_RATES = os.getenv("API_KEY_EXCHANGE_RATES")
print(f"===API_KEY_EXCHANGE_RATES = {API_KEY_EXCHANGE_RATES}")
if not API_KEY_EXCHANGE_RATES:
    raise ValueError("API ключ не найден!")


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

    Пример использования:
    >>> get_currency_rates(['USD', 'EUR'])
    [
        {'currency': 'USD', 'rate': 92.50},
        {'currency': 'EUR': 'rate': 101.75}
    ]

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
        print(f"url = {url}")

        # Выполняем GET-запрос к сайту и сохраняем ответ в переменную response
        response = requests.get(url, headers=headers)

        data = response.json()  # Преобразуем ответ в словарь
        print(f"data = response.json() = {data}")

        if "result" in data:
            # Извлекаем из API-запроса обменный курс
            amount = data["result"]
            print(f"amount = {amount}")
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
print(f"===API_KEY_STOCK_PRICES = {API_KEY_STOCK_PRICES}")
if not API_KEY_STOCK_PRICES:
    raise ValueError("API ключ не найден!")


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

    Пример использования:
    >>> get_stock_prices(['AAPL', 'MSFT'])
    [
        {'stock': 'AAPL', 'price': 232.80},
        {'stock': 'MSFT', 'price': 345.67}
    ]

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
        print(f"url_w_apikey = {url_with_apikey}")

        # Выполняем GET-запрос к сайту и сохраняем ответ в переменную response
        response = requests.get(url_with_apikey)  #, headers=headers)
        print(f"response = {response}")

        data = response.json()  # Преобразуем ответ в словарь
        print(f"response.json() = {response.json()}")
        print(f"data = {data}")

        if "price" in data[0]:
            # Извлекаем из API-запроса цену акции
            price = data[0]['price']  # получаем значение price
            print(f"price in 'if' = {price}")
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


def views_main_eventspage():
    """ """
    pass
