#!/bin/bash

###############################################################################
# stop-dev.sh - Скрипт для остановки всех сервисов
###############################################################################

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() {
    echo -e "${BLUE}ℹ ${1}${NC}"
}

success() {
    echo -e "${GREEN}✓ ${1}${NC}"
}

warning() {
    echo -e "${YELLOW}⚠ ${1}${NC}"
}

# Остановка процесса по PID файлу
stop_process() {
    local name=$1
    local pid_file=$2

    if [ -f "$pid_file" ]; then
        PID=$(cat "$pid_file")
        if ps -p $PID > /dev/null 2>&1; then
            info "Stopping ${name} (PID: ${PID})..."
            kill $PID
            rm "$pid_file"
            success "${name} stopped"
        else
            warning "${name} process not found (PID: ${PID})"
            rm "$pid_file"
        fi
    else
        warning "${name} PID file not found"
    fi
}

echo ""
echo "======================================"
echo "  Stopping All Services"
echo "======================================"
echo ""

# Остановка сервисов
stop_process "Backend" "logs/backend.pid"
stop_process "Celery" "logs/celery.pid"
stop_process "Frontend" "logs/frontend.pid"

echo ""

# Остановка Docker контейнеров
info "Stopping Docker containers..."
docker-compose -f docker-compose.dev.yml down
success "Docker containers stopped"

echo ""
success "All services stopped successfully!"
echo ""
