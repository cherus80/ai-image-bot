# 🧪 Руководство по локальному тестированию

Полное руководство для запуска и тестирования AI Image Generator Bot на локальном MacBook M1.

---

## 📋 Предварительные требования

### Установленное ПО

- ✅ **Docker Desktop для Mac** (с поддержкой ARM64/M1)
- ✅ **Python 3.11+** (рекомендуем через Homebrew)
- ✅ **Node.js 18+** и npm
- ✅ **Git**

### Проверка установки

```bash
# Docker
docker --version
docker info

# Python
python3 --version

# Node.js
node --version
npm --version
```

---

## 🚀 Быстрый старт

### 1. Клонирование репозитория (если ещё не сделано)

```bash
cd ~/Projects
git clone <your-repo-url>
cd "Telegram Web App для AI-генерации изображений"
```

### 2. Настройка окружения

#### Backend (.env)

Скопируйте `backend/.env.example` в `backend/.env` и заполните:

```bash
cp backend/.env.example backend/.env
nano backend/.env
```

**Обязательные переменные:**

```env
# Environment
ENVIRONMENT=development
DEBUG=True

# Database (оставить как есть для локального запуска)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ai_image_bot
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Telegram (ваши данные от @BotFather)
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_BOT_SECRET=your_bot_token_here
BOT_USERNAME=YourBotUsername

# API Keys (ваши реальные ключи)
KIE_AI_API_KEY=your_kie_api_key
OPENROUTER_API_KEY=your_openrouter_key

# ЮKassa (для mock-режима можно оставить любые значения)
YUKASSA_SHOP_ID=mock_shop_id
YUKASSA_SECRET_KEY=mock_secret_key
YUKASSA_WEBHOOK_SECRET=mock_webhook_secret

# 🔧 Mock режим платежей (включить для локального тестирования)
PAYMENT_MOCK_MODE=true

# Secrets (сгенерируйте случайные строки)
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)
ADMIN_SECRET_KEY=$(openssl rand -hex 32)
```

#### Frontend (.env)

Скопируйте `frontend/.env.example` в `frontend/.env`:

```bash
cp frontend/.env.example frontend/.env
```

```env
VITE_API_URL=http://localhost:8000
VITE_TELEGRAM_BOT_USERNAME=YourBotUsername
```

### 3. Запуск всех сервисов

#### Способ 1: Автоматический запуск (рекомендуется)

```bash
# Обычный режим
./start-dev.sh

# С mock-режимом платежей
./start-dev.sh --mock
```

Этот скрипт:
- ✅ Запустит Docker (PostgreSQL + Redis)
- ✅ Установит зависимости Python и npm
- ✅ Применит миграции БД
- ✅ Запустит Backend (FastAPI)
- ✅ Запустит Celery worker
- ✅ Запустит Frontend (Vite)
- ✅ Запустит Telegram Bot

#### Способ 2: Ручной запуск

**Шаг 1: Docker (PostgreSQL + Redis)**

```bash
docker-compose -f docker-compose.dev.yml up -d
```

**Шаг 2: Backend**

```bash
cd backend

# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Применить миграции
alembic upgrade head

# Запустить FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Шаг 3: Celery (в новом терминале)**

```bash
cd backend
source venv/bin/activate
celery -A app.celery_app.celery_app worker --loglevel=info
```

**Шаг 4: Frontend (в новом терминале)**

```bash
cd frontend

# Установить зависимости
npm install

# Запустить dev-сервер
npm run dev
```

**Шаг 5: Telegram Bot (в новом терминале)**

```bash
cd telegram_bot
source ../backend/venv/bin/activate
python bot.py
```

---

## 🔧 Mock-режим платежей

### Что это?

Mock-режим эмулирует платежи ЮKassa **без реальных транзакций**. Идеально для локального тестирования.

### Включение mock-режима

В `backend/.env`:

```env
PAYMENT_MOCK_MODE=true
```

### Использование эмулятора

1. **Запустите приложение** с mock-режимом:
   ```bash
   ./start-dev.sh --mock
   ```

2. **Откройте эмулятор** в браузере:
   ```
   http://localhost:5173/mock-payment-emulator
   ```

3. **Создайте платёж** в основном приложении (выберите тариф, нажмите "Оплатить")

4. **Вернитесь в эмулятор** — вы увидите новый платёж со статусом `PENDING`

5. **Подтвердите или отмените** платёж кнопками `Approve` или `Cancel`

6. **Проверьте результат** — кредиты/подписка должны начислиться пользователю

### API эмулятора

Доступно в Swagger: http://localhost:8000/docs

- `GET /api/v1/mock-payments/list` — список платежей
- `POST /api/v1/mock-payments/{id}/approve` — подтвердить платёж
- `POST /api/v1/mock-payments/{id}/cancel` — отменить платёж
- `POST /api/v1/mock-payments/webhook/{id}` — отправить webhook вручную

---

## 🌐 URL-адреса сервисов

| Сервис | URL | Описание |
|--------|-----|----------|
| **Frontend** | http://localhost:5173 | Главное приложение |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **ReDoc** | http://localhost:8000/redoc | Альтернативная документация |
| **PostgreSQL** | localhost:5432 | База данных |
| **Redis** | localhost:6379 | Кеш и очередь задач |
| **Mock Emulator** | http://localhost:5173/mock-payment-emulator | Эмулятор платежей |

---

## 🐛 Отладка

### Логи

Все логи сохраняются в директорию `logs/`:

```bash
# Backend логи
tail -f logs/backend.log

# Celery логи
tail -f logs/celery.log

# Frontend логи
tail -f logs/frontend.log

# Telegram Bot логи
tail -f logs/telegram_bot.log
```

### Остановка сервисов

```bash
./stop-dev.sh
```

Или вручную:

```bash
# Остановка Docker
docker-compose -f docker-compose.dev.yml down

# Остановка процессов (найти PID)
ps aux | grep uvicorn
ps aux | grep celery
ps aux | grep node
kill <PID>
```

### Очистка данных

```bash
# Очистка БД (удалит все данные!)
docker-compose -f docker-compose.dev.yml down -v

# Очистка кеша Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Очистка node_modules
rm -rf frontend/node_modules
```

---

## 🧪 Тестирование платёжного флоу

### Сценарий 1: Покупка подписки

1. Откройте приложение: http://localhost:5173
2. Войдите через Telegram WebApp (или используйте тестовый токен)
3. Перейдите в раздел "Платежи"
4. Выберите тариф подписки (Basic/Premium/Pro)
5. Нажмите "Оплатить"
6. Откройте эмулятор: http://localhost:5173/mock-payment-emulator
7. Найдите свой платёж и нажмите **Approve**
8. Вернитесь в приложение — подписка должна активироваться

### Сценарий 2: Покупка кредитов

1. В приложении выберите "Купить кредиты"
2. Выберите пакет (100/300/1000 кредитов)
3. Подтвердите покупку
4. В эмуляторе подтвердите платёж
5. Проверьте баланс кредитов в профиле

### Сценарий 3: Отмена платежа

1. Создайте платёж
2. В эмуляторе нажмите **Cancel**
3. Проверьте, что кредиты НЕ начислились

---

## 📊 Проверка состояния системы

### Проверка БД

```bash
# Подключиться к PostgreSQL
docker exec -it ai_image_bot_postgres_dev psql -U postgres -d ai_image_bot

# Проверить таблицы
\dt

# Проверить пользователей
SELECT id, telegram_id, username, credits_balance FROM users;

# Проверить платежи
SELECT payment_id, status, amount, payment_type FROM payments;

# Выход
\q
```

### Проверка Redis

```bash
# Подключиться к Redis
docker exec -it ai_image_bot_redis_dev redis-cli

# Проверить ключи
KEYS *

# Проверить конкретный ключ
GET key_name

# Выход
exit
```

### Проверка API

```bash
# Health check
curl http://localhost:8000/health

# Получить тарифы
curl http://localhost:8000/api/v1/payments/tariffs

# Список mock-платежей (если mock-режим включён)
curl http://localhost:8000/api/v1/mock-payments/list
```

---

## ⚠️ Известные проблемы

### Проблема: "Port 5432 already in use"

**Решение:** Остановите локальный PostgreSQL:

```bash
brew services stop postgresql
```

### Проблема: "Cannot connect to Docker daemon"

**Решение:** Запустите Docker Desktop:

```bash
open -a Docker
```

### Проблема: "Module not found" (Python)

**Решение:** Переустановите зависимости:

```bash
cd backend
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Проблема: Frontend не запускается

**Решение:** Очистите кеш и переустановите:

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

## 🎯 Следующие шаги

После успешного локального запуска:

1. ✅ Протестируйте все основные функции
2. ✅ Проверьте работу примерки одежды
3. ✅ Проверьте работу AI-редактора
4. ✅ Протестируйте платёжный флоу (с mock)
5. ✅ Проверьте реферальную систему
6. ✅ Запустите автотесты: `pytest backend/tests/`
7. 📝 Документируйте найденные баги в BUGFIXES.md

---

## 📚 Дополнительные ресурсы

- [README.md](README.md) — основная документация
- [TODO.md](TODO.md) — план разработки
- [CHANGELOG.md](CHANGELOG.md) — история изменений
- [TESTING.md](TESTING.md) — руководство по тестированию
- [PROJECT_STRUCTURE_ANALYSIS.md](PROJECT_STRUCTURE_ANALYSIS.md) — архитектура проекта

---

## 💡 Советы

- Используйте `./start-dev.sh --mock` для быстрого старта с mock-платежами
- Проверяйте логи регулярно: `tail -f logs/*.log`
- Используйте Swagger UI для тестирования API: http://localhost:8000/docs
- Mock-эмулятор автообновляется каждые 5 секунд
- Для production деплоя используйте `docker-compose.yml` (без mock-режима!)

---

**Удачного тестирования! 🚀**
