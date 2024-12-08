import logging
from pybit.unified_trading import HTTP
from dotenv import load_dotenv
import os
from decimal import Decimal, ROUND_DOWN

# Загрузка переменных окружения
load_dotenv()
BYBIT_API_KEY_TEST = os.getenv("BYBIT_API_KEY_TEST")
BYBIT_API_SECRET_TEST = os.getenv("BYBIT_API_SECRET_TEST")


class ByBitHandler:
    """
    Класс для работы с API ByBit: покупка и продажа активов.
    """
    def __init__(self):
        self.session = HTTP(
            api_key=BYBIT_API_KEY_TEST,
            api_secret=BYBIT_API_SECRET_TEST,
            testnet=True  # Указываем, что работаем с тестовой сетью
        )

    def place_market_order(self, symbol, qty, side="Buy"):
        """
        Размещение рыночного ордера на ByBit.
        :param symbol: Торговая пара (например, BTCUSDT).
        :param qty: Количество актива или сумма в USDT.
        :param side: Сторона сделки ("Buy" или "Sell").
        """
        try:
            response = self.session.place_order(
                category="spot",
                symbol=symbol,
                side=side,
                orderType="Market",
                qty=str(qty),
                timeInForce="GTC",
            )
            logging.info(f"Успешно размещен ордер: {response}")
            return response
        except Exception as e:
            logging.error(f"Ошибка при размещении ордера: {e}")
            raise e

    def get_asset_balance(self, asset):
        """
        Получение доступного баланса актива.
        :param asset: Название актива (например, BTC).
        :return: Баланс актива.
        """
        try:
            response = self.session.get_wallet_balance(accountType="UNIFIED")
            coins = response["result"]["list"][0]["coin"]
            for coin in coins:
                if coin["coin"] == asset:
                    balance = float(coin["walletBalance"])
                    logging.info(f"Баланс {asset}: {balance:.8f}")
                    return balance
            logging.warning(f"Актива {asset} нет в портфеле.")
            return 0
        except Exception as e:
            logging.error(f"Ошибка при получении баланса актива {asset}: {e}")
            raise e

    def get_asset_info(self, symbol):
        """
        Получение данных об активе с помощью get_instruments_info.
        :param symbol: Торговая пара (например, BTCUSDT).
        :return: Информация об активе.
        """
        try:
            response = self.session.get_instruments_info(category="spot", symbol=symbol)
            if response['retCode'] == 0:
                asset_info = response['result']['list'][0]
                logging.info(f"Получены данные об активе {symbol}: {asset_info}")
                return asset_info
            else:
                raise Exception(f"Ошибка получения данных об активе {symbol}: {response['retMsg']}")
        except Exception as e:
            logging.error(f"Ошибка при получении данных об активе {symbol}: {e}")
            raise e

    def execute_trade(self, action, asset):
        """
        Выполнение сделки на основе сигнала.
        :param action: "Buy" или "Sell".
        :param asset: Название актива.
        """
        try:
            symbol = f"{asset}USDT"
            asset_info = self.get_asset_info(symbol)
            base_precision = Decimal(asset_info["lotSizeFilter"]["basePrecision"])
            min_order_qty = Decimal(asset_info["lotSizeFilter"]["minOrderQty"])
            min_order_amt = Decimal(asset_info["lotSizeFilter"]["minOrderAmt"])

            if action == "Buy":
                qty = Decimal(100)  # Фиксированная сумма в USDT для покупки
                if qty < min_order_amt:
                    logging.warning(f"Сумма {qty} меньше минимально допустимой {min_order_amt}.")
                    return None
                logging.info(f"Начата покупка {asset} на сумму {qty}.")
                return self.place_market_order(symbol, qty, side="Buy")

            elif action == "Sell":
                qty = Decimal(self.get_asset_balance(asset))
                if qty < min_order_qty:
                    logging.warning(f"Количество {qty:.8f} меньше минимально допустимого {min_order_qty:.8f}.")
                    return None
                # Округляем qty до base_precision
                qty = qty.quantize(base_precision, rounding=ROUND_DOWN)
                logging.info(f"Начата продажа {asset} в количестве {qty}.")
                return self.place_market_order(symbol, qty, side="Sell")
        except Exception as e:
            logging.error(f"Ошибка при выполнении сделки: {e}")
            raise e
