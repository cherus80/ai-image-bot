#!/usr/bin/env python3
"""
Тестовый скрипт для проверки Telegram бота.

Проверяет:
- Импорты модулей
- Создание экземпляра бота
- Валидацию параметров
- Доступность методов
"""

import sys
import os
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Тест импортов всех необходимых модулей"""
    print("=" * 60)
    print("ТЕСТ 1: Проверка импортов")
    print("=" * 60)

    try:
        # Импорт telegram библиотеки
        import telegram
        from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
        from telegram.ext import (
            Application,
            CommandHandler,
            ContextTypes,
        )
        print("✅ telegram модули импортированы успешно")
        print(f"   Версия python-telegram-bot: {telegram.__version__}")

        # Импорт нашего бота
        from telegram_bot.bot import TelegramBot, create_bot
        print("✅ telegram_bot.bot импортирован успешно")

        # Импорт дополнительных модулей
        import logging
        from dotenv import load_dotenv
        print("✅ Вспомогательные модули импортированы успешно")

        return True
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False


def test_bot_creation():
    """Тест создания экземпляра бота"""
    print("\n" + "=" * 60)
    print("ТЕСТ 2: Создание экземпляра бота")
    print("=" * 60)

    try:
        from telegram_bot.bot import TelegramBot, create_bot

        # Тестовые данные
        test_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
        test_url = "https://example.com"

        # Создание через класс
        bot1 = TelegramBot(bot_token=test_token, web_app_url=test_url)
        print("✅ Бот создан через класс TelegramBot")
        print(f"   bot_token: {bot1.bot_token[:20]}...")
        print(f"   web_app_url: {bot1.web_app_url}")

        # Создание через фабричную функцию
        bot2 = create_bot(bot_token=test_token, web_app_url=test_url)
        print("✅ Бот создан через фабричную функцию create_bot")

        # Проверка атрибутов
        assert bot1.bot_token == test_token
        assert bot1.web_app_url == test_url
        assert bot1.application is None  # До вызова run()
        print("✅ Атрибуты бота корректны")

        return True
    except Exception as e:
        print(f"❌ Ошибка создания бота: {e}")
        return False


def test_bot_methods():
    """Тест наличия всех необходимых методов"""
    print("\n" + "=" * 60)
    print("ТЕСТ 3: Проверка методов бота")
    print("=" * 60)

    try:
        from telegram_bot.bot import TelegramBot

        test_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
        test_url = "https://example.com"
        bot = TelegramBot(bot_token=test_token, web_app_url=test_url)

        # Список ожидаемых методов
        expected_methods = [
            'start_command',
            'help_command',
            'error_handler',
            'post_init',
            'setup_handlers',
            'run'
        ]

        for method_name in expected_methods:
            if hasattr(bot, method_name):
                method = getattr(bot, method_name)
                if callable(method):
                    print(f"✅ Метод {method_name}() доступен")
                else:
                    print(f"⚠️  {method_name} существует, но не callable")
            else:
                print(f"❌ Метод {method_name}() не найден")
                return False

        return True
    except Exception as e:
        print(f"❌ Ошибка проверки методов: {e}")
        return False


def test_environment_variables():
    """Тест переменных окружения"""
    print("\n" + "=" * 60)
    print("ТЕСТ 4: Проверка переменных окружения")
    print("=" * 60)

    try:
        from dotenv import load_dotenv

        # Пытаемся загрузить .env
        env_file = project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            print(f"✅ .env файл найден: {env_file}")
        else:
            print(f"⚠️  .env файл не найден: {env_file}")
            print("   (Это нормально для тестирования без реального токена)")

        # Проверяем наличие переменных
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        web_app_url = os.getenv("WEB_APP_URL") or os.getenv("FRONTEND_URL")

        if bot_token:
            print(f"✅ TELEGRAM_BOT_TOKEN установлен: {bot_token[:20]}...")
        else:
            print("⚠️  TELEGRAM_BOT_TOKEN не установлен")
            print("   Для запуска бота установите эту переменную в .env")

        if web_app_url:
            print(f"✅ WEB_APP_URL установлен: {web_app_url}")
        else:
            print("⚠️  WEB_APP_URL не установлен")
            print("   Для запуска бота установите эту переменную в .env")

        return True
    except Exception as e:
        print(f"❌ Ошибка проверки переменных окружения: {e}")
        return False


def test_run_script():
    """Тест скрипта запуска"""
    print("\n" + "=" * 60)
    print("ТЕСТ 5: Проверка скрипта запуска")
    print("=" * 60)

    try:
        run_bot_file = project_root / "telegram_bot" / "run_bot.py"

        if run_bot_file.exists():
            print(f"✅ Скрипт запуска найден: {run_bot_file}")

            # Проверяем права на выполнение
            if os.access(run_bot_file, os.X_OK):
                print("✅ Скрипт имеет права на выполнение")
            else:
                print("⚠️  Скрипт не имеет прав на выполнение")
                print(f"   Выполните: chmod +x {run_bot_file}")

            # Проверяем импорт
            import importlib.util
            spec = importlib.util.spec_from_file_location("run_bot", run_bot_file)
            if spec and spec.loader:
                print("✅ Скрипт можно импортировать")
            else:
                print("❌ Скрипт нельзя импортировать")
                return False

        else:
            print(f"❌ Скрипт запуска не найден: {run_bot_file}")
            return False

        return True
    except Exception as e:
        print(f"❌ Ошибка проверки скрипта: {e}")
        return False


def main():
    """Главная функция тестирования"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 12 + "ТЕСТИРОВАНИЕ TELEGRAM БОТА" + " " * 20 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    tests = [
        ("Импорты модулей", test_imports),
        ("Создание бота", test_bot_creation),
        ("Методы бота", test_bot_methods),
        ("Переменные окружения", test_environment_variables),
        ("Скрипт запуска", test_run_script),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА в тесте '{test_name}': {e}")
            results.append((test_name, False))

    # Итоговая статистика
    print("\n" + "=" * 60)
    print("ИТОГОВАЯ СТАТИСТИКА")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")

    print("\n" + "-" * 60)
    print(f"Пройдено тестов: {passed}/{total}")

    if passed == total:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("\n📋 Следующие шаги:")
        print("   1. Создайте бота через @BotFather в Telegram")
        print("   2. Добавьте TELEGRAM_BOT_TOKEN и WEB_APP_URL в .env")
        print("   3. Запустите бота: python telegram_bot/run_bot.py")
        return 0
    else:
        print("\n⚠️  НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
        print("   Проверьте ошибки выше и исправьте код")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
