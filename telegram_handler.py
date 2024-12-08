import asyncio
import logging
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
import re

# Настройка регулярных выражений
BUY_PATTERN = re.compile(r"([A-Z0-9]+)(?=/USDT).*?LONG.*?✅\s*BUYING COMPLETED", re.IGNORECASE | re.DOTALL)
SELL_PATTERN = re.compile(r"([A-Z0-9]+)(?=/USDT).*?🆑\s*POSITION\s*CLOSED", re.IGNORECASE | re.DOTALL)

class TelegramHandler:
    """
       Класс для работы с Telegram API: подключение,
       получение сущности канала и обработка сообщений.
    """
    def __init__(self, api_id, api_hash, session_name, chat_id):
        self.client = TelegramClient(session_name, api_id, api_hash)
        self.chat_id = chat_id
        self.channel_entity = None

    async def start_client(self):
        """
        Запуск клиента Telegram и авторизация.
        """
        await self.client.start()
        if not await self.client.is_user_authorized():
            print("Требуется авторизация. Введите ваш номер телефона.")
            phone = input("Введите номер телефона: ")
            await self.client.send_code_request(phone)
            code = input("Введите код, отправленный на ваш номер: ")
            try:
                await self.client.sign_in(phone, code)
            except SessionPasswordNeededError:
                password = input("Введите ваш пароль: ")
                await self.client.sign_in(password=password)
        logging.info("Клиент Telegram успешно запущен.")

    async def connect_to_channel(self):
        """
        Получение entity канала.
        """
        try:
            self.channel_entity = await self.client.get_entity(self.chat_id)
            logging.info(f"Подключение к каналу {self.channel_entity.title} успешно выполнено.")
        except Exception as e:
            logging.error(f"Ошибка подключения к каналу: {e}")
            raise e

    async def listen_to_messages(self, callback):
        """
        Установка обработчика новых сообщений.
        """
        @self.client.on(events.NewMessage(chats=self.channel_entity))
        async def new_message_listener(event):
            message = event.message.message.strip()
            logging.info(f"Получено сообщение: {message.splitlines()[0]}")

            # Проверяем на сигнал покупки
            if BUY_PATTERN.search(message):
                asset = BUY_PATTERN.search(message).group(1)
                await callback("Buy", asset)
                return

            # Проверяем на сигнал продажи
            if SELL_PATTERN.search(message):
                asset = SELL_PATTERN.search(message).group(1)
                await callback("Sell", asset)
                return

            logging.info("Сообщение не содержит сигналов.")

    async def ensure_connection(self):
        """
        Поддержание соединения с Telegram.
        """
        while True:
            if not self.client.is_connected():
                logging.warning("Соединение с Telegram потеряно. Переподключение...")
                await self.client.connect()
                logging.info("Соединение восстановлено.")
            await asyncio.sleep(30)

    async def run(self, callback):
        """
        Запуск всех процессов.
        """
        await self.start_client()
        await self.connect_to_channel()
        await self.listen_to_messages(callback)
        asyncio.create_task(self.ensure_connection())
        await self.client.run_until_disconnected()
