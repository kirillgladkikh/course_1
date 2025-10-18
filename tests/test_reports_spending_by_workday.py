import pandas as pd
import datetime
from decimal import Decimal
from typing import List, Dict
from src.reports import spending_by_workday


# Тест 1: Только рабочие дни
def test_only_weekdays():
    # Создаем тестовые данные с правильными рабочими днями
    weekday_df = pd.DataFrame({
        'Дата операции': [
            '03.07.2023 12:00:00',  # Понедельник (в периоде)
            '04.07.2023 13:00:00'  # Вторник (в периоде)
        ],
        'Сумма платежа': [100, 200]
    })

    # Преобразуем даты
    weekday_df['Дата операции'] = pd.to_datetime(
        weekday_df['Дата операции'],
        format='%d.%m.%Y %H:%M:%S'
    )

    # Ожидаемый результат
    expected = pd.DataFrame({
        'Сумма платежа': {'Рабочий': 150.0, 'Выходной': 0.0}
    })

    # Указываем дату, которая охватывает все транзакции
    test_date = '2023-10-01'

    # Запускаем функцию
    result = spending_by_workday(weekday_df, date=test_date)

    # Приводим результат к float
    result = result.astype(float)

    # Проверяем период
    current_date = datetime.datetime.strptime(test_date, '%Y-%m-%d')
    start_date = current_date.replace(day=1) - pd.DateOffset(months=3)
    end_date = current_date

    # Проверяем даты транзакций
    assert all(weekday_df['Дата операции'] >= start_date)
    assert all(weekday_df['Дата операции'] <= end_date)

    # Проверяем, что все транзакции правильно определены как рабочие
    weekday_mask = weekday_df['Дата операции'].dt.dayofweek < 5
    assert weekday_mask.all(), "Не все транзакции определены как рабочие"

    # Проверяем количество транзакций
    assert len(weekday_df) == 2, "Неверное количество транзакций"

    # Сравниваем результаты
    assert result.equals(expected), (
        f"Тест не пройден!\n"
        f"Ожидалось:\n{expected}\n"
        f"Получено:\n{result}"
    )

    print("Тест только рабочих дней пройден!")


# Тест 2: Только выходные дни
def test_only_weekends():
    # Создаем тестовые данные с датами, которые точно попадут в период
    weekend_df = pd.DataFrame({
        'Дата операции': [
            '08.07.2023 12:00:00',  # Суббота (в периоде)
            '09.07.2023 13:00:00'  # Воскресенье (в периоде)
        ],
        'Сумма платежа': [150, 250]
    })

    # Преобразуем даты для проверки
    weekend_df['Дата операции'] = pd.to_datetime(
        weekend_df['Дата операции'],
        format='%d.%m.%Y %H:%M:%S'
    )

    # Рассчитываем ожидаемые средние значения:
    # (150 + 250) / 2 = 200.0

    expected = pd.DataFrame({
        'Сумма платежа': {'Рабочий': 0.0, 'Выходной': 200.0}
    })

    # Указываем дату, которая охватывает все транзакции
    test_date = '2023-10-01'

    # Запускаем функцию
    result = spending_by_workday(weekend_df, date=test_date)

    # Приводим результат к float для корректного сравнения
    result = result.astype(float)

    # Проверяем, что все даты попадают в период
    current_date = datetime.datetime.strptime(test_date, '%Y-%m-%d')
    start_date = current_date.replace(day=1) - pd.DateOffset(months=3)
    end_date = current_date

    # Добавляем проверку дат
    assert all(weekend_df['Дата операции'] >= start_date), "Транзакции не попадают в период"
    assert all(weekend_df['Дата операции'] <= end_date), "Транзакции не попадают в период"

    # Сравниваем результаты
    assert result.equals(expected), (
        f"Тест не пройден!\n"
        f"Ожидалось:\n{expected}\n"
        f"Получено:\n{result}"
    )

    print("Тест только выходных дней пройден!")


# Тест 3: Смешанные дни
def test_mixed_days():
    # Создаем тестовые данные с датами, которые точно попадут в период
    mixed_df = pd.DataFrame({
        'Дата операции': [
            '03.07.2023 12:00:00',  # Понедельник (в периоде)
            '08.07.2023 13:00:00',  # Суббота (в периоде)
            '10.07.2023 14:00:00'  # Понедельник (в периоде)
        ],
        'Сумма платежа': [100, 200, 300]
    })

    # Преобразуем даты для проверки
    mixed_df['Дата операции'] = pd.to_datetime(
        mixed_df['Дата операции'],
        format='%d.%m.%Y %H:%M:%S'
    )

    # Рассчитываем ожидаемые средние значения:
    # Рабочие дни: (100 + 300) / 2 = 200.0
    # Выходные дни: 200.0

    # Создаем ожидаемый результат
    expected = pd.DataFrame({
        'Сумма платежа': {'Рабочий': 200.0, 'Выходной': 200.0}
    })

    # Указываем дату, которая охватывает все транзакции
    test_date = '2023-10-01'

    # Запускаем функцию
    result = spending_by_workday(mixed_df, date=test_date)

    # Приводим результат к float для корректного сравнения
    result = result.astype(float)

    # Проверяем, что все даты попадают в период
    current_date = datetime.datetime.strptime(test_date, '%Y-%m-%d')
    start_date = current_date.replace(day=1) - pd.DateOffset(months=3)
    end_date = current_date

    # Добавляем проверку дат
    assert all(mixed_df['Дата операции'] >= start_date), "Транзакции не попадают в период"
    assert all(mixed_df['Дата операции'] <= end_date), "Транзакции не попадают в период"

    # Сравниваем результаты
    assert result.equals(expected), (
        f"Тест не пройден!\n"
        f"Ожидалось:\n{expected}\n"
        f"Получено:\n{result}"
    )

    print("Тест смешанных дней пройден!")


# Тест 4: Пустые данные
def test_empty_data():
    empty_df = pd.DataFrame(columns=['Дата операции', 'Сумма платежа'])

    expected = pd.DataFrame({
        'Сумма платежа': {'Рабочий': 0.0, 'Выходной': 0.0}
    })

    result = spending_by_workday(empty_df, "2021-12-31")

    assert result.equals(expected), f"Тест не пройден!\nОжидалось:\n{expected}\nПолучено:\n{result}"
    print("Тест пустых данных пройден!")