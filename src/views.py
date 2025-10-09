from datetime import datetime, timedelta
from typing import List, Dict


# Основные функции для генерации JSON-ответа


def get_greeting(date_str: str = "2021-12-31 16:44:00") -> str:
    """
    Определение приветствия по времени суток
    Принимает строку в формате 'YYYY-MM-DD HH:MM:SS'
    """
    try:
        # Парсим строку в объект datetime
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        hour = date.hour

        if 5 <= hour < 12:
            return "Доброе утро"
        elif 12 <= hour < 18:
            return "Добрый день"
        elif 18 <= hour < 23:
            return "Добрый вечер"
        else:
            return "Доброй ночи"

    except ValueError:
        return "Ошибка: неверный формат даты. Используйте формат 'YYYY-MM-DD HH:MM:SS'"


def card_last_digits():
    pass


def card_total_spent():
    pass


def card_cashback():
    pass


def top_transactions():
    pass


def currency_rates():
    pass


def stock_prices():
    pass




# ===================================================================================================================
def views_main_page(transactions_full: List[Dict], date_str: str = "2021-12-31 16:44:00")-> List[Dict]:
    """
    Основная функция для генерации JSON-ответов.
    Фильтрует транзакции по дате: от начала месяца до указанной даты.

    Параметры:
    date_str (str): строка с датой в формате "YYYY-MM-DD HH:MM:SS"
    transactions_full (List[Dict]): список всех транзакций

    Возвращает:
    List[Dict]: отфильтрованный список транзакций
    """
    # print(f"transactions_full = {len(transactions_full)}")

    # Преобразуем входную строку в объект datetime
    target_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    # print(f"target_datetime: {target_datetime} {type(target_datetime)}")

    # Получаем первый день месяца для указанной даты
    first_day_of_month = target_datetime.replace(day=1, hour=0, minute=0, second=0)
    # print(f"first_day_of_month: {first_day_of_month} {type(first_day_of_month)}")

    # Создаем пустой список для отфильтрованных транзакций
    filtered_transactions = []

    # Проходим по всем транзакциям
    for transaction in transactions_full:
        # try:

        # Парсим исходную дату транзакции и форматируем ее в нужный формат
        date_obj = datetime.strptime(transaction["transaction_date"], "%d.%m.%Y %H:%M:%S") # type data
        # print(f"date_obj: {date_obj} {type(date_obj)}")
        date_obj_1 = date_obj.strftime("%Y-%m-%d %H:%M:%S") # type str
        # print(f"date_obj_1: {date_obj_1} {type(date_obj_1)}")
        transaction_date = datetime.strptime(date_obj_1, "%Y-%m-%d %H:%M:%S") #type data
        # print(f"transaction_date: {transaction_date} {type(transaction_date)}")

        # print(f"first_day_of_month {first_day_of_month} <= transaction_date {transaction_date} <= target_datetime {target_datetime}")

        # Проверяем, попадает ли дата транзакции в нужный диапазон
        if (first_day_of_month <= transaction_date <= target_datetime):
            filtered_transactions.append(transaction)

        # except (KeyError, ValueError):
        #     # Пропускаем транзакции с некорректной датой
        #     continue

    return filtered_transactions


def views_main_eventspage():
    """ """
    pass
