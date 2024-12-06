from pybit.unified_trading import HTTP
from dotenv import load_dotenv
import os

# Загрузка API-ключей из файла .env
load_dotenv()
BYBIT_API_KEY_TEST = os.getenv("BYBIT_API_KEY_TEST")
BYBIT_API_SECRET_TEST = os.getenv("BYBIT_API_SECRET_TEST")

# Инициализация клиента Bybit для тестовой сети
client = HTTP(
    api_key=BYBIT_API_KEY_TEST,
    api_secret=BYBIT_API_SECRET_TEST,
    testnet=True  # Указываем, что работаем с тестовой сетью
)


def get_usdt_total_wallet_balance():
    """
    Получение общего баланса кошелька (totalWalletBalance) для USDT.
    :return: Значение totalWalletBalance для USDT.
    """
    try:
        # Запрос баланса для унифицированного аккаунта
        response = client.get_wallet_balance(accountType="UNIFIED")
        coins = response["result"]["list"][0]["coin"]

        # Ищем баланс для USDT
        for coin in coins:
            if coin["coin"] == "USDT":
                return float(coin["walletBalance"])
        raise Exception("USDT не найден в списке активов.")
    except Exception as e:
        raise Exception(f"Ошибка при запросе баланса: {e}")


# Проверка работы
try:
    usdt_balance = get_usdt_total_wallet_balance()
    print("Общий баланс кошелька для USDT (totalWalletBalance):", usdt_balance)
except Exception as e:
    print(e)
