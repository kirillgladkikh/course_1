import logging


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Создаем форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Создаем FileHandler с режимом перезаписи
    file_handler = logging.FileHandler('course_1.log', mode='w')
    file_handler.setFormatter(formatter)

    # Создаем StreamHandler для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)