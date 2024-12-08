import asyncio
import logging
from dotenv import load_dotenv

from logging_config import setup_logger
from telegram_handler import TelegramHandler
from bybit_handler import ByBitHandler
import os

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
setup_logger("main.log")

# Задайте параметры подключения к Telegram
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = "session_name"
CHAT_ID = "@ai_for_live_content"  # Укажите реальный ID или username канала

# Инициализация ByBitHandler
bybit_handler = ByBitHandler()

async def process_signal(action, asset):
    """
    Callback-функция для обработки сигналов.
    :param action: Тип сигнала ("Buy" или "Sell").
    :param asset: Название актива (например, BTC).
    """
    try:
        logging.info(f"Получен сигнал: {action} {asset}")
        print(f"Получен сигнал: {action} {asset}")

        # Выполняем сделку на ByBit
        response = bybit_handler.execute_trade(action, asset)
        logging.info(f"Результат сделки: {response}")
        print(f"Результат сделки: {response}")
    except Exception as e:
        logging.error(f"Ошибка при обработке сигнала {action} {asset}: {e}")
        print(f"Ошибка при обработке сигнала {action} {asset}: {e}")

async def main():
    """
    Основной процесс работы программы.
    """
    # Инициализация TelegramHandler
    telegram_handler = TelegramHandler(API_ID, API_HASH, SESSION_NAME, CHAT_ID)

    # Запуск TelegramHandler
    try:
        await telegram_handler.run(process_signal)
    except Exception as e:
        logging.error(f"Ошибка в работе TelegramHandler: {e}")
        print(f"Ошибка в работе TelegramHandler: {e}")

if __name__ == "__main__":
    try:
        print("Программа запущена. Ждем сигналы $$$")
        asyncio.run(main())

    except KeyboardInterrupt:
        print("Работа программы завершена вручную.")
        logging.info("Работа программы завершена вручную.")
