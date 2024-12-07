import logging
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()
API_ID = os.getenv("TELEGRAM_API_ID_2")
API_HASH = os.getenv("TELEGRAM_API_HASH_2")
SESSION_NAME = "session_name"
CHAT_ID = "@ZION_BOT_CH"  # ID канала

# Настройка логирования
logging.basicConfig(
    filename="telegram_parser.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

client = TelegramClient(SESSION_NAME, API_ID, API_HASH,
                        system_version='4.16.30-vxCUSTOM',
                        device_model="iPhone 13 Pro Max",
                        app_version="8.4",
                        lang_code="en",
                        system_lang_code="en-US"
                        )

async def handle_new_message(event):
    """
    Обработка нового сообщения.
    """
    try:
        message = event.message.message.strip()
        print(f"Новое сообщение: {message}")
        logging.info(f"Новое сообщение: {message}")
    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")

async def main():
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
        channel_entity = await client.get_entity(CHAT_ID)
        print(f"Подключение к каналу: {channel_entity.title}")

        # Обработка новых сообщений
        @client.on(events.NewMessage(chats=channel_entity))
        async def new_message_listener(event):
            await handle_new_message(event)

        print("Клиент Telegram успешно запущен!")
        logging.info("Клиент Telegram запущен и готов к работе.")

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
