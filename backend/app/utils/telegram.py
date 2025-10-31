"""
Утилиты для работы с Telegram WebApp.

Валидация initData согласно документации:
https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
"""

import hashlib
import hmac
import json
import time
from typing import Optional
from urllib.parse import parse_qsl, unquote


class TelegramInitDataError(Exception):
    """Ошибка валидации Telegram initData"""
    pass


def validate_telegram_init_data(
    init_data: str,
    bot_token: str,
    max_age_seconds: int = 86400  # 24 часа
) -> dict:
    """
    Валидация initData от Telegram WebApp.

    Args:
        init_data: Строка initData из Telegram WebApp SDK
        bot_token: Токен бота из BotFather
        max_age_seconds: Максимальный возраст данных в секундах (по умолчанию 24 часа)

    Returns:
        dict: Распарсенные и валидированные данные пользователя

    Raises:
        TelegramInitDataError: Если валидация не прошла
    """
    try:
        # Парсим параметры из initData
        parsed_data = dict(parse_qsl(init_data))

        # Проверяем наличие обязательных полей
        if "hash" not in parsed_data:
            raise TelegramInitDataError("Missing 'hash' parameter")

        received_hash = parsed_data.pop("hash")

        # Проверяем auth_date
        if "auth_date" not in parsed_data:
            raise TelegramInitDataError("Missing 'auth_date' parameter")

        try:
            auth_date = int(parsed_data["auth_date"])
        except (ValueError, TypeError):
            raise TelegramInitDataError("Invalid 'auth_date' parameter")

        # Проверяем, что данные не устарели
        current_time = int(time.time())
        if current_time - auth_date > max_age_seconds:
            raise TelegramInitDataError(
                f"initData is too old (age: {current_time - auth_date}s, max: {max_age_seconds}s)"
            )

        # Создаём data_check_string согласно алгоритму Telegram
        # Сортируем параметры по ключу
        data_check_arr = [f"{key}={value}" for key, value in sorted(parsed_data.items())]
        data_check_string = "\n".join(data_check_arr)

        # Создаём secret_key = HMAC_SHA256(bot_token, "WebAppData")
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=bot_token.encode(),
            digestmod=hashlib.sha256
        ).digest()

        # Вычисляем hash = HMAC_SHA256(secret_key, data_check_string)
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        # Сравниваем хэши
        if not hmac.compare_digest(calculated_hash, received_hash):
            raise TelegramInitDataError("Invalid hash signature")

        # Парсим user данные
        if "user" not in parsed_data:
            raise TelegramInitDataError("Missing 'user' parameter")

        try:
            user_data = json.loads(unquote(parsed_data["user"]))
        except (json.JSONDecodeError, TypeError):
            raise TelegramInitDataError("Invalid 'user' parameter format")

        # Проверяем обязательные поля user
        if "id" not in user_data:
            raise TelegramInitDataError("Missing 'id' in user data")

        return {
            "telegram_id": user_data["id"],
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "username": user_data.get("username"),
            "language_code": user_data.get("language_code"),
            "is_premium": user_data.get("is_premium", False),
            "auth_date": auth_date,
            "query_id": parsed_data.get("query_id"),
        }

    except TelegramInitDataError:
        raise
    except Exception as e:
        raise TelegramInitDataError(f"Unexpected error during validation: {str(e)}")


def get_telegram_user_id(init_data: str, bot_token: str) -> Optional[int]:
    """
    Быстрое получение Telegram user ID из initData.

    Args:
        init_data: Строка initData из Telegram WebApp SDK
        bot_token: Токен бота из BotFather

    Returns:
        Optional[int]: Telegram user ID или None при ошибке
    """
    try:
        validated_data = validate_telegram_init_data(init_data, bot_token)
        return validated_data["telegram_id"]
    except TelegramInitDataError:
        return None
