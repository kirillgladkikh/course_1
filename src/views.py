import math
from datetime import datetime, timedelta
from typing import List, Dict


# Основные функции для генерации JSON-ответа
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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


def card_to_json(transactions_filtered: List[Dict], date_str: str = "2021-12-31 16:44:00"):
    """ """
    return


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
def get_transactions_filtered(transactions_full: List[Dict], date_str: str = "2021-12-31 16:44:00")-> List[Dict]:
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


def get_cards_data(transactions_filtered: list) -> list:
    """
    Анализирует список транзакций и агрегирует данные по банковским картам.

    Функция обрабатывает список транзакций, группируя их по последним 4 цифрам
    номера карты. Для каждой карты подсчитывается общая сумма потраченных средств
    и накопленный кешбэк.

    Параметры:
    transactions_filtered (list): список словарей с данными транзакций, где каждый
        словарь содержит следующие ключи:
        - card_number: номер карты (может быть строкой или числом)
        - transaction_amount: сумма транзакции (число или строка с числом)
        - cashback_amount: сумма кешбэка (число или строка с числом)

    Возвращает:
    list: список словарей с агрегированными данными по картам, где каждый словарь
        содержит:
        - last_digits: последние 4 цифры номера карты
        - total_spent: общая сумма потраченных средств
        - cashback: накопленный кешбэк

    Особые случаи:
    - Транзакции без номера карты игнорируются
    - При ошибках преобразования числовых значений транзакция пропускается
    - Номера карт обрабатываются как строки для корректной работы с ведущими нулями
    """
    # Создаем словарь для хранения результатов по картам
    result = {}

    # Проходим по всем транзакциям
    for transaction in transactions_filtered:

        # Игнорируем строки без данных карт
        # print(f'transaction["card_number"]: {transaction["card_number"]} {type(transaction["card_number"])}')
        if type(transaction["card_number"]) != float:

            # Извлекаем последние 4 цифры карты
            # print(f'transaction["card_number"]: {transaction["card_number"]} {type(transaction["card_number"])}')
            card_number = str(transaction["card_number"])
            last_digits = card_number[-4:]  # Берем последние 4 символа

            # Получаем сумму транзакции и кешбэк
            try:
                # Преобразуем строки в числа, если они хранятся как строки
                # transaction_amount = float(transaction["transaction_amount"])

                # Фильтруем nan
                transaction_amount = (
                    0.0
                    if math.isnan(float(transaction["transaction_amount"]))
                    else float(transaction["transaction_amount"])
                )

                # Фильтруем nan
                cashback_amount = (
                    0.0
                    if math.isnan(float(transaction["cashback_amount"]))
                    else float(transaction["cashback_amount"])
                )

                print(
                    f'transaction["cashback_amount"]: {transaction["cashback_amount"]} {type(transaction["cashback_amount"])}')
                print(f'cashback_amount: {cashback_amount} {type(cashback_amount)}')

            except ValueError:
                print(f"Ошибка преобразования данных для карты {last_digits}")
                continue

            # Если карта еще не в результатах, добавляем её
            if last_digits not in result:
                result[last_digits] = {
                    "last_digits": last_digits,
                    "total_spent": 0.0,
                    "cashback": 0.0
                }

            # Накапливаем суммы
            result[last_digits]["total_spent"] += transaction_amount
            result[last_digits]["cashback"] += cashback_amount

        else:
            print(f"строка {transaction} не содержит данных карты")



    # Преобразуем словарь в список
    return list(result.values())


def views_main_eventspage():
    """ """
    pass
