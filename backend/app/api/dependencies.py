"""
API Dependencies — зависимости для FastAPI endpoints.

Содержит dependency functions для:
- Получение текущего пользователя из JWT токена
- Проверка авторизации
- Получение DB сессии
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.utils.jwt import JWTTokenError, verify_token

# HTTP Bearer схема для Authorization header
security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """
    Dependency для получения текущего авторизованного пользователя.

    Проверяет JWT токен из Authorization header и загружает пользователя из БД.

    Args:
        credentials: HTTP Bearer credentials (из Authorization header)
        db: Async database session

    Returns:
        User: Объект текущего пользователя

    Raises:
        HTTPException 401: Если токен невалидный или пользователь не найден
        HTTPException 403: Если пользователь заблокирован
    """
    # Извлекаем токен
    token = credentials.credentials

    try:
        # Проверяем и декодируем токен
        payload = verify_token(token)

        if not payload or "user_id" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = payload["user_id"]

    except JWTTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Загружаем пользователя из БД
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Проверяем, не заблокирован ли пользователь
    if user.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is banned",
        )

    # Обновляем время последней активности
    # (это будет делаться через middleware или другую логику)
    # user.last_activity_at = datetime.utcnow()
    # await db.commit()

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Dependency для получения только активных пользователей.

    Args:
        current_user: Текущий пользователь из get_current_user

    Returns:
        User: Объект активного пользователя

    Raises:
        HTTPException 403: Если пользователь не активен
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not active",
        )

    return current_user


# Type aliases для удобства
CurrentUser = Annotated[User, Depends(get_current_user)]
ActiveUser = Annotated[User, Depends(get_current_active_user)]
DBSession = Annotated[AsyncSession, Depends(get_db)]
