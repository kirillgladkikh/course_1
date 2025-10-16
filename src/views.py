import os
import json
from datetime import datetime
from pandas import Timestamp
from decimal import Decimal
from src.utils import read_transactions_from_excel, read_user_settings_json, get_transactions_filtered, get_greeting, get_cards_data, get_top_transactions, cards_data_to_json, top_transactions_to_json, get_currency_rates, get_stock_prices
# from src.services import
# from src.reports import


# Инициализация пустой структуры JSON-объекта
json_answer_common_page = {
    "greeting": "",
    "cards": [],
    "top_transactions": [],
    "currency_rates": [],
    "stock_prices": []
}

# Инициализация пустых массивов с базовой структурой
json_answer_common_page["cards"] = [
    {"last_digits": "", "total_spent": 0.00, "cashback": 0.00}
]

json_answer_common_page["top_transactions"] = [
    {"date": "", "amount": 0.00, "category": "", "description": ""}
]

json_answer_common_page["currency_rates"] = [
    {"currency": "", "rate": 0.00}
]

json_answer_common_page["stock_prices"] = [
    {"stock": "", "price": 0.00}
]

# Считываем транзакции из файла xlsx в список
transactions_full = read_transactions_from_excel("data/operations.xlsx")
# Выводим первые N элементов
# for item in transactions_full[:150]:
#     print(item)

# print(f"transactions_full {len(transactions_full)} {type(transactions_full)}")

# Получаем список транзакций для заданного диапазона дат
transactions_filtered= get_transactions_filtered(transactions_full, Timestamp('14.11.2021 14:46:24'))
# 2021-12-31 16:44:00 - база
# 24.08.2021 03:39:33 и 14.11.2021 14:46:24 - проверка FAILED;

# for transaction in transactions_filtered:
#     print(transaction)

# print(f"transactions_full {len(transactions_full)} {type(transactions_full)}")
# print(f"transactions_filtered {len(transactions_filtered)} {type(transactions_filtered)}")


# GREETING
# Формируем приветствие в зависимости от текущего времени
current_datetime  = datetime.now()
greeting = get_greeting(current_datetime)
# print(greeting)
# Записываем приветствие (значение greeting) в итоговый список
# Очищаем существующий массив
json_answer_common_page["greeting"] = ""
# Добавляем элемент
json_answer_common_page["greeting"] = greeting
# print(json_answer_common_page)


# CARDS
# Формируем список транзакций по картам - по условиям
cards_list = get_cards_data(transactions_filtered)
# print(len(cards_list))
# print(cards_list)
# Записываем список транзакций по картам в итоговый список
cards_list_list_for_json = cards_data_to_json(cards_list)
# for card in cards_list_list_for_json:
#     print(f"cards_list_list_for_json = {card}")
# Очищаем существующий массив
json_answer_common_page["cards"].clear()
# Добавляем каждый элемент
for item in cards_list_list_for_json:
    json_answer_common_page["cards"].append(item)
# print(json_answer_common_page)


# TOP-5 TRANSACTIONS
# Формируем ТОП-список транзакций - по условиям
# top_transactions_list = get_top_transactions_test()
# for transaction in top_transactions_list:
#     print(transaction)
top_transactions_list = get_top_transactions(transactions_filtered)
# for transaction in top_transactions_list:
#     print(f"top_transactions_list = {transaction}")
# Записываем ТОП-список транзакций в итоговый список
top_transactions_list_for_json = top_transactions_to_json(top_transactions_list)
# for transaction in top_transactions_list_for_json:
#     print(f"top_transactions_list_for_json = {transaction}")
# Очищаем существующий массив
json_answer_common_page["top_transactions"].clear()
# Добавляем каждый элемент
for item in top_transactions_list_for_json:
    json_answer_common_page["top_transactions"].append(item)
# print(json_answer_common_page)


# USER_SETTINGS.JSON
# Открываем файл JSON и считываем из него данные в список
user_settings = read_user_settings_json("user_settings.json")
# print(f"user_settings = {user_settings}")


# CURRENCY_RATES
# Формируем список курсов валют
user_settings_currencies = user_settings["user_currencies"]
# print(f"user_settings_currency = {user_settings_currencies}")
# Записываем список курсов валют в итоговый список
# currency_rates_list = get_currency_rates(user_settings_currencies)
currency_rates_list = [{'currency': 'USD', 'rate': 79.12}, {'currency': 'EUR', 'rate': 92.05}]
# Очищаем существующий массив
json_answer_common_page["currency_rates"].clear()
# Добавляем каждый элемент
for item in currency_rates_list:
    json_answer_common_page["currency_rates"].append(item)
# print(json_answer_common_page)


# STOCK PRICES
# Формируем список цен акций
user_settings_stocks = user_settings["user_stocks"]
# print(f"user_settings_stocks = {user_settings_stocks}")
# Записываем список цен акций в итоговый список
# stock_prices_list = get_stock_prices(user_settings_stocks)
stock_prices_list = [{'stock': 'AAPL', 'price': 247.77}, {'stock': 'AMZN', 'price': 216.39}, {'stock': 'GOOGL', 'price': 245.45}, {'stock': 'MSFT', 'price': 513.57}, {'stock': 'TSLA', 'price': 429.24}]
# print(f"stock_prices_list = {stock_prices_list}")
# Очищаем существующий массив
json_answer_common_page["stock_prices"].clear()
# Добавляем каждый элемент
for item in stock_prices_list:
    json_answer_common_page["stock_prices"].append(item)
# print(json_answer_common_page)


# ФОРМИРУЕМ JSON-ОТВЕТ
# Преобразуем в JSON строку с форматированием
json_string = json.dumps(
    json_answer_common_page,
    ensure_ascii=False,
    indent=4
)
print("\nJSON-ОТВЕТ:")
print(json_string)
# # Сохраняем в файл
# with open('common_page_json_answer.json', 'w', encoding='utf-8') as file:
#     file.write(json_string)
