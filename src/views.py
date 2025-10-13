import math
from datetime import datetime, timedelta
from typing import List, Dict, Union
from pandas import Timestamp


# Основные функции для генерации JSON-ответа

def get_greeting(date: datetime) -> str:
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

    filtered_transactions = []

    for transaction in transactions_full:

        try:
            # Получаем дату транзакции
            date_obj = transaction["transaction_date"]

            # Проверяем тип date_obj
            if not isinstance(date_obj, Timestamp):
                raise ValueError("transaction_date не является Timestamp")

            # print(f"\nfirst_day_of_month {first_day_of_month} <= date_obj {date_obj} <= target_datetime {target_datetime}")

            # Проверяем, попадает ли дата транзакции в нужный диапазон
            if first_day_of_month <= date_obj <= target_datetime:

                # print(f"transaction in transactions_full {transaction}")

                filtered_transactions.append(transaction)

                # print(f"transaction in filtered_transactions {filtered_transactions[-1]}")

        except (KeyError, ValueError) as e:
            print(f"Ошибка при обработке транзакции: {e}")
            continue

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
