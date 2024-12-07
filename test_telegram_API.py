from telethon import TelegramClient
from dotenv import load_dotenv
import os

# Загрузка API-ключей из файла .env
load_dotenv()
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID_2")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH_2")

# Создайте клиент Telegram
client = TelegramClient('session_name', TELEGRAM_API_ID, TELEGRAM_API_HASH,
                        system_version='4.16.30-vxCUSTOM',
                        device_model="iPhone 13 Pro Max",
                        app_version="8.4",
                        lang_code="en",
                        system_lang_code="en-US"
                        )

async def main():
    # Выводим имя вашего аккаунта
    me = await client.get_me()
    print(f"Successfully connected as {me.username}")

# Запуск клиента
with client:
    client.loop.run_until_complete(main())
