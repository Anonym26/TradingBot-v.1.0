import logging
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv
import os
import asyncio
import re

# Загрузка переменных окружения
load_dotenv()
API_ID = os.getenv("TELEGRAM_API_ID_2")
API_HASH = os.getenv("TELEGRAM_API_HASH_2")
SESSION_NAME = "session_name"
CHAT_ID = "@ai_for_live_content"  # Замените на реальный ID или username канала

# Настройка логирования
logging.basicConfig(
    filename="logs/test_telegram_message.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"  # Указываем кодировку
)

# Авторизация клиента Telegram
client = TelegramClient(
    SESSION_NAME, API_ID, API_HASH,
    system_version='4.16.30-vxCUSTOM',
    device_model="iPhone 13 Pro Max",
    app_version="8.4",
    lang_code="en",
    system_lang_code="en-US"
)

# Регулярные выражения для поиска сигналов
BUY_PATTERN = re.compile(r"([A-Z0-9]+)(?=/USDT).*?LONG.*?✅\s*BUYING COMPLETED", re.IGNORECASE | re.DOTALL)
SELL_PATTERN = re.compile(r"([A-Z0-9]+)(?=/USDT).*?🆑\s*POSITION\s*CLOSED", re.IGNORECASE | re.DOTALL)


async def handle_new_message(event):
    """
    Обработка нового сообщения.
    """
    try:
        message = event.message.message.strip()
        print(f"Новое сообщение: {message}")
        logging.info(f"Новое сообщение: {message}")

        # Проверяем на сигнал покупки
        buy_match = BUY_PATTERN.search(message)
        if buy_match:
            asset = buy_match.group(1)
            logging.info(f"Сигнал на покупку: Buy {asset}")
            print(f"Сигнал на покупку: Buy {asset}")
            return "Buy", asset

        # Проверяем на сигнал продажи
        sell_match = SELL_PATTERN.search(message)
        if sell_match:
            asset = sell_match.group(1)
            logging.info(f"Сигнал на продажу: Sell {asset}")
            print(f"Сигнал на продажу: Sell {asset}")
            return "Sell", asset

        # Если сообщение не соответствует формату
        logging.info("Сообщение не содержит сигналов.")
        print("Сообщение не содержит сигналов.")
        buy_match = BUY_PATTERN.search(message)
        sell_match = SELL_PATTERN.search(message)
        print(f"BUY_PATTERN: {buy_match}")
        print(f"SELL_PATTERN: {sell_match}")

    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")
        print(f"Ошибка при обработке сообщения: {e}")


async def ensure_connection():
    """
    Периодическая проверка соединения с Telegram и его восстановление при разрыве.
    """
    while True:
        try:
            if not client.is_connected():
                print("Соединение потеряно. Попытка переподключения...")
                logging.warning("Соединение потеряно. Попытка переподключения...")
                await client.connect()
                print("Соединение восстановлено.")
                logging.info("Соединение восстановлено.")
        except Exception as e:
            logging.error(f"Ошибка при попытке восстановить соединение: {e}")
        await asyncio.sleep(30)  # Проверка каждые 30 секунд


async def main():
    """
    Основная логика программы.
    """
    print("Запуск клиента Telegram...")
    try:
        await client.start()

        # Проверка авторизации
        if not await client.is_user_authorized():
            print("Требуется авторизация. Введите ваш номер телефона.")
            phone = input("Введите номер телефона: ")
            await client.send_code_request(phone)
            code = input("Введите код, отправленный на ваш номер: ")
            try:
                await client.sign_in(phone, code)
            except SessionPasswordNeededError:
                password = input("Введите ваш пароль: ")
                await client.sign_in(password=password)

        # Получение entity канала
        try:
            channel_entity = await client.get_entity(CHAT_ID)
            print(f"Подключение к каналу: {channel_entity.title}")
            logging.info(f"Подключение к каналу {channel_entity.title} успешно выполнено.")
        except Exception as e:
            logging.error(f"Ошибка подключения к каналу: {e}")
            print(f"Ошибка подключения к каналу: {e}")
            return

        # Обработка новых сообщений
        @client.on(events.NewMessage(chats=channel_entity))
        async def new_message_listener(event):
            await handle_new_message(event)

        print("Клиент Telegram успешно запущен!")
        logging.info("Клиент Telegram успешно запущен!")

        # Запуск задачи проверки соединения
        asyncio.create_task(ensure_connection())

        # Удерживаем клиента в активном состоянии
        await client.run_until_disconnected()
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
        print(f"Критическая ошибка: {e}")


if __name__ == "__main__":
    try:
        with client:
            client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Работа программы завершена вручную.")
        logging.info("Работа программы завершена вручную.")
