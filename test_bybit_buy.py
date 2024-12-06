from pybit.unified_trading import HTTP
from dotenv import load_dotenv
import os

# Загрузка API-ключей из файла .env
load_dotenv()
BYBIT_API_KEY_TEST = os.getenv("BYBIT_API_KEY_TEST")
BYBIT_API_SECRET_TEST = os.getenv("BYBIT_API_SECRET_TEST")

# Инициализация клиента Bybit для тестовой сети
session = HTTP(
    api_key=BYBIT_API_KEY_TEST,
    api_secret=BYBIT_API_SECRET_TEST,
    testnet=True  # Указываем, что работаем с тестовой сетью
)


def place_market_order(symbol, qty, side="Buy"):
    """
    Размещение рыночного ордера на спотовом рынке.
    """
    # Размещение ордера
    response = session.place_order(
        category="spot",
        symbol=symbol,
        side=side,
        orderType="Market",
        qty=str(qty),
        timeInForce="GTC",
    )
    return response

# Тест работы
try:
    symbol = "BTCUSDT"  # Торговая пара
    qty = 100         # Количество покупаемого актива в USDT
    order_response = place_market_order(symbol=symbol, qty=qty)
    print("Ответ API:", order_response)
except Exception as e:
    print("Ошибка:", e)
