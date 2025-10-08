import os
import json
# from src.views import
# from src.services import
# from src.reports import
from src.utils import read_transactions_from_excel, convert_date_format


print(convert_date_format())


transactions = read_transactions_from_excel("data/operations.xlsx")

# # Преобразуем в JSON строку
# json_data = json.dumps(transactions, ensure_ascii=False, indent=4)
#
# # Сохраняем в файл
# with open('transactions.json', 'w', encoding='utf-8') as file:
#     file.write(json_data)


def views_main():
    pass


def services_main():
    pass


def reports_main():
    pass
