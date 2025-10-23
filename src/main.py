import logging
from config import setup_logger
from pandas import Timestamp
from src.views import views_page
from src.services import services_page
from src.reports import reports_page

# Создаем логгер
setup_logger()
logger = logging.getLogger(__name__)

# Устанавливаем дату для фильтрации
input_data = Timestamp('2021-12-31 16:44:00')

# ЗАПУСК views.py
logger.info(f"ЗАПУСК views.py")
views_page_json = views_page(input_data)
# print(views_page_json)

# ЗАПУСК services.py
logger.info(f"ЗАПУСК services.py")
services_page_json = services_page(input_data)
# print(services_page_json)

# ЗАПУСК reports.py
logger.info(f"ЗАПУСК reports.py")
reports_page_json = reports_page(input_data)
# print(reports_page_json)


