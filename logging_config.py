import logging

def setup_logger(log_file="app.log"):
    """
    Настройка логирования для проекта.
    :param log_file: Имя файла для сохранения логов.
    """
    logging.basicConfig(
        level=logging.INFO,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format="%(asctime)s - %(levelname)s - %(message)s",  # Формат сообщений
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),  # Логи в файл
            # logging.StreamHandler()  # Логи в консоль
        ]
    )
