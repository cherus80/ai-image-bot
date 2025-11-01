#!/bin/bash

# Скрипт для исправления файлов на VPS
# Скопируйте этот скрипт на VPS и запустите

set -e

info() { echo -e "\033[0;32m[INFO]\033[0m $1"; }
error() { echo -e "\033[0;31m[ERROR]\033[0m $1"; }

info "Удаляем старую директорию..."
rm -rf /opt/ai-image-bot

info "Клонируем репозиторий заново..."
git clone https://github.com/cherus80/ai-image-bot.git /opt/ai-image-bot

cd /opt/ai-image-bot

info "Проверяем файлы..."
if [ ! -f "docker-compose.prod.yml" ]; then
    error "docker-compose.prod.yml не найден!"
    info "Создаю файлы вручную через curl..."

    # Скачиваем docker-compose.prod.yml напрямую
    curl -L "https://raw.githubusercontent.com/cherus80/ai-image-bot/master/docker-compose.prod.yml" -o docker-compose.prod.yml

    # Проверяем размер
    SIZE=$(wc -c < docker-compose.prod.yml)
    if [ "$SIZE" -lt 100 ]; then
        error "Файл docker-compose.prod.yml поврежден (размер: $SIZE байт)"
        exit 1
    fi
fi

info "Проверяем другие файлы..."
for file in docker-compose.dev.yml docker-compose.yml .env.example README.md; do
    if [ ! -f "$file" ] || [ $(wc -c < "$file") -lt 10 ]; then
        info "Скачиваем $file..."
        curl -L "https://raw.githubusercontent.com/cherus80/ai-image-bot/master/$file" -o "$file"
    fi
done

info "Проверяем директории..."
for dir in backend frontend telegram_bot nginx docs; do
    if [ ! -d "$dir" ]; then
        error "Директория $dir отсутствует!"
    fi
done

info "Список файлов в /opt/ai-image-bot:"
ls -lh

info "✅ Файлы восстановлены! Теперь можно запускать docker-compose"
