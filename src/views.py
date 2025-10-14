import math
import heapq
from datetime import datetime, timedelta
from typing import List, Dict, Union
from pandas import Timestamp
from decimal import Decimal


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

        # Игнорируем строки без данных карт
        # print(f'transaction["card_number"]: {transaction["card_number"]} {type(transaction["card_number"])}')
        if transaction["card_number"] != "":

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

                # # Фильтруем nan
                # transaction_amount = (
                #     Decimal('0.00')
                #     if math.isnan(Decimal(str(transaction["transaction_amount"])))
                #     else Decimal(str(transaction["transaction_amount"]))
                # )
                #
                # # Фильтруем nan
                # cashback_amount = (
                #     Decimal('0.00')
                #     if math.isnan(Decimal(str(transaction["cashback_amount"])))
                #     else Decimal(str(transaction["cashback_amount"]))
                # )

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


def top_transactions_to_json(top_transactions: List[Dict]) -> List[Dict]:
    """
    Преобразует список транзакций в сокращенный формат с основными полями

    Args:
        transactions: список транзакций в исходной структуре

    Returns:
        список сокращенных транзакций с основными полями
    """
    result = []

    for transaction in top_transactions:
        # Создаем новый словарь с нужными полями
        top_transaction = {
            "date": transaction["transaction_date"],  #.strftime('%Y-%m-%d') if transaction["transaction_date"] else "",
            "amount": transaction["transaction_amount"],
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





    # Создаем словарь для хранения результатов по топ-транзакциям
    result = {}



  # "top_transactions": [
  #   {
  #     "date": "21.12.2021",
  #     "amount": 1198.23,
  #     "category": "Переводы",
  #     "description": "Перевод Кредитная карта. ТП 10.2 RUR"
  #   },
  #   {
  #     "date": "20.12.2021",
  #     "amount": 829.00,
  #     "category": "Супермаркеты",
  #     "description": "Лента"
  #   },
  #   {
  #     "date": "20.12.2021",
  #     "amount": 421.00,
  #     "category": "Различные товары",
  #     "description": "Ozon.ru"
  #   },
  #   {
  #     "date": "16.12.2021",
  #     "amount": -14216.42,
  #     "category": "ЖКХ",
  #     "description": "ЖКУ Квартира"
  #   },
  #   {
  #     "date": "16.12.2021",
  #     "amount": 453.00,
  #     "category": "Бонусы",
  #     "description": "Кешбэк за обычные покупки"
  #   }
  # ],
  #
















def views_main_eventspage():
    """ """
    pass
