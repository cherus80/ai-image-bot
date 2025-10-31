#!/usr/bin/env python3
"""
Скрипт для запуска Telegram бота.

Использование:
    python telegram_bot/run_bot.py

Переменные окружения:
    TELEGRAM_BOT_TOKEN - токен бота из BotFather
    WEB_APP_URL - URL Web App (например, https://your-domain.com)
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Загружаем переменные окружения
env_file = project_root / ".env"
if env_file.exists():
    load_dotenv(env_file)
    logging.info(f"Loaded environment from: {env_file}")
else:
    logging.warning(f"Environment file not found: {env_file}")

from telegram_bot.bot import create_bot

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Главная функция запуска бота"""
    # Получаем переменные окружения
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    web_app_url = os.getenv("WEB_APP_URL") or os.getenv("FRONTEND_URL", "http://localhost:5173")

    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is not set!")
        logger.error("Please set it in .env file or export it")
        sys.exit(1)

    if not web_app_url:
        logger.error("WEB_APP_URL or FRONTEND_URL environment variable is not set!")
        logger.error("Please set it in .env file or export it")
        sys.exit(1)

    logger.info("=" * 50)
    logger.info("AI Image Generator Bot - Starting...")
    logger.info(f"Web App URL: {web_app_url}")
    logger.info("=" * 50)

    try:
        # Создаём и запускаем бота
        bot = create_bot(bot_token=bot_token, web_app_url=web_app_url)
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
