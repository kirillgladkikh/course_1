import os
import json
from pandas import Timestamp
from decimal import Decimal
from src.views import get_transactions_filtered, get_greeting, get_current_time, get_cards_data
# from src.services import
# from src.reports import
from src.utils import read_transactions_from_excel, convert_date_format


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
    {"last_digits": "", "total_spent": Decimal('0.00'), "cashback": Decimal('0.00')} # Инициализация с Decimal
]

json_answer_common_page["top_transactions"] = [
    {"date": "", "amount": Decimal('0.00'), "category": "", "description": ""} # Инициализация с Decimal
]

json_answer_common_page["currency_rates"] = [
    {"currency": "", "rate": Decimal('0.00')} # Инициализация с Decimal
]

json_answer_common_page["stock_prices"] = [
    {"stock": "", "price": Decimal('0.00')} # Инициализация с Decimal
]

# Считываем транзакции из файла xlsx в список
transactions_full = read_transactions_from_excel("data/operations.xlsx")
# Выводим первые N элементов
for item in transactions_full[:150]:
    print(item)

print(f"transactions_full {len(transactions_full)} {type(transactions_full)}")

# Получаем список транзакций для заданного диапазона дат
transactions_filtered= get_transactions_filtered(transactions_full, Timestamp('2021-12-31 16:44:00'))
# for transaction in transactions_filtered:
#     print(transactions_filtered)

print(f"transactions_full {len(transactions_full)} {type(transactions_full)}")
print(f"transactions_filtered {len(transactions_filtered)} {type(transactions_filtered)}")
#
# # Формируем приветствие в зависимости от текущего времени
# local_time = get_current_time()
# greeting = get_greeting(local_time)
# # print(greeting)
#
# # Записываем приветствие (значение greeting) в итоговый список
#
# # Очищаем существующий массив
# json_answer_common_page["greeting"].clear()
#
# # Добавляем элемент
# json_answer_common_page["greeting"] = greeting
# # print(json_answer_common_page)
#
# # Формируем список транзакций по картам - по условиям
# cards_list = get_cards_data(transactions_filtered)
# print(len(cards_list))
# print(cards_list)
#
# # Записываем список транзакций по картам в итоговый список
#
# # Очищаем существующий массив
# json_answer_common_page["cards"].clear()
#
# # Добавляем каждый элемент
# for card in cards_list:
#     json_answer_common_page["cards"].append(card)
# print(json_answer_common_page)
#
# # Формируем ТОП-список транзакций - по условиям
#
# # Записываем ТОП-список транзакций в итоговый список
#
# # Формируем список курсов валют
#
# # Записываем список курсов валют в итоговый список
#
# # Формируем список цен акций
#
# # Записываем список цен акций в итоговый список
#
# # Формируем полный JSON-ответ из итогового списка
#
#
#
#
# # # Преобразуем в JSON строку
# # json_data = json.dumps(transactions, ensure_ascii=False, indent=4)
# #
# # # Сохраняем в файл
# # with open('transactions.json', 'w', encoding='utf-8') as file:
# #     file.write(json_data)
#
#
#
#
# def services_main():
#     pass
#
#
# def reports_main():
#     pass
#
#
# # ==============================================================================================================
# def course_1_main():
#     pass
