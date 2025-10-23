# Реализуйте отчеты в отдельном модуле reports.py
import os
import json
import logging
from config import setup_logger
import datetime
from typing import Callable, Any, Optional
import pandas as pd


# Настройки логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def report_saver(filename: Optional[str] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal filename
            result = func(*args, **kwargs)
            if filename is None:
                func_name = func.__name__
                filename = f"{func_name}.json"
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(result.to_dict(), f, ensure_ascii=False, indent=4)
                logging.info(f"Отчет успешно сохранен в файл {filename}")
            except Exception as e:
                logging.error(f"Ошибка при сохранении отчета: {str(e)}")
            return result
        return wrapper
    return decorator

# Создаем логгер один раз для всего модуля
setup_logger()
logger = logging.getLogger(__name__)  # __name__ автоматически содержит имя модуля

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
    """
    # Преобразуем даты в нужный формат
    transactions['Дата операции'] = pd.to_datetime(
        transactions['Дата операции'],
        format='%d.%m.%Y %H:%M:%S'
    )

    # Определяем текущую дату
    if date is None:
        current_date = datetime.datetime.now()
    else:
        current_date = datetime.datetime.strptime(date, '%Y-%m-%d')

    # Рассчитываем период анализа
    start_date = current_date.replace(day=1) - pd.DateOffset(months=3)
    end_date = current_date

    # Фильтруем транзакции по периоду
    filtered_df = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date)
        ].copy()

    # Разделяем транзакции на рабочие и выходные дни
    work_days = filtered_df[
        filtered_df['Дата операции'].dt.dayofweek < 5
        ]

    weekend_days = filtered_df[
        filtered_df['Дата операции'].dt.dayofweek >= 5
        ]

    # Считаем средние значения отдельно для каждой категории
    avg_work = work_days['Сумма платежа'].mean() if not work_days.empty else 0
    avg_weekend = weekend_days['Сумма платежа'].mean() if not weekend_days.empty else 0

    # Формируем итоговый результат с явным приведением к float
    result = pd.DataFrame({
        'Сумма платежа': {
            'Рабочий': avg_work,
            'Выходной': avg_weekend
        }
    }).astype(float)

    return result



def reports_page() -> None:
    """
    Генерирует отчёт о средних тратах в рабочие и выходные дни за последние три месяца
    относительно заданной даты на основе данных из Excel-файла.

    Функция выполняет следующие действия:
    1. Определяет путь к файлу data/operations.xlsx в корне проекта.
    2. Загружает данные из Excel-файла в DataFrame.
    3. Задаёт фиксированную дату начала отчётного периода (2021-12-31).
    4. Вызывает функцию spending_by_workday для расчёта средних трат
       по типу дня (рабочий/выходной) за последние три месяца от заданной даты.
    5. Логирует входные данные и результаты расчёта.

    Параметры:
        Не принимает явных параметров. Путь к файлу и дата начала периода
        задаются внутри функции.

    Возвращаемое значение:
        None. Результаты выводятся через логирование (logger.info).

    Используемые внешние зависимости:
        - os: для формирования пути к файлу.
        - pandas as pd: для загрузки и обработки данных из Excel.
        - logger: для вывода отладочной и информационной информации.
        - spending_by_workday: функция для расчёта средних трат по типу дня.

    Пример логируемого вывода:
        INFO: Дата начала периода отчета (переданная дата): 2021-12-31
        INFO: Группируем по типу дня и считаем средние траты...
        INFO: Выводим средние траты в рабочий и в выходной день за последние три месяца (от переданной даты):
        INFO:
                   day_type  average_spending
                0  workday           1500.50
                1  weekend           2300.75
    """
    # Получаем путь к корню проекта
    file_path = "data/operations.xlsx"
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # Формируем полный путь
    full_path = os.path.join(project_root, file_path)

    df = pd.read_excel(full_path)

    # # Выводим отладочную информацию
    logger.debug(f"full_path = {full_path}")
    logger.debug("Входной DataFrame:")
    logger.debug(df)
    # print(f"full_path = {full_path}")
    # print("Входной DataFrame:")
    # print(df)

    # Задаём дату присутствующую в XLS-файле
    input_data = "2021-12-31"

    result = spending_by_workday(df, input_data)

    logger.info(f"Дата начала периода отчета (переданная дата): {input_data}")
    logger.info("Группируем по типу дня и считаем средние траты...")
    logger.info("Выводим средние траты в рабочий и в выходной день за последние три месяца (от переданной даты):")
    logger.info(f"\n{result}")
    # print(f"\nДата начала периода отчета (переданная дата): {input_data}")
    # print("Группируем по типу дня и считаем средние траты...")
    # print("Выводим средние траты в рабочий и в выходной день за последние три месяца (от переданной даты):")
    # print(result)

    return
