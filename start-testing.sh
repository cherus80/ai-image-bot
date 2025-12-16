#!/bin/bash

# Скрипт для быстрого запуска приложения для тестирования
# Использование: ./start-testing.sh

set -e  # Остановка при ошибке

echo "🚀 AI Generator - Быстрый запуск для тестирования"
echo ""

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Проверка наличия .env файлов
echo "📝 Проверка конфигурации..."
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}❌ Файл backend/.env не найден!${NC}"
    echo "Создайте его из backend/.env.example"
    exit 1
fi

if [ ! -f "frontend/.env" ]; then
    echo -e "${RED}❌ Файл frontend/.env не найден!${NC}"
    echo "Создайте его из frontend/.env.example"
    exit 1
fi

echo -e "${GREEN}✅ Конфигурационные файлы найдены${NC}"

# Проверка Docker
echo ""
echo "🐳 Проверка Docker..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker не установлен!${NC}"
    echo "Установите Docker: https://www.docker.com/get-started"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker не запущен!${NC}"
    echo "Запустите Docker Desktop"
    exit 1
fi

echo -e "${GREEN}✅ Docker работает${NC}"

# Запуск PostgreSQL
echo ""
echo "🗄️  Запуск PostgreSQL..."
docker-compose up -d postgres

# Ожидание запуска PostgreSQL
echo "⏳ Ожидание запуска PostgreSQL (5 секунд)..."
sleep 5

# Проверка подключения к PostgreSQL
echo ""
echo "🔌 Проверка подключения к PostgreSQL..."
cd backend
if python3 -c "
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings

async def check_db():
    try:
        engine = create_async_engine(settings.DATABASE_URL)
        async with engine.connect() as conn:
            await conn.execute('SELECT 1')
        print('OK')
        return True
    except Exception as e:
        print(f'ERROR: {e}')
        return False

asyncio.run(check_db())
" 2>/dev/null | grep -q "OK"; then
    echo -e "${GREEN}✅ PostgreSQL доступен${NC}"
else
    echo -e "${RED}❌ Не удалось подключиться к PostgreSQL${NC}"
    echo "Проверьте настройки в backend/.env"
    exit 1
fi

# Применение миграций
echo ""
echo "📦 Применение миграций базы данных..."
if alembic upgrade head; then
    echo -e "${GREEN}✅ Миграции применены${NC}"
else
    echo -e "${YELLOW}⚠️  Ошибка миграций (возможно, уже применены)${NC}"
fi

cd ..

# Информация о запуске
echo ""
echo -e "${GREEN}✅ Подготовка завершена!${NC}"
echo ""
echo "📋 Следующие шаги:"
echo ""
echo "1️⃣  Запустите Backend (в отдельном терминале):"
echo "   cd backend && uvicorn app.main:app --reload"
echo ""
echo "2️⃣  Запустите Frontend (в другом терминале):"
echo "   cd frontend && npm run dev"
echo ""
echo "3️⃣  Откройте браузер:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000/docs"
echo ""
echo "🧪 Для тестирования:"
echo "   - Регистрация: http://localhost:5173/register"
echo "   - Вход: http://localhost:5173/login"
echo ""
echo -e "${YELLOW}ℹ️  Google Sign-In отключен. Используйте Email/Password авторизацию.${NC}"
echo ""
echo "📚 Документация:"
echo "   - QUICK_START.md - быстрый старт"
echo "   - ENV_SETUP_GUIDE.md - настройка окружения"
echo "   - FRONTEND_COMPLETED_REPORT.md - детали frontend"
echo ""
echo "🎉 Готово к тестированию!"
