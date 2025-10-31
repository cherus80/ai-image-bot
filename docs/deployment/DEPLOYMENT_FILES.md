# Файлы для деплоя на production

Список всех созданных файлов для развёртывания AI Image Generator Bot на Beget VPS.

---

## Созданные файлы

### 📄 Конфигурационные файлы

1. **[nginx/ai-image-bot.conf](nginx/ai-image-bot.conf)**
   - Конфигурация nginx для production
   - Reverse proxy для Backend API, Frontend, WebSocket
   - SSL настройки, security headers, gzip
   - **Нужно изменить**: `your-domain.com` на ваш домен

2. **[docker-compose.prod.yml](docker-compose.prod.yml)**
   - Production docker-compose файл
   - Все сервисы: PostgreSQL, Redis, Backend, Celery, Frontend, Telegram Bot
   - Healthchecks, логирование, restart policies
   - Порты только на localhost для безопасности

3. **[frontend/Dockerfile.prod](frontend/Dockerfile.prod)**
   - Production Dockerfile для frontend
   - Multi-stage build (Node.js → nginx)
   - Build-time аргументы для VITE_*
   - Healthcheck встроен

4. **[telegram_bot/Dockerfile](telegram_bot/Dockerfile)**
   - Dockerfile для Telegram бота
   - Python 3.11 slim
   - Non-root пользователь
   - Healthcheck

5. **[backend/.env.production.example](backend/.env.production.example)**
   - Шаблон для production .env
   - Все необходимые переменные окружения
   - Инструкции по генерации секретных ключей
   - **Копировать в** `backend/.env.production` и заполнить

### 🔧 Скрипты управления

6. **[deploy.sh](deploy.sh)** ⭐ **ОСНОВНОЙ СКРИПТ**
   - Управление production окружением
   - Команды: start, stop, restart, logs, build, update
   - Автоматическая проверка .env файлов
   - Backup, migrate, health check, cleanup
   - **Сделан исполняемым**: `chmod +x deploy.sh`

### 📚 Документация

7. **[DEPLOY.md](DEPLOY.md)** ⭐ **ПОЛНАЯ ИНСТРУКЦИЯ**
   - Подробное руководство по деплою на Beget VPS
   - Все шаги от A до Z
   - Настройка сервера, SSL, nginx, Docker
   - Troubleshooting, backup, мониторинг
   - **Размер**: ~600 строк

8. **[QUICK_DEPLOY.md](QUICK_DEPLOY.md)** ⭐ **БЫСТРЫЙ СТАРТ**
   - Краткая инструкция для быстрого запуска
   - 8 шагов до production
   - Чек-лист готовности
   - Полезные команды

9. **[NGINX_SETUP.md](NGINX_SETUP.md)**
   - Детальная инструкция по настройке nginx
   - Объяснение каждой секции конфигурации
   - Troubleshooting nginx проблем
   - Безопасность и оптимизация

---

## Структура файлов после деплоя

```
/var/www/ai-image-bot/
├── backend/
│   ├── .env.production              # <- СОЗДАТЬ из .env.production.example
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── .env.production              # <- СОЗДАТЬ из .env.example
│   ├── src/
│   ├── Dockerfile.prod              # <- НОВЫЙ
│   └── package.json
├── telegram_bot/
│   ├── .env.production              # <- СОЗДАТЬ вручную или через deploy.sh
│   ├── bot.py
│   ├── run_bot.py
│   ├── Dockerfile                   # <- НОВЫЙ
│   └── requirements.txt
├── nginx/
│   └── ai-image-bot.conf            # <- НОВЫЙ
├── docker-compose.yml               # Development
├── docker-compose.prod.yml          # <- НОВЫЙ (Production)
├── deploy.sh                        # <- НОВЫЙ (Скрипт управления)
├── DEPLOY.md                        # <- НОВЫЙ (Полная инструкция)
├── QUICK_DEPLOY.md                  # <- НОВЫЙ (Быстрый старт)
├── NGINX_SETUP.md                   # <- НОВЫЙ (Настройка nginx)
└── DEPLOYMENT_FILES.md              # <- НОВЫЙ (Этот файл)
```

---

## Что нужно сделать перед деплоем

### ✅ Шаг 1: Создать .env файлы

```bash
# Backend
cp backend/.env.production.example backend/.env.production
nano backend/.env.production
# Заполните все API ключи!

# Frontend
cp frontend/.env.example frontend/.env.production
nano frontend/.env.production
# Укажите VITE_API_BASE_URL=https://your-domain.com

# Telegram Bot (или создастся автоматически через deploy.sh)
echo "TELEGRAM_BOT_TOKEN=your_token" > telegram_bot/.env.production
echo "WEB_APP_URL=https://your-domain.com" >> telegram_bot/.env.production
```

### ✅ Шаг 2: Получить SSL сертификаты

```bash
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com
```

### ✅ Шаг 3: Настроить nginx

```bash
# Копировать конфигурацию
sudo cp nginx/ai-image-bot.conf /etc/nginx/sites-available/

# Редактировать (заменить your-domain.com)
sudo nano /etc/nginx/sites-available/ai-image-bot.conf

# Создать симлинк
sudo ln -s /etc/nginx/sites-available/ai-image-bot.conf /etc/nginx/sites-enabled/

# Проверить и перезагрузить
sudo nginx -t
sudo systemctl reload nginx
```

### ✅ Шаг 4: Запустить через Docker

```bash
# Сборка
./deploy.sh build

# Запуск
./deploy.sh start

# Миграции
./deploy.sh migrate

# Проверка
./deploy.sh health
```

### ✅ Шаг 5: Настроить Telegram Bot

Через @BotFather:
- `/setmenubutton` → URL: https://your-domain.com
- `/setcommands` → start, help

### ✅ Шаг 6: Настроить ЮKassa Webhook

https://yookassa.ru/my → Уведомления:
- URL: `https://your-domain.com/api/v1/payments/webhook`
- События: `payment.succeeded`, `payment.canceled`

---

## Использование deploy.sh

```bash
# Запуск production
./deploy.sh start

# Остановка
./deploy.sh stop

# Перезапуск
./deploy.sh restart

# Обновление (git pull + rebuild + restart)
./deploy.sh update

# Просмотр логов
./deploy.sh logs
./deploy.sh logs backend
./deploy.sh logs celery_worker

# Статус сервисов
./deploy.sh status

# Health check
./deploy.sh health

# Создать backup БД
./deploy.sh backup

# Запустить миграции
./deploy.sh migrate

# Очистить Docker ресурсы
./deploy.sh cleanup

# Справка
./deploy.sh help
```

---

## Важные URL после деплоя

- **Frontend**: https://your-domain.com
- **Backend API**: https://your-domain.com/api/v1
- **Swagger UI**: https://your-domain.com/docs (отключите в production!)
- **Health Check**: https://your-domain.com/api/v1/health
- **Админка**: https://your-domain.com/admin (требует ADMIN_SECRET_KEY)
- **Telegram Bot**: https://t.me/YourBotUsername

---

## Секретные ключи

Нужно сгенерировать:

```bash
# SECRET_KEY (64 символа)
openssl rand -hex 32

# JWT_SECRET_KEY (64 символа)
openssl rand -hex 32

# ADMIN_SECRET_KEY (32 символа)
openssl rand -hex 16

# YUKASSA_WEBHOOK_SECRET (48 символов)
openssl rand -hex 24

# POSTGRES_PASSWORD (случайный)
openssl rand -base64 32
```

**⚠️ ВАЖНО:**
- Сохраните все ключи в безопасном месте (password manager)
- НЕ коммитьте .env.production в git!
- После первого деплоя НЕ МЕНЯЙТЕ SECRET_KEY и JWT_SECRET_KEY

---

## Чек-лист готовности

Перед запуском в production проверьте:

- [ ] Все .env.production файлы созданы и заполнены
- [ ] SSL сертификаты получены (`sudo certbot certificates`)
- [ ] nginx конфигурация проверена (`sudo nginx -t`)
- [ ] Docker образы собраны (`./deploy.sh build`)
- [ ] Все сервисы запущены (`./deploy.sh status`)
- [ ] Health check пройден (`./deploy.sh health`)
- [ ] Миграции БД выполнены (`./deploy.sh migrate`)
- [ ] Telegram Bot настроен через @BotFather
- [ ] ЮKassa webhook настроен (https://yookassa.ru/my)
- [ ] Backup настроен (cron job: `./deploy.sh backup`)
- [ ] Логи проверены на ошибки (`./deploy.sh logs`)
- [ ] Приложение доступно по HTTPS
- [ ] Swagger UI отключен в nginx.conf (закомментирован)
- [ ] ADMIN_SECRET_KEY надёжно сохранён

---

## Поддержка

- **Полная инструкция**: [DEPLOY.md](DEPLOY.md)
- **Быстрый старт**: [QUICK_DEPLOY.md](QUICK_DEPLOY.md)
- **Настройка nginx**: [NGINX_SETUP.md](NGINX_SETUP.md)
- **Скрипт управления**: `./deploy.sh help`

---

**Готово к деплою! 🚀**

Следуйте инструкции [QUICK_DEPLOY.md](QUICK_DEPLOY.md) для быстрого старта
или [DEPLOY.md](DEPLOY.md) для подробного руководства.
