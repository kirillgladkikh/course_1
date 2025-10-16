# Реализуйте отчеты в отдельном модуле reports.py
import os
import json
import logging
import datetime
from typing import Callable, Any, Optional
import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def report_saver(filename: Optional[str] = None):
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            # Используем переменную filename из внешнего окружения (из функции decorator),
            # а не создаем новую локальную переменную
            nonlocal filename

            # Получаем результат выполнения функции
            result = func(*args, **kwargs)

            # Формируем имя файла, если не передано
            if filename is None:
                func_name = func.__name__
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{func_name}_{timestamp}.json"

            try:
                # Сохраняем результат в JSON
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(result.to_dict(), f, ensure_ascii=False, indent=4)
                logging.info(f"Отчет успешно сохранен в файл {filename}")
            except Exception as e:
                logging.error(f"Ошибка при сохранении отчета: {str(e)}")

            return result

        return wrapper

    return decorator


# Использование декоратора
@report_saver()  # Без параметра - используем имя по умолчанию
def spending_by_workday(transactions: pd.DataFrame,
                        date: Optional[str] = None) -> pd.DataFrame:
    """
    Анализирует средние траты по рабочим и выходным дням за последние 3 месяца.

    Параметры:
    transactions (pd.DataFrame): DataFrame с транзакциями, содержащий колонки:
        - 'Дата операции' (формат 'DD.MM.YYYY HH:MM:SS')
        - 'Сумма платежа' (числовой тип)
    date (Optional[str]): Опциональная дата в формате 'YYYY-MM-DD' для расчета периода.
        Если не указана, используется текущая дата.

    Возвращает:
    pd.DataFrame: DataFrame с двумя строками:
        - 'Рабочий' - средняя сумма трат в рабочие дни
        - 'Выходной' - средняя сумма трат в выходные дни

    Алгоритм работы:
    1. Преобразует даты транзакций в формат datetime
    2. Определяет период анализа (последние 3 месяца от указанной или текущей даты)
    3. Фильтрует транзакции по выбранному периоду
    4. Разделяет дни на рабочие и выходные
    5. Вычисляет средние значения трат для каждой категории
    """
    # Преобразуем колонку с датами в формат datetime
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')

    # Получаем текущую дату, если не передана
    if date is None:
        current_date = datetime.datetime.now()
    else:
        current_date = datetime.datetime.strptime(date, '%Y-%m-%d')

    # Определяем диапазон дат (последние 3 месяца)
    start_date = current_date.replace(day=1) - pd.DateOffset(months=3)
    end_date = current_date

    # # Выводим отладочную информацию
    # print(f"current_date = {current_date}")
    # print(f"start_date = {start_date}")
    # print(f"end_date = {end_date}")

    # Фильтруем транзакции по дате
    filtered_df = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date)
        ]
    # # Выводим отладочную информацию
    # print(filtered_df)

    # Добавляем колонку с определением выходных
    filtered_df = filtered_df.assign(
        is_weekend=filtered_df['Дата операции'].dt.dayofweek >= 5
    )

    # Добавляем колонку с названием дня недели для наглядности
    filtered_df['День недели'] = filtered_df['Дата операции'].dt.day_name()

    # # Выводим отладочную информацию
    # print(filtered_df)

    # Группируем по типу дня и считаем средние траты
    result = filtered_df.groupby('is_weekend').agg({
        'Сумма платежа': 'mean'
    }).rename(index={True: 'Выходной', False: 'Рабочий'})

    return result


# Получаем путь к корню проекта
file_path = "data/operations.xlsx"
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Формируем полный путь
full_path = os.path.join(project_root, file_path)

df = pd.read_excel(full_path)

# # Выводим отладочную информацию
# print(f"full_path = {full_path}")
# print("Входной DataFrame:")
# print(df)

# Задаём дату присутствующую в XLS-файле
input_data = "2021-12-31"

result = spending_by_workday(df, input_data)

print(f"\nДата начала периода отчета (переданная дата): {input_data}")
print("Группируем по типу дня и считаем средние траты...")
print("Выводим средние траты в рабочий и в выходной день за последние три месяца (от переданной даты):")
print(result)
