import logging
from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter

def setup_logger(log_file="app.log", max_bytes=10 * 1024 * 1024, backup_count=5):
    """
    Настройка логирования для проекта.
    :param log_file: Имя файла для сохранения логов.
    :param max_bytes: Максимальный размер файла логов (в байтах) перед ротацией.
    :param backup_count: Количество резервных копий логов.
    """
    # Настройка формата для логов в файле
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    # Ротация файлов логов
    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setFormatter(file_formatter)

    # Настройка цветного формата для консоли
    console_formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "white",
            "INFO": "cyan",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    # Настройка основного логгера
    logging.basicConfig(
        level=logging.INFO,  # Уровень логирования
        handlers=[file_handler, console_handler]  # Логи в файл и консоль
    )

    logging.info("Логирование настроено. Логи сохраняются в '%s'", log_file)
