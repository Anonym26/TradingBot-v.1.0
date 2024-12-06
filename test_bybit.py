import requests
import time
import hmac
import hashlib
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

# Конфигурация
TESTNET_BASE_URL = "https://api-testnet.bybit.com"
BYBIT_API_KEY_TEST = os.getenv("BYBIT_API_KEY_TEST")
BYBIT_API_SECRET_TEST = os.getenv("BYBIT_API_SECRET_TEST")


def generate_signature(BYBIT_API_SECRET_TEST, params):
    """
    Генерация подписи для авторизации запроса.
    :param BYBIT_API_SECRET_TEST: Секретный ключ API.
    :param params: Параметры запроса.
    :return: Подпись запроса.
    """
    sorted_params = "&".join(f"{key}={value}" for key, value in sorted(params.items()))
    return hmac.new(
        bytes(BYBIT_API_SECRET_TEST, "utf-8"),
        bytes(sorted_params, "utf-8"),
        hashlib.sha256
    ).hexdigest()


def get_usdt_total_wallet_balance():
    """
    Получение общего баланса кошелька (totalWalletBalance) для USDT.
    :return: Значение totalWalletBalance для USDT.
    """
    endpoint = "/v5/account/wallet-balance"
    url = f"{TESTNET_BASE_URL}{endpoint}"

    # Параметры запроса
    params = {
        "api_key": BYBIT_API_KEY_TEST,
        "accountType": "UNIFIED",  # Тип аккаунта
        "timestamp": int(time.time() * 1000)  # Текущее время в миллисекундах
    }

    # Добавляем подпись
    params["sign"] = generate_signature(BYBIT_API_SECRET_TEST, params)

    # Выполняем GET-запрос
    response = requests.get(url, params=params)

    if response.status_code == 200:
        response_data = response.json()
        # Извлекаем totalWalletBalance для USDT
        try:
            coins = response_data["result"]["list"][0]["coin"]  # Достаём список монет
            for coin in coins:
                if coin["coin"] == "USDT":
                    return float(coin["walletBalance"])  # Возвращаем totalWalletBalance
            raise Exception("USDT не найден в списке активов.")
        except (KeyError, IndexError):
            raise Exception("Не удалось найти информацию о балансе в ответе API.")
    else:
        raise Exception(f"Ошибка API: {response.status_code}, {response.text}")


# Проверка работы
try:
    usdt_balance = get_usdt_total_wallet_balance()
    print("Общий баланс кошелька для USDT (totalWalletBalance):", usdt_balance)
except Exception as e:
    print("Ошибка при запросе баланса USDT:", e)
