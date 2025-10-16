# Реализуйте сервисы в отдельном модуле services.py
import pandas as pd
from decimal import Decimal
from typing import List, Dict
from datetime import datetime
from utils import read_transactions_from_excel


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

    Пример использования:
    >>> transactions = [
    ...     {'transaction_date': Timestamp('2023-10-01 12:00:00'), 'payment_amount': Decimal('123.45')},
    ...     {'transaction_date': Timestamp('2023-10-15 15:30:00'), 'payment_amount': Decimal('78.90')}
    ... ]
    >>> investment_bank(transactions, '2023-10', Decimal('100'))
    Decimal('137.65')
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
            # print(f"Исходная дата: {transaction_date}")
            # print(f"Преобразованная дата: {datetime_obj}")
            # print(f"Форматированная дата: {formatted_date}")
            # print(f"Целевой месяц: {month}")
            # print("-" * 40)

            # Сравниваем с целевым месяцем
            if formatted_date == month:
                filtered_transactions.append(transaction)

        except Exception as e:
            print(f"Ошибка обработки транзакции {transaction}: {str(e)}")

    # Функция округления суммы
    def round_to_limit(amount: Decimal) -> Decimal:
        return ((amount // limit) + Decimal('1')) * limit

    # Расчет разницы между округленной и реальной суммой
    def calculate_difference(transaction: Dict) -> Decimal:
        amount = transaction['payment_amount']  # amount type Decimal
        rounded_amount = round_to_limit(amount)
        return rounded_amount - amount

    # Применение функционального подхода
    differences = map(calculate_difference, filtered_transactions)

    # Суммирование с начальным значением Decimal
    total_amount = sum(differences, start=Decimal('0.00'))

    return total_amount.quantize(Decimal('0.00'))


# Пример использования
if __name__ == "__main__":
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
    print(f"Сумма в инвесткопилке (лимит: ₽ {coin_limit}, период: {coin_month}): ₽ {result}")  # Вывод: ₽ 54.00