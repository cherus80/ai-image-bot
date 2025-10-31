#!/bin/bash

# Production deployment script для AI Image Generator Bot на Beget VPS
# Использование: ./deploy.sh [start|stop|restart|logs|status|build|update]

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функции для красивого вывода
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка .env файлов
check_env_files() {
    info "Проверка файлов окружения..."

    if [ ! -f "backend/.env.production" ]; then
        error "Файл backend/.env.production не найден!"
        error "Скопируйте backend/.env.example в backend/.env.production и заполните реальными значениями"
        exit 1
    fi

    if [ ! -f "frontend/.env.production" ]; then
        warn "Файл frontend/.env.production не найден, создаю из .env.example..."
        cp frontend/.env.example frontend/.env.production
    fi

    if [ ! -f "telegram_bot/.env.production" ]; then
        warn "Файл telegram_bot/.env.production не найден, создаю из backend/.env.production..."
        grep "TELEGRAM_BOT_TOKEN\|WEB_APP_URL\|FRONTEND_URL" backend/.env.production > telegram_bot/.env.production
    fi

    info "Файлы окружения готовы"
}

# Запуск production
start() {
    info "Запуск production окружения..."
    check_env_files

    # Загрузка переменных из .env.production для docker-compose
    export $(grep -v '^#' backend/.env.production | xargs)

    # Запуск через docker-compose
    docker-compose -f docker-compose.prod.yml up -d

    info "Production окружение запущено!"
    info "Проверьте статус: ./deploy.sh status"
}

# Остановка production
stop() {
    info "Остановка production окружения..."
    docker-compose -f docker-compose.prod.yml down
    info "Production окружение остановлено"
}

# Перезапуск production
restart() {
    info "Перезапуск production окружения..."
    stop
    sleep 2
    start
}

# Просмотр логов
logs() {
    SERVICE=${1:-}
    if [ -z "$SERVICE" ]; then
        info "Показываю логи всех сервисов (Ctrl+C для выхода)..."
        docker-compose -f docker-compose.prod.yml logs -f --tail=100
    else
        info "Показываю логи сервиса: $SERVICE (Ctrl+C для выхода)..."
        docker-compose -f docker-compose.prod.yml logs -f --tail=100 "$SERVICE"
    fi
}

# Статус сервисов
status() {
    info "Статус production сервисов:"
    docker-compose -f docker-compose.prod.yml ps
}

# Сборка образов
build() {
    info "Сборка Docker образов..."
    check_env_files

    # Загрузка переменных
    export $(grep -v '^#' backend/.env.production | xargs)

    # Сборка образов
    docker-compose -f docker-compose.prod.yml build --no-cache

    info "Образы успешно собраны!"
}

# Обновление и перезапуск
update() {
    info "Обновление приложения..."

    # Pull последних изменений (если используется git)
    if [ -d ".git" ]; then
        info "Обновление кода из git..."
        git pull
    fi

    # Пересборка образов
    build

    # Перезапуск сервисов
    restart

    info "Обновление завершено!"
}

# Миграции БД
migrate() {
    info "Запуск миграций БД..."
    docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
    info "Миграции выполнены"
}

# Backup БД
backup() {
    info "Создание backup БД..."
    BACKUP_DIR="./backups"
    mkdir -p "$BACKUP_DIR"

    BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"

    docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U postgres ai_image_bot > "$BACKUP_FILE"

    info "Backup создан: $BACKUP_FILE"
}

# Health check
health() {
    info "Проверка здоровья сервисов..."

    # Backend health
    if curl -f http://localhost:8000/health &> /dev/null; then
        info "✓ Backend: OK"
    else
        error "✗ Backend: FAILED"
    fi

    # Frontend health
    if curl -f http://localhost:3000/ &> /dev/null; then
        info "✓ Frontend: OK"
    else
        error "✗ Frontend: FAILED"
    fi

    # PostgreSQL health
    if docker-compose -f docker-compose.prod.yml exec -T postgres pg_isready &> /dev/null; then
        info "✓ PostgreSQL: OK"
    else
        error "✗ PostgreSQL: FAILED"
    fi

    # Redis health
    if docker-compose -f docker-compose.prod.yml exec -T redis redis-cli ping &> /dev/null; then
        info "✓ Redis: OK"
    else
        error "✗ Redis: FAILED"
    fi
}

# Очистка старых образов и volumes
cleanup() {
    warn "Очистка неиспользуемых Docker ресурсов..."
    docker system prune -f
    info "Очистка завершена"
}

# Помощь
usage() {
    cat << EOF
Production deployment script для AI Image Generator Bot

Использование: ./deploy.sh [команда]

Команды:
  start       Запустить production окружение
  stop        Остановить production окружение
  restart     Перезапустить production окружение
  logs        Показать логи всех сервисов
  logs <srv>  Показать логи конкретного сервиса (backend, frontend, postgres, redis, celery_worker)
  status      Показать статус сервисов
  build       Пересобрать Docker образы
  update      Обновить код, пересобрать образы и перезапустить
  migrate     Запустить миграции БД
  backup      Создать backup БД
  health      Проверить здоровье сервисов
  cleanup     Очистить неиспользуемые Docker ресурсы
  help        Показать эту справку

Примеры:
  ./deploy.sh start          # Запустить production
  ./deploy.sh logs backend   # Смотреть логи backend
  ./deploy.sh restart        # Перезапустить всё
  ./deploy.sh backup         # Создать backup БД

EOF
}

# Главная логика
case "${1:-}" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs "${2:-}"
        ;;
    status)
        status
        ;;
    build)
        build
        ;;
    update)
        update
        ;;
    migrate)
        migrate
        ;;
    backup)
        backup
        ;;
    health)
        health
        ;;
    cleanup)
        cleanup
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        error "Неизвестная команда: ${1:-}"
        echo ""
        usage
        exit 1
        ;;
esac
