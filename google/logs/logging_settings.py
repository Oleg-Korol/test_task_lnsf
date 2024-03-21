import logging


def setup_logging():
    # Проверяем, что логгер еще не создан
    if not logging.getLogger().handlers:
        # Создаем объект логгера
        logger = logging.getLogger()

        # Устанавливаем уровень логирования (в данном случае INFO)
        logger.setLevel(logging.INFO)

        # Создаем форматтер
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler_warning = logging.FileHandler("logs/log.txt")
        file_handler_warning.setFormatter(formatter)
        file_handler_warning.setLevel(logging.WARNING)
        logger.addHandler(file_handler_warning)

        # Создаем обработчик для вывода в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)





