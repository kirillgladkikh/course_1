import os
import json
from src.views import views_main_page, get_greeting, get_current_time
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
    {"last_digits": "", "total_spent": 0.0, "cashback": 0.0}
]

json_answer_common_page["top_transactions"] = [
    {"date": "", "amount": 0.0, "category": "", "description": ""}
]

json_answer_common_page["currency_rates"] = [
    {"currency": "", "rate": 0.0}
]

json_answer_common_page["stock_prices"] = [
    {"stock": "", "price": 0.0}
]

# Считываем транзакции из файла xlsx в список
transactions_full = read_transactions_from_excel("data/operations.xlsx")

# Получаем список транзакций для заданного диапазона дат
transactions_filtered= views_main_page(transactions_full, "2021-12-31 16:44:00")
# print(f"transactions_filtered {len(transactions_filtered)}")

# Формируем приветствие в зависимости от текущего времени
local_time = get_current_time()
greeting = get_greeting(local_time)
# print(greeting)

# Записываем приветствие (значение greeting) в итоговый список
json_answer_common_page["greeting"] = greeting
# print(json_answer_common_page)

# Формируем список транзакций по картам - по условиям

# Записываем список транзакций по картам в итоговый список

# Формируем ТОП-список транзакций - по условиям

# Записываем ТОП-список транзакций в итоговый список

# Формируем список курсов валют

# Записываем список курсов валют в итоговый список

# Формируем список цен акций

# Записываем список цен акций в итоговый список

# Формируем полный JSON-ответ из итогового списка




# # Преобразуем в JSON строку
# json_data = json.dumps(transactions, ensure_ascii=False, indent=4)
#
# # Сохраняем в файл
# with open('transactions.json', 'w', encoding='utf-8') as file:
#     file.write(json_data)




def services_main():
    pass


def reports_main():
    pass


# ==============================================================================================================
def course_1_main():
    pass
