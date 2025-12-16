#!/bin/bash

###############################################################################
# start-dev.sh - Скрипт для запуска всех сервисов в режиме разработки
#
# Запускает:
# 1. Docker (PostgreSQL + Redis)
# 2. Backend (FastAPI + Celery)
# 3. Frontend (React + Vite)
#
# Использование:
#   ./start-dev.sh              # Запустить все сервисы
#   ./start-dev.sh --mock       # Запустить с mock-режимом платежей
###############################################################################

set -e  # Exit on error

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функции для красивого вывода
info() {
    echo -e "${BLUE}ℹ ${1}${NC}"
}

success() {
    echo -e "${GREEN}✓ ${1}${NC}"
}

warning() {
    echo -e "${YELLOW}⚠ ${1}${NC}"
}

error() {
    echo -e "${RED}✗ ${1}${NC}"
}

# Проверка наличия Docker
check_docker() {
    info "Checking Docker..."
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker Desktop for Mac."
        exit 1
    fi

    if ! docker info &> /dev/null; then
        error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi

    success "Docker is running"
}

# Проверка наличия Python
check_python() {
    info "Checking Python..."
    if ! command -v python3 &> /dev/null; then
        error "Python 3 is not installed. Please install Python 3.11+"
        exit 1
    fi

    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    success "Python ${PYTHON_VERSION} found"
}

# Проверка наличия Node.js
check_node() {
    info "Checking Node.js..."
    if ! command -v node &> /dev/null; then
        error "Node.js is not installed. Please install Node.js 18+"
        exit 1
    fi

    NODE_VERSION=$(node --version)
    success "Node.js ${NODE_VERSION} found"
}

# Запуск Docker контейнеров
start_docker() {
    info "Starting Docker containers (PostgreSQL + Redis)..."

    docker-compose -f docker-compose.dev.yml up -d

    # Ждём, пока PostgreSQL будет готов
    info "Waiting for PostgreSQL to be ready..."
    sleep 5

    # Проверка, что контейнеры запущены
    if docker ps | grep -q "ai_image_bot_postgres_dev"; then
        success "PostgreSQL is running on port 5432"
    else
        error "Failed to start PostgreSQL"
        exit 1
    fi

    if docker ps | grep -q "ai_image_bot_redis_dev"; then
        success "Redis is running on port 6379"
    else
        error "Failed to start Redis"
        exit 1
    fi
}

# Настройка backend
setup_backend() {
    info "Setting up backend..."

    cd backend

    # Создание виртуального окружения (если не существует)
    if [ ! -d "venv" ]; then
        info "Creating Python virtual environment..."
        python3 -m venv venv
    fi

    # Активация venv
    source venv/bin/activate

    # Установка зависимостей
    info "Installing Python dependencies..."
    pip install -q -r requirements.txt

    # Применение миграций
    info "Applying database migrations..."
    alembic upgrade head

    success "Backend setup complete"

    cd ..
}

# Запуск backend
start_backend() {
    info "Starting FastAPI backend..."

    cd backend
    source venv/bin/activate

    # Запуск в фоне
    nohup uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../logs/backend.pid

    success "Backend started (PID: $BACKEND_PID)"
    info "Backend logs: logs/backend.log"
    info "Backend API: http://localhost:8000"
    info "Backend Docs: http://localhost:8000/docs"

    cd ..
}

# Запуск Celery
start_celery() {
    info "Starting Celery worker..."

    cd backend
    source venv/bin/activate

    # Запуск в фоне
    nohup celery -A app.tasks.celery_app:celery_app worker --loglevel=info -Q fitting,editing,maintenance > ../logs/celery.log 2>&1 &
    CELERY_PID=$!
    echo $CELERY_PID > ../logs/celery.pid

    success "Celery worker started (PID: $CELERY_PID)"
    info "Celery logs: logs/celery.log"

    cd ..
}

# Настройка frontend
setup_frontend() {
    info "Setting up frontend..."

    cd frontend

    # Установка зависимостей
    if [ ! -d "node_modules" ]; then
        info "Installing npm dependencies..."
        npm install
    fi

    success "Frontend setup complete"

    cd ..
}

# Запуск frontend
start_frontend() {
    info "Starting React frontend..."

    cd frontend

    # Запуск в фоне
    nohup npm run dev -- --host 0.0.0.0 --port 5173 > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../logs/frontend.pid

    success "Frontend started (PID: $FRONTEND_PID)"
    info "Frontend logs: logs/frontend.log"
    info "Frontend URL: http://localhost:5173"

    cd ..
}


# Включение mock-режима платежей
enable_mock_mode() {
    info "Enabling PAYMENT_MOCK_MODE..."

    # Обновляем .env файл backend
    if [ -f "backend/.env" ]; then
        if grep -q "PAYMENT_MOCK_MODE" backend/.env; then
            sed -i '' 's/PAYMENT_MOCK_MODE=.*/PAYMENT_MOCK_MODE=true/' backend/.env
        else
            echo "PAYMENT_MOCK_MODE=true" >> backend/.env
        fi
        success "PAYMENT_MOCK_MODE enabled in backend/.env"
    else
        warning "backend/.env not found. Please create it from backend/.env.example"
    fi
}

# Создание директории для логов
mkdir -p logs

# Основная логика
echo ""
echo "======================================"
echo "  AI Generator - Dev Start"
echo "======================================"
echo ""

# Обработка аргументов
MOCK_MODE=false
if [ "$1" == "--mock" ]; then
    MOCK_MODE=true
    warning "Running in MOCK PAYMENT MODE"
fi

# Проверка зависимостей
check_docker
check_python
check_node

echo ""

# Запуск сервисов
start_docker

echo ""

setup_backend
setup_frontend

echo ""

if [ "$MOCK_MODE" = true ]; then
    enable_mock_mode
fi

start_backend
sleep 3  # Ждём запуска backend

start_celery
sleep 2

start_frontend
sleep 2


echo ""
echo "======================================"
success "All services started successfully!"
echo "======================================"
echo ""
echo "Services running:"
echo "  • PostgreSQL:    localhost:5432"
echo "  • Redis:         localhost:6379"
echo "  • Backend API:   http://localhost:8000"
echo "  • API Docs:      http://localhost:8000/docs"
echo "  • Frontend:      http://localhost:5173"

if [ "$MOCK_MODE" = true ]; then
    echo "  • Mock Emulator: http://localhost:5173/mock-payment-emulator"
fi

echo ""
echo "Logs:"
echo "  • Backend:       logs/backend.log"
echo "  • Celery:        logs/celery.log"
echo "  • Frontend:      logs/frontend.log"
echo ""
echo "To stop all services, run: ./stop-dev.sh"
echo ""
