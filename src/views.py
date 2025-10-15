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

def get_greeting(date: Union[Timestamp, str]) -> str:
    """
    Определение приветствия по времени суток
    Принимает объект datetime в формате 'YYYY-MM-DD HH:MM:SS'
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
    Фильтрует транзакции по дате: от начала месяца до указанной даты.

    Параметры:
    transactions_full (List[Dict]): список всех транзакций
    target_datetime (Union[Timestamp, str]): объект Timestamp или строка с датой в формате "YYYY-MM-DD HH:MM:SS"

    Возвращает:
    List[Dict]: отфильтрованный список транзакций
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
    Анализирует список транзакций и агрегирует данные по банковским картам.

    Функция обрабатывает список транзакций, группируя их по последним 4 цифрам
    номера карты. Для каждой карты подсчитывается общая сумма потраченных средств
    и накопленный кешбэк.

    Параметры:
    transactions_filtered (list): список словарей с данными транзакций, где каждый
        словарь содержит следующие ключи:
        - card_number (str/int): номер карты (может быть строкой или числом)
        - transaction_amount (str/float): сумма транзакции (число или строка с числом)
        - cashback_amount (str/float): сумма кешбэка (число или строка с числом)

    Возвращаемое значение:
    list: список словарей с агрегированными данными по картам, где каждый словарь
        содержит:
        - last_digits (str): последние 4 цифры номера карты
        - total_spent (Decimal): общая сумма потраченных средств
        - cashback (Decimal): накопленный кешбэк

    Особенности обработки:
    1. Номера карт обрабатываются как строки для корректной работы с ведущими нулями
    2. Транзакции без номера карты игнорируются
    3. При ошибках преобразования числовых значений транзакция пропускается
    4. Суммы хранятся в типе Decimal для точности вычислений
    5. Результат сортируется по убыванию общей суммы потраченных средств
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
    Преобразует список транзакций в сокращенный формат с основными полями

    Args:
        ----------------transactions: список транзакций в исходной структуре

    Returns:
        ----------------список сокращенных транзакций с основными полями
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
    Возвращает список из 5 транзакций с наибольшими значениями payment_amount
    с использованием heapq.nlargest
    """
    # Используем heapq.nlargest для получения топ-5 элементов
    transactions_top = heapq.nlargest(
        5,
        transactions_filtered,
        key=lambda x: x['payment_amount']
    )

    return transactions_top


def timestamp_to_str(timestamp_date: Union[Timestamp, str]) -> str:
    """ """
    # Преобразуем Timestamp в datetime объект
    datetime_obj = datetime.fromtimestamp(timestamp_date.timestamp())
    formatted_date = datetime_obj.strftime('%d.%m.%Y')
    return formatted_date


def top_transactions_to_json(top_transactions: List[Dict]) -> List[Dict]:
    """
    Преобразует список транзакций в сокращенный формат с основными полями

    Args:
        transactions: список транзакций в исходной структуре

    Returns:
        список сокращенных транзакций с основными полями
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

    # курсы валют (валюты берем из файла user_settings.json)

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
    """ """
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
    """ """
    # Создаем список для хранения результатов по валютам
    result = []

    for item in user_stocks:
        stock = item

        # ДОКУМЕНТЫ:
        # https://site.financialmodelingprep.com/developer/docs
        # https://site.financialmodelingprep.com/developer/docs/pricing

        # ИСПОЛЬЗУЙ ЭТО:
        # https://site.financialmodelingprep.com/developer/docs/stable/peers
        # https://financialmodelingprep.com/stable/profile?symbol=AAPL&apikey=...
        # RESPONSE:
        # [
        #     {
        #         "symbol": "AAPL",
        #         "price": 232.8,
        #         "marketCap": 3500823120000,
        #         "beta": 1.24,
        #         "lastDividend": 0.99,
        #         "range": "164.08-260.1",
        #         "change": 4.79,
        #         "changePercentage": 2.1008,
        #         "volume": 0,
        #         "averageVolume": 50542058,
        #         "companyName": "Apple Inc.",
        #         "currency": "USD",
        #         "cik": "0000320193",
        #         "isin": "US0378331005",
        #         "cusip": "037833100",
        #         "exchangeFullName": "NASDAQ Global Select",
        #         "exchange": "NASDAQ",
        #         "industry": "Consumer Electronics",
        #         "website": "https://www.apple.com",
        #         "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. The company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, and HomePod. It also provides AppleCare support and cloud services; and operates various platforms, including the App Store that allow customers to discov...",
        #         "ceo": "Mr. Timothy D. Cook",
        #         "sector": "Technology",
        #         "country": "US",
        #         "fullTimeEmployees": "164000",
        #         "phone": "(408) 996-1010",
        #         "address": "One Apple Park Way",
        #         "city": "Cupertino",
        #         "state": "CA",
        #         "zip": "95014",
        #         "image": "https://images.financialmodelingprep.com/symbol/AAPL.png",
        #         "ipoDate": "1980-12-12",
        #         "defaultImage": false,
        #         "isEtf": false,
        #         "isActivelyTrading": true,
        #         "isAdr": false,
        #         "isFund": false
        #     }
        # ]

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
