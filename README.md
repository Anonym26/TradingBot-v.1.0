# 🚀 Автоматизированный торговый бот для ByBit с интеграцией Telegram

![Статус сборки](https://img.shields.io/badge/build-passing-brightgreen)
![Лицензия](https://img.shields.io/badge/license-MIT-blue)

---

## 📝 Описание

**Торговый бот для ByBit** — это автоматизированная система, которая:

1. Подключается к Telegram-каналу.
2. Анализирует входящие сигналы на покупку и продажу.
3. Выполняет спотовые сделки на бирже ByBit в тестовой или основной сети.

---

## 🔧 Основные возможности

- 📩 **Подключение к Telegram**: Обработка сигналов о покупке/продаже.
- 🔄 **Интеграция с ByBit**: Автоматическое выполнение сделок.
- 🧪 **Работа с тестовой сетью ByBit**: Для безопасного тестирования.
- 📊 **Работа с основной сетью ByBit**: Для торговли на реальном счете.
- 🛠 **Расширенное логирование**: Для отслеживания работы программы.
- 🛡 **Минимальная проверка параметров сделки**: Учет лимитов биржи.

---

## 🛠 Требования

- Python 3.8 и выше
- Установленные библиотеки (см. `requirements.txt`)
- Аккаунты на Telegram и ByBit

---

## 🚀 Установка

1. **Клонируйте репозиторий**:
    ```bash
    git clone https://github.com/ваш-username/ваш-репозиторий.git
    cd ваш-репозиторий
    ```

2. **Установите зависимости**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Создайте файл `.env`**:
    В корневой папке создайте файл `.env` и добавьте в него параметры:
    ```env
    # Telegram API
    TELEGRAM_API_ID=<Ваш_Telegram_API_ID>
    TELEGRAM_API_HASH=<Ваш_Telegram_API_HASH>
    
    # API ByBit (основная сеть)
    BYBIT_API_KEY=<Ваш_ByBit_API_KEY>
    BYBIT_API_SECRET=<Ваш_ByBit_API_SECRET>
    
    # API ByBit (тестовая сеть)
    BYBIT_API_KEY_TEST=<Ваш_ByBit_API_KEY>
    BYBIT_API_SECRET_TEST=<Ваш_ByBit_API_SECRET>
    ```

---

## ⚙️ Настройка

### 1. **Получение API-ключей Telegram**
   - Зайдите на сайт [Telegram API](https://my.telegram.org/auth).
   - Создайте новое приложение и получите `api_id` и `api_hash`.

### 2. **Получение API-ключей ByBit**
   - Зарегистрируйтесь на ByBit (или войдите).
   - Создайте API-ключи для тестовой сети в [API Management](https://testnet.bybit.com).
   - Создайте API-ключи для основной сети в [API Management](https://bybit.com).

### 3. **Настройка сети**
   - Настройте параметры сети в которой будете работать (осносная / тестовая).
   - Для этого укажите соответствующие API и статус тестовой сети:
  ```python
    class ByBitHandler:
    """
    Класс для работы с API ByBit: покупка и продажа активов.
    """
    def __init__(self):
        self.session = HTTP(
            api_key=BYBIT_API_KEY_TEST, # Указываем соответствующий API KEY для тестовой или основной сети
            api_secret=BYBIT_API_SECRET_TEST,  # Указываем соответствующий API SECRET для тестовой или основной сети
            testnet=True  # True - работаем с тестовой сетью. False - с основной.
        )
  ```

### 4. **Подключение Telegram канала**
  - Задайте параметры подключения к Telegram
  ```python
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = "session_name"
CHAT_ID = "@ai_for_live_content"  # Укажите реальный ID или username
  ```

---

## 🧪 Тестирование API
1. **Тестирование Telegram API**:
Проверьте подключение к Telegram API, выполнив: 
 ```bash
    python tests/test_telegram_api.py
 ```
После успешного подключения вы увидите имя вашего аккаунта в консоли.

2. **Тестирование ByBit API**:
Проверьте подключение к ByBit API, и получение баланса выполнив:
 ```bash
    python tests/test_bybit_api.py
 ```
После успешного выполнения вы увидите текущий баланс USDT в консоли.

---

## 📄 Примечания
- Убедитесь, что вы используете тестовую сеть ByBit для безопасного тестирования.
- Telegram-аккаунт должен быть авторизован для работы с каналами или чатами.
- Бот настроен на спотовую торговлю используя счет "единого торгового аккаунта".

---

## 💻 Использование

 ❗ Пред финальным запуском не забудьте переключиться с тестовой на основную сеть.
 
1. **Запуск программы**:
    ```bash
    python main.py
    ```
    
3. **Ожидание сигналов**:
    После запуска программа будет подключена к указанному Telegram-каналу и обрабатывать поступающие сигналы.

4. **Логи**:
    Все действия записываются в файл `main.log`.

---

## 📂 Модули

| Модуль              | Описание                                     |
|---------------------|---------------------------------------------|
| `main.py`           | Главный модуль для запуска программы        |
| `telegram_handler.py` | Обработка сигналов Telegram                |
| `bybit_handler.py`  | Интеграция с ByBit                         |
| `logging_config.py` | Настройка логирования                      |

---

## 🔍 Примеры работы

### Пример сигнала из Telegram:
<table>
  <tr>
    <td>
        
🚀 AVAX/USDT LONG on BINANCE           

BUY TIME 15:41 GMT (+3 MSK)

✅ BUYING COMPLETED        

📈 AVERAGE PRICE: 52,6 USDT

Trade AVAX/USDT on Binance
    
   </td>
    <td>
      
❌ CRV/USDT on BINANCE
      
SELL TIME 14:39 GMT (+3 MSK)

🆑 POSITION CLOSED

📉 AVERAGE PRICE: 1,231475 USDT

💰 TAKE PROFIT: 0,44 %

Trade CRV/USDT on Binance
  </tr>
</table>

Бот распознает такие сообщения и автоматически покупает или продает актив.

---

## 🤝 Вклад в проект

Буду рад вашему вкладу в проект! Если у вас есть идеи для улучшения, открывайте [issues](https://github.com/Anonym26/TradingBot-v.1.0/issues) или отправляйте Pull Requests.

---

## 📜 Лицензия

Проект распространяется под лицензией [MIT](LICENSE).

---

## 📜 Автор

- 🔗 GitHub: [Anonym26](https://github.com/Anonym26)
- 🚀 Проект был создан для автоматизации сигналов из Telegram и интеграции с API ByBit.

---

✨ **Наслаждайтесь автоматизированной торговлей!** 🚀
