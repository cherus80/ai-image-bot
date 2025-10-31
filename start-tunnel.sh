#!/bin/bash

# Скрипт для запуска туннеля БЕЗ прокси

echo "🌐 Запуск туннеля для Telegram Web App..."
echo ""

# Проверяем, установлен ли ngrok
if command -v ngrok &> /dev/null; then
    echo "✅ ngrok найден, запускаем БЕЗ прокси..."
    echo ""
    # Отключаем прокси только для этой команды
    unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
    ngrok http 5174
else
    echo "⚠️ ngrok не установлен, используем localtunnel..."
    echo ""
    npx localtunnel --port 5174
fi
