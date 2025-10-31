"""
FastAPI Main Application.

Точка входа для AI Image Generator Bot backend.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.core.config import settings
from app.db import init_db, close_db
from app.services.kie_ai import close_kie_client
from app.services.openrouter import close_openrouter_client
from app.services.yukassa import close_yukassa_client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Lifespan events для FastAPI.

    Startup:
    - Инициализация БД (создание таблиц)
    - Логирование в Sentry (опционально)

    Shutdown:
    - Закрытие соединений с БД
    - Закрытие HTTP клиентов
    """
    # Startup
    print("🚀 Starting AI Image Generator Bot backend...")

    # Инициализация БД
    if not settings.is_production:
        print("📊 Initializing database...")
        await init_db()

    # Инициализация Sentry (опционально)
    if settings.SENTRY_DSN:
        import sentry_sdk
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.ENVIRONMENT,
            traces_sample_rate=0.1 if settings.is_production else 1.0,
        )
        print("📡 Sentry initialized")

    print(f"✅ Backend started in {settings.ENVIRONMENT} mode")

    yield

    # Shutdown
    print("🛑 Shutting down backend...")

    # Закрытие БД
    await close_db()

    # Закрытие HTTP клиентов
    await close_kie_client()
    await close_openrouter_client()
    await close_yukassa_client()

    print("✅ Backend shutdown complete")


# Создание FastAPI приложения
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.11.0",
    description="AI Image Generator Bot — Telegram Web App",
    docs_url="/docs" if settings.is_debug else None,
    redoc_url="/redoc" if settings.is_debug else None,
    openapi_url="/openapi.json" if settings.is_debug else None,
    lifespan=lifespan,
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend dev
        "http://127.0.0.1:3000",
        "https://yourdomain.com",  # Production (заменить на реальный домен)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# GZip Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint — health check"""
    return {
        "status": "ok",
        "service": "AI Image Generator Bot API",
        "version": "0.11.0",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint для мониторинга"""
    return {
        "status": "healthy",
        "version": "0.11.0",
        "database": "connected",  # TODO: добавить реальную проверку
        "redis": "connected",      # TODO: добавить реальную проверку
    }


# Подключение API роутеров
from app.api.v1.endpoints import auth, fitting, editing, payments, referrals, admin

app.include_router(
    auth.router,
    prefix=settings.API_V1_PREFIX,
)

app.include_router(
    fitting.router,
    prefix=f"{settings.API_V1_PREFIX}/fitting",
    tags=["fitting"],
)

app.include_router(
    editing.router,
    prefix=f"{settings.API_V1_PREFIX}/editing",
    tags=["editing"],
)

app.include_router(
    payments.router,
    prefix=f"{settings.API_V1_PREFIX}/payments",
    tags=["payments"],
)

app.include_router(
    referrals.router,
    prefix=f"{settings.API_V1_PREFIX}/referrals",
    tags=["referrals"],
)

app.include_router(
    admin.router,
    prefix=f"{settings.API_V1_PREFIX}/admin",
    tags=["admin"],
)

# Mock Payment Emulator (только для разработки)
if settings.PAYMENT_MOCK_MODE:
    from app.api.v1.endpoints import mock_payments
    app.include_router(
        mock_payments.router,
        prefix=f"{settings.API_V1_PREFIX}/mock-payments",
        tags=["mock-payments"],
    )
    print("🔧 Mock Payment Emulator enabled")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_debug,
        log_level="info" if settings.is_debug else "warning",
    )
