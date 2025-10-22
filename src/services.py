# Реализуйте сервисы в отдельном модуле services.py
import pandas as pd
import logging

from pandas.io.formats.format import return_docstring

from config import setup_logger
from decimal import Decimal
from typing import List, Dict
from datetime import datetime
from src.utils import read_transactions_from_excel

# Создаем логгер один раз для всего модуля
setup_logger()  # ======================================================================================================
logger = logging.getLogger(__name__)  # __name__ автоматически содержит имя модуля


def investment_bank(
        transactions: List[Dict],  # список транзакций
        month: str,  # месяц в формате 'YYYY-MM'
        limit: Decimal  # порог округления (10, 50 или 100) как Decimal
) -> Decimal:
    """
    Рассчитывает сумму накоплений в инвесткопилке за указанный месяц путем округления сумм транзакций до заданного порога.

    Функция фильтрует транзакции по указанному месяцу, округляет сумму каждой транзакции вверх до ближайшего значения,
    кратного заданному порогу, и вычисляет разницу между округленной и фактической суммой. Все разницы суммируются
    для получения итоговой суммы накоплений.

    :param transactions: список транзакций, где каждая транзакция представлена в виде словаря с полями:
        - transaction_date: дата транзакции (Timestamp)
        - payment_amount: сумма платежа (Decimal)
    :param month: строка, содержащая месяц в формате 'YYYY-MM', за который производится расчет
    :param limit: порог округления сумм транзакций (Decimal, допустимые значения: 10, 50, 100)
    :return: общая сумма накоплений за указанный месяц, округленная до двух знаков после запятой (Decimal)
    """
    # Фильтрация транзакций по месяцу
    filtered_transactions = []

    for transaction in transactions:
        try:
            # Получаем дату транзакции
            transaction_date = transaction['transaction_date']

            # Преобразуем Timestamp в datetime
            datetime_obj = transaction_date.to_pydatetime()

            # Форматируем дату в нужный формат
            formatted_date = datetime_obj.strftime('%Y-%m')

            # # Выводим отладочную информацию
            # logger.debug(f"Исходная дата: {transaction_date}")
            # logger.debug(f"Преобразованная дата: {datetime_obj}")
            # logger.debug(f"Форматированная дата: {formatted_date}")
            # logger.debug(f"Целевой месяц: {month}")
            # logger.debug("-" * 40)

            # Сравниваем с целевым месяцем
            if formatted_date == month:
                filtered_transactions.append(transaction)

        except Exception as e:
            logger.error(f"Ошибка обработки транзакции {transaction}: {str(e)}")
            # print(f"Ошибка обработки транзакции {transaction}: {str(e)}")

    # Функция округления суммы
    def round_to_limit(amount: Decimal, limit: Decimal) -> Decimal:
        """
        Округляет число до ближайшего большего значения, кратного заданному лимиту.

        Функция проверяет, кратно ли входное значение `amount` заданному лимиту `limit`.
        Если кратно — возвращает исходное значение.
        Если не кратно — округляет вверх до ближайшего значения, кратного `limit`.

        Параметры:
        -----------
        amount : Decimal
            Исходное число, которое требуется округлить.
        limit : Decimal
            Лимит (шаг округления) — значение, к которому должно быть кратно итоговое число.

        Возвращает:
        ------------
        Decimal
            Если `amount` кратно `limit` — возвращается `amount`.
            Иначе — ближайшее большее число, кратное `limit`.
        """
        # Проверяем кратность
        if amount % limit == 0:
            return amount
        # Иначе округляем вверх
        return ((amount // limit) + Decimal('1')) * limit

    # Расчет разницы между округленной и реальной суммой
    def calculate_difference(transaction: Dict, limit: Decimal) -> Decimal:
        amount = transaction['payment_amount']  # amount type Decimal
        rounded_amount = round_to_limit(amount, limit)
        return rounded_amount - amount

    # Применение функционального подхода
    differences = map(lambda t: calculate_difference(t, limit), filtered_transactions)

    # Суммирование с начальным значением Decimal
    total_amount = sum(differences, start=Decimal('0.00'))

    return total_amount.quantize(Decimal('0.00'))


def services_page():
    """
    Формирует данные для страницы сервисов (в частности, расчёт суммы в «Инвесткопилке»).

    Функция выполняет следующие действия:
    1. Считывает полные данные о транзакциях из Excel‑файла `data/operations.xlsx`
       с помощью функции `read_transactions_from_excel()`.
    2. Задаёт параметры для расчёта «Инвесткопилки»:
       - `coin_limit` — максимальный размер отчисления за операцию (в рублях);
       - `coin_month` — целевой месяц для расчёта (в формате 'ГГГГ‑ММ').
    3. Преобразует лимит отчислений в тип `Decimal` для точной арифметики.
    4. Вызывает функцию `investment_bank()` для расчёта суммы в «Инвесткопилке»
       на основе транзакций, целевого месяца и лимита.
    5. Логирует результат расчёта (сумма в «Инвесткопилке» с указанием лимита и периода).

    Параметры расчёта:
    - coin_limit (int): максимальный размер отчисления за одну транзакцию (по умолчанию 50 руб.).
    - coin_month (str): месяц и год для расчёта в формате 'ГГГГ‑ММ' (по умолчанию '2021‑12').

    Используемые функции:
    - read_transactions_from_excel(filepath: str) -> list:
      считывает транзакции из Excel‑файла и возвращает список словарей.
    - investment_bank(
        transactions: list,
        month: str,
        limit: Decimal
      ) -> Decimal:
      рассчитывает сумму в «Инвесткопилке» на основе транзакций, месяца и лимита отчисления.

    Логирование:
    - Используется `logger.info()` для вывода итога: суммы в «Инвесткопилке»,
      заданного лимита и периода расчёта.

    Возвращаемое значение:
    None: функция не возвращает явного значения (результат выводится через логирование).

    Пример вывода лога:
    Сумма в инвесткопилке (лимит: 50 руб., период: 2021‑12): 54.00 руб.
    """
    # Считываем транзакции из файла xlsx в список
    transactions_full = read_transactions_from_excel("data/operations.xlsx")
    # # Создаем тестовые данные
    # transactions_full = [
    #     {
    #         "transaction_date": pd.Timestamp('2021-12-01 18:12:17'),
    #         "payment_amount": Decimal('1712.00')
    #     },
    #     {
    #         "transaction_date": pd.Timestamp('2021-12-05 18:12:17'),
    #         "payment_amount": Decimal('345.00')
    #     },
    #     {
    #         "transaction_date": pd.Timestamp('2021-12-10 18:12:17'),
    #         "payment_amount": Decimal('89.00')
    #     }
    # ]

    # Исходные данные для расчета Инвесткопилки
    coin_limit = 50
    coin_month = '2021-12'
    # Преобразуем лимит в Decimal для использования в функции
    coin_limit_decimal = Decimal(str(coin_limit))

    result = investment_bank(transactions_full, coin_month, coin_limit_decimal)
    logger.info(f"\nСумма в инвесткопилке (лимит: {coin_limit} руб., период: {coin_month}): {result} руб.")  # Вывод для тестовых данных: ₽ 54.00
    # print(f"\nСумма в инвесткопилке (лимит: ₽ {coin_limit}, период: {coin_month}): ₽ {result}")  # Вывод для тестовых данных: ₽ 54.00

    return