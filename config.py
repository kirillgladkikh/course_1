import logging


def setup_logger() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Очищаем существующие обработчики
    logger.handlers.clear()  # Добавляем эту строку

    # Создаем форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Создаем FileHandler с режимом перезаписи + добавляем форматтер к обработчику
    file_handler = logging.FileHandler('course_1.log', mode='w')
    file_handler.setFormatter(formatter)

    # Создаем StreamHandler для вывода в консоль + добавляем форматтер к обработчику
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)