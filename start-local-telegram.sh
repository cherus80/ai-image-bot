#!/bin/bash

# Скрипт для запуска локального Telegram бота с проверками

echo "🚀 AI Image Generator Bot - Local Setup"
echo "========================================"
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для проверки команды
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}❌ $1 не установлен!${NC}"
        echo -e "${YELLOW}Установите его: $2${NC}"
        return 1
    else
        echo -e "${GREEN}✅ $1 установлен${NC}"
        return 0
    fi
}

# Проверка зависимостей
echo -e "${BLUE}📋 Проверка зависимостей...${NC}"
echo ""

check_command "python3" "brew install python3"
PYTHON_OK=$?

check_command "ngrok" "brew install ngrok"
NGROK_OK=$?

echo ""

# Если что-то не установлено, выходим
if [ $PYTHON_OK -ne 0 ] || [ $NGROK_OK -ne 0 ]; then
    echo -e "${RED}❌ Установите недостающие зависимости и запустите скрипт снова${NC}"
    exit 1
fi

# Проверка .env файла
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Файл .env не найден!${NC}"
    echo -e "${YELLOW}Создайте его на основе .env.example${NC}"
    exit 1
fi

# Проверка TELEGRAM_BOT_TOKEN в .env
if ! grep -q "TELEGRAM_BOT_TOKEN=" .env || grep -q "TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here" .env; then
    echo -e "${RED}❌ TELEGRAM_BOT_TOKEN не настроен в .env!${NC}"
    echo -e "${YELLOW}Получите токен от @BotFather и добавьте в .env${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Конфигурация в порядке${NC}"
echo ""

# Установка Python зависимостей
echo -e "${BLUE}📦 Установка Python зависимостей...${NC}"
cd telegram_bot
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Создание виртуального окружения...${NC}"
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt
echo -e "${GREEN}✅ Зависимости установлены${NC}"
echo ""

# Инструкции по запуску
echo -e "${BLUE}📋 Следующие шаги:${NC}"
echo ""
echo -e "${YELLOW}1.${NC} В НОВОМ ТЕРМИНАЛЕ запустите ngrok:"
echo -e "   ${GREEN}ngrok http 5174${NC}"
echo ""
echo -e "${YELLOW}2.${NC} Скопируйте HTTPS URL от ngrok (например: https://abc123.ngrok-free.app)"
echo ""
echo -e "${YELLOW}3.${NC} Обновите .env файл:"
echo -e "   ${GREEN}WEB_APP_URL=https://ваш-ngrok-url${NC}"
echo ""
echo -e "${YELLOW}4.${NC} Настройте бота в @BotFather:"
echo -e "   - Отправьте: ${GREEN}/mybots${NC}"
echo -e "   - Выберите бота → Bot Settings → Menu Button → Configure menu button"
echo -e "   - Отправьте ваш ngrok URL"
echo ""
echo -e "${YELLOW}5.${NC} Запустите этот скрипт снова для старта бота"
echo ""

# Спрашиваем, готов ли пользователь запустить бота
read -p "Вы выполнили все шаги выше? Запустить бота? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${GREEN}🤖 Запуск Telegram бота...${NC}"
    echo ""
    cd ..
    source telegram_bot/venv/bin/activate
    python telegram_bot/run_bot.py
else
    echo ""
    echo -e "${YELLOW}Хорошо! Выполните шаги выше и запустите скрипт снова.${NC}"
    echo ""
    echo -e "${BLUE}Когда будете готовы, запустите:${NC}"
    echo -e "   ${GREEN}./start-local-telegram.sh${NC}"
    echo ""
fi
