"""
Утилиты для работы с JWT токенами.

Используется для создания и верификации access токенов для API.
"""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

from app.core.config import settings


class JWTTokenError(Exception):
    """Ошибка обработки JWT токена"""
    pass


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Создание JWT access токена.

    Args:
        data: Данные для включения в payload токена
        expires_delta: Время жизни токена (если не указано, берётся из settings)

    Returns:
        str: Закодированный JWT токен
    """
    to_encode = data.copy()

    # Устанавливаем время истечения токена
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
    })

    # Кодируем токен
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Проверка и декодирование JWT токена.

    Args:
        token: JWT токен для проверки

    Returns:
        Optional[dict]: Payload токена или None при ошибке

    Raises:
        JWTTokenError: При ошибке валидации токена
    """
    try:
        # Декодируем токен
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        # Проверяем наличие обязательных полей
        if "user_id" not in payload:
            raise JWTTokenError("Missing 'user_id' in token payload")

        return payload

    except JWTError as e:
        raise JWTTokenError(f"Invalid token: {str(e)}")


def get_user_id_from_token(token: str) -> Optional[int]:
    """
    Извлечение user ID из JWT токена.

    Args:
        token: JWT токен

    Returns:
        Optional[int]: User ID или None при ошибке
    """
    try:
        payload = verify_token(token)
        return payload.get("user_id") if payload else None
    except JWTTokenError:
        return None


def create_user_access_token(user_id: int, telegram_id: int) -> str:
    """
    Создание access токена для пользователя.

    Args:
        user_id: ID пользователя в БД
        telegram_id: Telegram ID пользователя

    Returns:
        str: JWT токен
    """
    return create_access_token(
        data={
            "user_id": user_id,
            "telegram_id": telegram_id,
            "type": "access",
        }
    )
