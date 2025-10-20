
import logging
from config import setup_logger
from src.views import views_page
from src.services import services_page
from src.reports import reports_page

# Создаем логгер
setup_logger()
logger = logging.getLogger(__name__)

# ЗАПУСК views.py
logger.info(f"ЗАПУСК views.py")
views_page()

# ЗАПУСК services.py
logger.info(f"ЗАПУСК services.py")
services_page()

# ЗАПУСК reports.py
logger.info(f"ЗАПУСК reports.py")
reports_page()


