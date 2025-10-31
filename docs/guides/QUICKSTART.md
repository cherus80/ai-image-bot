# Quick Start — AI Image Generator Bot

Быстрое руководство по запуску backend для локальной разработки и тестирования.

## Требования

- Python 3.11+
- Docker и Docker Compose
- macOS/Linux (для Windows используйте WSL2 или Git Bash)

## Первый запуск (пошагово)

### 1. Клонирование репозитория

```bash
# Если ещё не клонировали
cd /path/to/your/projects
git clone <repo-url>
cd ai-image-bot
```

### 2. Настройка переменных окружения

```bash
cd backend

# Копирование .env.example в .env
cp .env.example .env
```

**Отредактируйте `backend/.env`** и заполните обязательные переменные:

```bash
# Минимально необходимые для запуска:
SECRET_KEY=your-secret-key-here-change-me
JWT_SECRET_KEY=your-jwt-secret-key-here-change-me
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_BOT_SECRET=your-telegram-webapp-secret

# API ключи (можно временно оставить пустыми для тестирования)
KIE_AI_API_KEY=your-kie-ai-api-key
OPENROUTER_API_KEY=your-openrouter-api-key
YUKASSA_SHOP_ID=your-yukassa-shop-id
YUKASSA_SECRET_KEY=your-yukassa-secret-key
YUKASSA_WEBHOOK_SECRET=your-webhook-secret
ADMIN_SECRET_KEY=your-admin-secret

# База данных (можно оставить по умолчанию для dev)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ai_image_bot
```

**Генерация секретных ключей:**
```bash
# Генерация случайных ключей (выполните дважды для SECRET_KEY и JWT_SECRET_KEY)
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Запуск PostgreSQL и Redis

```bash
# Вернитесь в корневую директорию проекта
cd ..

# Запуск PostgreSQL и Redis через Docker
docker-compose -f docker-compose.dev.yml up -d

# Проверка статуса
docker-compose -f docker-compose.dev.yml ps
```

**Ожидаемый вывод:**
```
NAME                          STATUS    PORTS
ai_image_bot_postgres_dev     Up        0.0.0.0:5432->5432/tcp
ai_image_bot_redis_dev        Up        0.0.0.0:6379->6379/tcp
```

**Проверка соединения:**
```bash
# PostgreSQL
docker exec ai_image_bot_postgres_dev pg_isready

# Redis
docker exec ai_image_bot_redis_dev redis-cli ping
```

### 4. Запуск Backend

```bash
cd backend

# Сделать скрипт исполняемым (только первый раз)
chmod +x run_dev.sh

# Запуск backend
./run_dev.sh
```

**Скрипт автоматически:**
1. ✅ Создаст виртуальное окружение (если не существует)
2. ✅ Установит зависимости из requirements.txt
3. ✅ Проверит наличие .env файла
4. ✅ Проверит, что PostgreSQL и Redis запущены
5. ✅ Применит миграции Alembic
6. ✅ Запустит FastAPI сервер с auto-reload

**Ожидаемый вывод:**
```
🚀 Starting AI Image Generator Bot backend (development mode)...

📦 Activating virtual environment...
✅ .env file found

🔍 Checking database connections...
✅ PostgreSQL is running
✅ Redis is running

📊 Applying database migrations...
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> abc123, Initial migration
✅ Migrations applied successfully

🌟 Starting FastAPI server...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Backend is starting...

📍 API will be available at: http://localhost:8000
📖 API Docs at: http://localhost:8000/docs
🔄 Auto-reload is enabled

Press Ctrl+C to stop the server
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
🚀 Starting AI Image Generator Bot backend...
📊 Initializing database...
✅ Backend started in development mode
INFO:     Application startup complete.
```

### 5. Тестирование API

Откройте браузер и перейдите по ссылкам:

**Health Check:**
```bash
curl http://localhost:8000/

# Ожидаемый ответ:
{
  "status": "ok",
  "service": "AI Image Generator Bot API",
  "version": "0.1.0",
  "environment": "development"
}
```

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 6. Проверка базы данных

```bash
# Подключение к PostgreSQL
docker exec -it ai_image_bot_postgres_dev psql -U postgres -d ai_image_bot

# Проверка созданных таблиц
\dt

# Ожидаемый вывод:
#          List of relations
#  Schema |      Name       | Type  |  Owner
# --------+-----------------+-------+----------
#  public | users           | table | postgres
#  public | generations     | table | postgres
#  public | chat_histories  | table | postgres
#  public | payments        | table | postgres
#  public | referrals       | table | postgres
#  public | alembic_version | table | postgres

# Выход
\q
```

## Остановка сервисов

```bash
# Остановка backend
# Нажмите Ctrl+C в терминале с запущенным backend

# Остановка PostgreSQL и Redis
docker-compose -f docker-compose.dev.yml down

# Остановка с удалением данных (опционально)
docker-compose -f docker-compose.dev.yml down -v
```

## Частые команды

### Пересоздание базы данных

```bash
# Остановка и удаление данных
docker-compose -f docker-compose.dev.yml down -v

# Запуск заново
docker-compose -f docker-compose.dev.yml up -d

# Миграции применятся автоматически при запуске ./run_dev.sh
```

### Создание новой миграции

```bash
cd backend
source venv/bin/activate

# Автогенерация миграции из моделей
alembic revision --autogenerate -m "Add new field to User"

# Применение миграции
alembic upgrade head
```

### Просмотр логов

```bash
# Логи PostgreSQL
docker logs ai_image_bot_postgres_dev -f

# Логи Redis
docker logs ai_image_bot_redis_dev -f

# Логи backend
# Смотрите в терминале, где запущен ./run_dev.sh
```

## Troubleshooting

### Ошибка: "Address already in use"

```bash
# Проверка, что порт не занят
lsof -i :8000  # Backend
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis

# Убить процесс на порту
kill -9 <PID>
```

### Ошибка: "Module not found"

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Ошибка: "Database connection failed"

```bash
# Проверка, что PostgreSQL запущен
docker ps | grep postgres

# Перезапуск PostgreSQL
docker-compose -f docker-compose.dev.yml restart postgres
```

### Ошибка миграций

```bash
# Сброс всех миграций (ВНИМАНИЕ: удалит все данные!)
cd backend
source venv/bin/activate

# Откат всех миграций
alembic downgrade base

# Удаление файлов миграций
rm -rf alembic/versions/*.py

# Создание новой начальной миграции
alembic revision --autogenerate -m "Initial migration"

# Применение
alembic upgrade head
```

## Исправленные баги (2025-10-29)

В процессе тестирования были обнаружены и исправлены следующие проблемы:

### ✅ БАГ #1: Некорректное сравнение дат с timezone
**Файл:** `backend/app/models/user.py:178`

**Проблема:** Метод `has_active_subscription` использовал `datetime.now()` вместо `datetime.now(timezone.utc)`, что приводило к ошибкам сравнения с timezone-aware datetime из БД.

**Исправление:**
```python
# Было:
return self.subscription_end > datetime.now(self.subscription_end.tzinfo)

# Стало:
from datetime import timezone
return self.subscription_end > datetime.now(timezone.utc)
```

### ✅ БАГ #2: Несогласованность в reset_freemium_if_needed
**Файл:** `backend/app/models/user.py:188`

**Проблема:** Метод использовал `datetime.now()` вместо `datetime.now(timezone.utc)`, несоответствие с полем БД `freemium_reset_at` (DateTime(timezone=True)).

**Исправление:**
```python
# Было:
self.freemium_reset_at = datetime.now()
now = datetime.now()

# Стало:
from datetime import timezone
self.freemium_reset_at = datetime.now(timezone.utc)
now = datetime.now(timezone.utc)
```

### ✅ БАГ #3: Дублирование зависимости httpx
**Файл:** `backend/requirements.txt:22, 46`

**Проблема:** Пакет `httpx==0.26.0` был указан дважды.

**Исправление:** Удалено дублирование на строке 46.

### ✅ ПРОБЛЕМА #7: Отсутствие валидации файлов перед генерацией
**Файл:** `backend/app/api/v1/endpoints/fitting.py:114`

**Проблема:** Не проверялось существование файлов с указанными UUID перед запуском генерации.

**Исправление:** Добавлена детальная проверка существования файлов с понятными сообщениями об ошибках.

### ✅ ПРОБЛЕМА #8: Дублирование сохранения в localStorage
**Файл:** `frontend/src/store/authStore.ts:63-64`

**Проблема:** Ручное сохранение в localStorage дублировало работу Zustand persist middleware.

**Исправление:** Удалены все ручные вызовы `localStorage.setItem/removeItem`, так как Zustand persist автоматически управляет localStorage.

---

## Следующие шаги

После успешного запуска backend:

1. ✅ Проверьте `/health` endpoint
2. ✅ Изучите API документацию в `/docs`
3. ✅ Этап 2: Авторизация реализована
4. ✅ Этап 3-4: API и UI примерки реализованы
5. ⏭️ Этап 5-6: Редактирование изображений (следующий этап)
6. ⏭️ Запустите frontend для тестирования интеграции

---

**Полная документация:** См. [README.md](README.md)