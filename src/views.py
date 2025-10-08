from datetime import datetime


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
def views_main_page(date_str: str = "2021-12-31 16:44:00"):
    """ """
    pass


def views_main_eventspage():
    """ """
    pass
