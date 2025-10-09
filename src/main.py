import os
import json
from src.views import views_main_page, get_greeting
# from src.services import
# from src.reports import
from src.utils import read_transactions_from_excel, convert_date_format


# print(convert_date_format())
#
# print(get_greeting())



transactions_full = read_transactions_from_excel("data/operations.xlsx")
transactions_filtered= views_main_page(transactions_full, "2021-12-31 16:44:00")
print(f"transactions_filtered {len(transactions_filtered)}")


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
