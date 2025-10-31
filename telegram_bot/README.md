# Telegram Bot для AI Image Generator Bot

Базовый Telegram бот с командой `/start` и кнопкой для открытия Web App.

## Возможности

- ✅ Команда `/start` — приветствие с кнопкой "Открыть App"
- ✅ Команда `/help` — справочная информация
- ✅ Inline кнопка с Web App URL
- ✅ Обработка ошибок
- ✅ Логирование

## Структура модуля

```
telegram_bot/
├── __init__.py        # Инициализация модуля
├── bot.py             # Основной код бота
├── run_bot.py         # Скрипт запуска
└── README.md          # Документация (этот файл)
```

## Установка и настройка

### 1. Создайте бота через BotFather

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям (название бота, username)
4. Получите API токен (например, `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Настройте Web App

1. Отправьте команду `/mybots` в BotFather
2. Выберите вашего бота
3. Нажмите "Bot Settings" → "Menu Button"
4. Выберите "Configure menu button"
5. Отправьте текст кнопки: `Открыть App`
6. Отправьте URL: ваш Web App URL (production или ngrok для локальной разработки)

### 3. Настройте переменные окружения

Добавьте в корневой `.env` файл:

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_BOT_SECRET=your_telegram_bot_token_here
BOT_USERNAME=YourBotUsername
WEB_APP_URL=https://your-domain.com  # или http://localhost:5173 для разработки
```

**Важно:** Для локальной разработки используйте [ngrok](https://ngrok.com/) или аналогичный сервис для создания публичного URL.

## Запуск бота

### Локальная разработка

```bash
# Из корневой директории проекта
python telegram_bot/run_bot.py
```

Или с использованием виртуального окружения backend:

```bash
# Активируйте виртуальное окружение
cd backend
source venv/bin/activate  # для Linux/macOS
# или
venv\Scripts\activate  # для Windows

# Запустите бота
cd ..
python telegram_bot/run_bot.py
```

### Production (Docker)

Добавьте сервис в `docker-compose.yml`:

```yaml
telegram-bot:
  build:
    context: .
    dockerfile: telegram_bot/Dockerfile
  env_file:
    - .env
  restart: unless-stopped
  networks:
    - app-network
  depends_on:
    - backend
```

Или запустите как отдельный процесс:

```bash
python telegram_bot/run_bot.py &
```

## Использование бота

### Команды

- `/start` — приветствие и кнопка "Открыть App"
- `/help` — справочная информация о боте

### Inline кнопка

После команды `/start` пользователь увидит кнопку "Открыть App", которая откроет Web App в Telegram.

## Разработка

### Добавление новых команд

Откройте [bot.py](bot.py) и добавьте новый handler:

```python
async def new_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик новой команды"""
    await update.message.reply_text("Ответ на команду")

# В методе setup_handlers()
self.application.add_handler(CommandHandler("newcommand", self.new_command))
```

### Добавление обработчиков сообщений

```python
from telegram.ext import MessageHandler, filters

async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    text = update.message.text
    # Обработка сообщения
    await update.message.reply_text(f"Вы написали: {text}")

# В методе setup_handlers()
self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
```

### Логирование

Бот использует стандартный модуль `logging` Python:

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Информационное сообщение")
logger.error("Ошибка", exc_info=True)
```

## Тестирование

### Локальное тестирование

1. Запустите бота локально
2. Используйте [ngrok](https://ngrok.com/) для публичного URL:
   ```bash
   ngrok http 5173
   ```
3. Обновите `WEB_APP_URL` в `.env` на ngrok URL
4. Откройте бота в Telegram и протестируйте команды

### Проверка логов

Логи выводятся в консоль. Для production используйте:

```bash
# Запуск с сохранением логов
python telegram_bot/run_bot.py > bot.log 2>&1 &
```

## Деплой

### Вариант 1: systemd service (Linux)

Создайте файл `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=AI Image Generator Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/project
Environment="PATH=/path/to/project/backend/venv/bin"
ExecStart=/path/to/project/backend/venv/bin/python telegram_bot/run_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Запустите сервис:

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

### Вариант 2: Docker

Создайте `telegram_bot/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY telegram_bot/ ./telegram_bot/
COPY .env .

CMD ["python", "telegram_bot/run_bot.py"]
```

Соберите и запустите:

```bash
docker build -t telegram-bot -f telegram_bot/Dockerfile .
docker run -d --name telegram-bot --env-file .env telegram-bot
```

## Мониторинг

### Проверка статуса бота

```bash
# Просмотр логов (systemd)
journalctl -u telegram-bot -f

# Просмотр логов (Docker)
docker logs -f telegram-bot

# Проверка процесса
ps aux | grep run_bot.py
```

### Отправка команды боту

Откройте бота в Telegram и отправьте `/start`. Вы должны увидеть приветственное сообщение с кнопкой.

## Обработка ошибок

Бот автоматически логирует все ошибки и отправляет пользователю уведомление при возникновении проблем.

Для production рекомендуется настроить интеграцию с [Sentry](https://sentry.io/) для мониторинга ошибок.

## Дополнительные возможности

### Интеграция с Backend API

Если нужно взаимодействовать с Backend API (например, для отправки уведомлений):

1. Импортируйте настройки из `backend/app/core/config.py`
2. Используйте `httpx` для HTTP запросов
3. Добавьте соответствующие endpoints в Backend

### Webhook режим (вместо polling)

Для production рекомендуется использовать webhook вместо polling:

```python
# В bot.py, метод run()
self.application.run_webhook(
    listen="0.0.0.0",
    port=8443,
    url_path="telegram",
    webhook_url=f"{your_domain}/telegram"
)
```

Настройте nginx для проксирования запросов на порт 8443.

## Поддержка

По вопросам создайте issue в репозитории проекта.

---

**Версия:** 0.12.0
**Автор:** AI Image Generator Bot Team
**Лицензия:** MIT
