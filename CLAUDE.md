# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

# AI Image Generator Bot – Telegram Web App

## Цель проекта
Создать Telegram Web App для виртуальной примерки одежды/аксессуаров и редактирования изображений с помощью модели Nano Banana через kie.ai и ассистента Claude Haiku (OpenRouter), с гибридной монетизацией (Freemium, подписки, покупка кредитов) и безопасной архитектурой.

## Технологический стек
- Frontend: React 18+ (TypeScript, Vite, Tailwind, Telegram WebApp SDK)
- Backend: FastAPI (Python 3.11+), SQLAlchemy (async), Celery, WebSocket, Pydantic
- База данных: PostgreSQL 15 (JSONB для истории чата)
- Внешние API: kie.ai Nano Banana, OpenRouter (Claude Haiku), ЮKassa, Telegram Bot API
- Деплой: Docker/Portainer (Beget VPS)

## Ключевые функции
1. **Примерка одежды/аксессуаров (step-квиз без AI-ассистента)**
   - Фиксированный промпт для генерации через kie.ai
   - Валидация файлов (JPEG/PNG, ≤5MB, MIME, UUID-имя)
   - Списание 2 кредитов за генерацию

2. **Редактирование изображений (чат с AI-ассистентом)**
   - История чата (только последние 10 сообщений)
   - Генерация нескольких вариантов промптов через Claude Haiku (OpenRouter)
   - WebSocket для отображения прогресса
   - Списание 1 кредит за запрос, 1 — за генерацию

3. **Авторизация**
   - Проверка Telegram initData через HMAC SHA-256
   - JWT-токены для сессий

4. **Монетизация**
   - Freemium: 10 действий/месяц с водяным знаком
   - Подписки: 299₽/50, 499₽/150, 899₽/500 действий
   - Кредиты: 199₽/100 кредитов
   - ЮKassa webhook и автоматическое начисление
   - Учёт налогов для НПД (4%) и комиссии ЮKassa (2.8%)

## КРИТИЧЕСКИ ВАЖНЫЕ ПРАВИЛА РАБОТЫ С КОДОМ

### ⚠️ ЗАПРЕЩЕНО без разрешения пользователя:

1. **НЕ УРЕЗАТЬ КОД**:
   - НИКОГДА не заменяйте существующий код на заглушки типа `# ... existing code ...` или `{/* ... existing code ... */}`
   - НИКОГДА не пропускайте части кода с комментариями `# ... остальной код ...` или `// ... rest of code ...`
   - ВСЕГДА показывайте полный код модуля/функции/компонента при внесении изменений
   - При исправлении багов сохраняйте весь функционал, который уже работает

2. **НЕ СОЗДАВАТЬ ДУБЛИ**:
   - ПЕРЕД созданием любого кода, функции или компонента — ОБЯЗАТЕЛЬНО проверьте, не существует ли уже такая реализация
   - Используйте Grep/Glob для поиска похожих функций/компонентов
   - Если функционал уже есть — используйте его, не создавайте новый
   - Не плодите копии одной и той же логики в разных местах

3. **НЕ УДАЛЯТЬ ФУНКЦИОНАЛ**:
   - Функционал приложения не должен урезаться без явного указания пользователя
   - Если нужно изменить логику — спросите у пользователя, прежде чем удалять существующие возможности
   - Сохраняйте обратную совместимость API

### 📋 ОБЯЗАТЕЛЬНЫЙ ЧЕК-ЛИСТ перед написанием кода:

1. [ ] **Запросил актуальную документацию через context7 для всех используемых библиотек/API?**
2. [ ] Проверил, существует ли уже такая функция/компонент/модуль? (Grep/Glob)
3. [ ] Уверен, что не дублирую существующий код?
4. [ ] Показываю полный код без заглушек?
5. [ ] Сохраняю весь существующий функционал?
6. [ ] Спросил у пользователя, если собираюсь удалить функционал?

### 🔌 ОБЯЗАТЕЛЬНОЕ ИСПОЛЬЗОВАНИЕ MCP CONTEXT7

**⚠️ КРИТИЧЕСКИ ВАЖНО:** Перед выполнением ЛЮБОЙ задачи по кодингу ОБЯЗАТЕЛЬНО использовать MCP context7 для получения актуальной документации!

#### Когда ОБЯЗАТЕЛЬНО использовать context7:

1. **Перед написанием кода с использованием библиотек/фреймворков:**
   - React, TypeScript, Vite, Tailwind CSS
   - FastAPI, SQLAlchemy, Celery, Pydantic
   - Telegram WebApp SDK, Telegram Bot API
   - Любые другие внешние библиотеки из tech stack

2. **Перед интеграцией с внешними API:**
   - kie.ai Nano Banana API
   - OpenRouter API (Claude Haiku)
   - ЮKassa Payment API
   - Telegram Bot API

3. **Перед решением сложных задач:**
   - Асинхронное программирование (async/await)
   - WebSocket реализация
   - JWT авторизация
   - HMAC подписи
   - Database миграции (Alembic)

#### Как правильно использовать context7:

**Формат запроса:**
```
use context7 to get [library name] [version] [specific topic] documentation

Примеры:
- use context7 to get FastAPI WebSocket implementation examples
- use context7 to get SQLAlchemy async session relationship examples
- use context7 to get React 18 hooks best practices
- use context7 to get Telegram WebApp SDK latest API documentation
- use context7 to get Celery task retry configuration
```

**Workflow для задач по кодингу:**

1. **Получить задачу от пользователя**
2. **Определить технологии/библиотеки, которые будут использованы**
3. **ОБЯЗАТЕЛЬНО запросить актуальную документацию через context7:**
   ```
   use context7 to get [каждая технология из списка]
   ```
4. **Изучить полученную документацию**
5. **Проверить существующий код (Grep/Glob)**
6. **Написать код, следуя актуальным best practices из context7**
7. **Обновить TODO.md при необходимости**

#### Примеры обязательного использования:

**Задача:** Добавить WebSocket для real-time обновлений статуса генерации

**Правильный подход:**
```
1. use context7 to get FastAPI WebSocket implementation guide
2. use context7 to get SQLAlchemy async session with WebSocket examples
3. Изучить полученную документацию
4. Проверить существующий код: grep -r "websocket" backend/
5. Написать код согласно актуальным best practices
```

**Задача:** Исправить ошибку в Celery task

**Правильный подход:**
```
1. use context7 to get Celery error handling and retry strategies
2. use context7 to get Celery async task best practices
3. Изучить актуальные паттерны
4. Исправить код
```

**Задача:** Реализовать новый React компонент

**Правильный подход:**
```
1. use context7 to get React 18 TypeScript component patterns
2. use context7 to get Zustand state management examples
3. Проверить существующие компоненты: glob "frontend/src/components/**/*.tsx"
4. Написать компонент согласно актуальным best practices
```

#### ❌ ЗАПРЕЩЕНО:

1. **Писать код БЕЗ предварительного запроса документации через context7**
2. **Полагаться только на устаревшие знания или примеры из интернета**
3. **Игнорировать актуальные best practices, полученные через context7**
4. **Использовать deprecated API без проверки через context7**

#### ✅ ПРАВИЛЬНО:

1. **ВСЕГДА начинать задачи с запроса актуальной документации через context7**
2. **Сверяться с context7 при возникновении ошибок или неопределённостей**
3. **Использовать актуальные версии API и best practices из context7**
4. **Документировать использованные паттерны из context7 в комментариях кода**

**⚠️ Эти правила являются ОБЯЗАТЕЛЬНЫМИ и имеют приоритет наравне с правилами "НЕ УРЕЗАТЬ КОД" и "НЕ СОЗДАВАТЬ ДУБЛИ"!**

### 📝 ОБЯЗАТЕЛЬНОЕ ОБНОВЛЕНИЕ ПРОГРЕССА:

**ПОСЛЕ завершения каждого этапа разработки из TODO.md:**

1. **ОБЯЗАТЕЛЬНО обновить TODO.md**:
   - Изменить статус этапа с ⏳ на ✅
   
   - Отметить все выполненные подзадачи: [ ] → [x]
   - Добавить итоговую секцию с результатами этапа
   - Указать количество созданных файлов и модулей


2. **Шаблон итоговой секции для TODO.md**:
```
### Итого по Этапу X
- ✅ **Backend/Frontend полностью реализован** (N модулей создано)
- ✅ **Создано M сервисов/компонентов**: список
- 📚 **Документация:** CHANGELOG.md обновлён (версия X.Y.Z)
- 🔍 **Доступно для тестирования:** описание
- ⏳ **Тестирование:** статус тестов

**Этап X завершён! Готово к следующему этапу.**
```

**⚠️ КРИТИЧЕСКИ ВАЖНО:** Не переходить к следующему этапу без обновления TODO.md!

## Стандарты кодирования
- async/await для всех IO-операций (Backend)
- Проверка файлов MIME-типов и сигнатур (magic bytes)
- Разделение структуры /backend, /frontend с отдельными CLAUDE.md
- Каждый модуль должен иметь отдельный CLAUDE.md с описанием логики
- No sensitive keys in code: все через переменные окружения (.env)
- API-ключи для всех интеграций указывать только в .env

## Структура базы данных
- Таблицы: users, generations, chat_history, payments (описать поля и индексы кратко)
- Чат-история — хранить последние 10 сообщений (JSONB)
- Идемпотентность: использовать idempotency_key при начислении кредитов

## Интеграции
- **kie.ai Nano Banana API**: описание endpoint и параметров
- **OpenRouter Claude Haiku**: системный промпт на английском, структура сообщений для чата
- **ЮKassa**: URL webhook, проверка подписи, поля для идентификации платежа и начисления токенов

## Обработка ошибок
- Retry для API-запросов (3 попытки, exponential backoff)
- Отправка ошибок в чат с понятным сообщением для пользователя

## Важные ограничения
- Не хранить пароли в открытом виде
- Не доверять только расширению файлов — проверять тип и сигнатуру
- Не использовать синхронные операции БД
- Для генерации изображений использовать Celery (не FastAPI BackgroundTasks)
- Отправлять только последние 10 сообщений в OpenRouter для чата

## Обязательно записывай всю историю изминений в проекте в файле CHANGELOG.md
## Ты выступаешь в качестве главного аркестратора. Ты получаешь задание от пользователя и решаешь какой агент из дирректории .claude/agents лучше справиться с полученым заданием. Поручаешь выполнение задания выбраному агенту далее получаешь от него отвчет о выполнении задания и уже потом отвечаешь пользователю.

---

## 🚀 Команды для разработки

### Локальная разработка

**Запуск всех сервисов (Docker + Backend + Frontend + Bot):**
```bash
./start-dev.sh
```

**Остановка всех сервисов:**
```bash
./stop-dev.sh
```

**Backend только:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend только:**
```bash
cd frontend
npm install
npm run dev  # Запуск на http://localhost:5173
```

**⚠️ ВАЖНОЕ ПРАВИЛО: Остановка dev сервера перед запуском нового**

**КРИТИЧЕСКИ ВАЖНО:** ВСЕГДА останавливать работающий dev сервер перед запуском нового, чтобы не создавать дубликаты на разных портах!

**Проблема:** Если dev сервер уже запущен на порту 5173, Vite автоматически запустит новый сервер на следующем свободном порту (5174, 5175 и т.д.), что создаёт путаницу.

**Правильный workflow:**

1. **Проверить работающие процессы:**
```bash
# Найти процессы на порту 5173
lsof -i :5173
# или
ps aux | grep "npm run dev"
```

2. **Остановить работающий dev сервер:**
```bash
# Если запущен через Bash tool с ID:
KillShell tool с ID процесса

# Если запущен вручную:
# Найти PID и убить процесс
kill -9 <PID>

# Или использовать pkill:
pkill -f "vite"
```

3. **Только после остановки запускать новый:**
```bash
cd frontend
npm run dev
```

**❌ НЕПРАВИЛЬНО:**
- Запускать `npm run dev` не проверив наличие работающего сервера
- Игнорировать сообщение "Port 5173 is in use, trying another one"
- Оставлять множество dev серверов работающими параллельно

**✅ ПРАВИЛЬНО:**
- ВСЕГДА проверять и останавливать работающий dev сервер перед запуском нового
- Использовать один и тот же порт (5173) для консистентности
- Если порт занят - остановить процесс, а не запускать на новом порту

**Celery worker (обязательно для генерации изображений):**
```bash
cd backend
celery -A app.tasks.celery_app worker --loglevel=info
```

**Celery beat (для периодических задач):**
```bash
cd backend
celery -A app.tasks.celery_app beat --loglevel=info
```

### Тестирование

**Backend тесты:**
```bash
cd backend
pytest tests/ -v --cov=app                    # Все тесты с покрытием
pytest tests/test_auth.py -v                  # Только авторизация
pytest tests/test_credits.py -v               # Только кредиты
pytest tests/test_auth.py::test_name -v       # Конкретный тест
pytest tests/ -k "test_telegram" -v           # Тесты по паттерну
```

**Frontend тесты:**
```bash
cd frontend
npm test              # Запуск Jest тестов
npm run test:watch    # Watch mode
```

**Линтинг:**
```bash
cd frontend
npm run lint
```

### Docker Compose

**Development:**
```bash
docker-compose up -d                          # Запуск всех сервисов
docker-compose logs -f backend                # Логи backend
docker-compose ps                             # Статус контейнеров
docker-compose down                           # Остановка
```

**Production:**
```bash
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### База данных

**Миграции Alembic:**
```bash
cd backend
alembic revision --autogenerate -m "описание"  # Создать миграцию
alembic upgrade head                           # Применить все миграции
alembic downgrade -1                           # Откатить последнюю
alembic history                                # История миграций
alembic current                                # Текущая версия
```

**Создание тестовой БД:**
```bash
./backend/tests/create_test_db.sh
```

### Деплой на VPS

**Автоматический деплой:**
```bash
./vps-deploy-script.sh
```

**Обновление и деплой:**
```bash
./update-and-deploy.sh
```

**Быстрый деплой:**
```bash
./deploy.sh
```

---

## 🏛️ Архитектура проекта

### Структура Backend (FastAPI)

```
backend/app/
├── main.py                           # Entry point, CORS, middleware
├── core/
│   ├── config.py                     # Pydantic Settings (все env переменные)
│   ├── security.py                   # JWT, HMAC, Telegram validation
│   └── deps.py                       # FastAPI dependencies (get_db, get_current_user)
├── api/v1/endpoints/
│   ├── auth.py                       # POST /auth/telegram, GET /auth/me
│   ├── fitting.py                    # 5 endpoints: upload, generate, status, result, history
│   ├── editing.py                    # 6 endpoints: upload, session, chat, generate, history, delete
│   ├── payments.py                   # 5 endpoints: create, webhook, history, tariffs, status
│   ├── referrals.py                  # 3 endpoints: link, register, stats
│   ├── admin.py                      # 4 endpoints: stats, charts, users, export
│   └── mock_payments.py              # Mock payment emulator (dev only)
├── models/
│   ├── user.py                       # User: telegram_id, balance_credits, subscription_type
│   ├── generation.py                 # Generation: type, photos, credits_spent
│   ├── chat.py                       # ChatHistory: session_id, messages (JSONB)
│   ├── payment.py                    # Payment: yukassa_payment_id, tax_amount, commission
│   └── referral.py                   # Referral: referrer_id, referred_id, bonus_credits
├── schemas/
│   ├── auth.py                       # TelegramAuthRequest, TokenResponse, UserResponse
│   ├── fitting.py                    # FittingRequest, FittingResponse, GenerationStatus
│   ├── editing.py                    # EditingRequest, ChatMessage, PromptVariant
│   ├── payment.py                    # PaymentCreate, YuKassaWebhook, TariffResponse
│   └── user.py                       # UserProfile, BalanceResponse
├── services/
│   ├── kie_ai.py                     # Nano Banana API (try_on, image_editing)
│   ├── openrouter.py                 # Claude Haiku API (generate_prompt_variants)
│   ├── yukassa.py                    # YuKassa payments + webhook verification
│   ├── yukassa_mock.py               # Mock payment provider
│   ├── credits.py                    # deduct_credits, add_credits, check_balance
│   ├── billing.py                    # Tariff calculations, subscription logic
│   ├── chat.py                       # Chat session management (10 messages limit)
│   ├── file_storage.py               # Upload/download/delete from server
│   ├── file_validator.py             # MIME validation + magic bytes checking
│   └── watermark.py                  # Freemium watermark overlay
├── tasks/
│   ├── celery_app.py                 # Celery config + beat schedule
│   ├── fitting.py                    # generate_fitting_task() - async generation
│   ├── editing.py                    # generate_editing_task() - async generation
│   └── maintenance.py                # Periodic tasks: file cleanup, freemium reset
└── db/
    ├── session.py                    # AsyncSession factory
    └── base.py                       # SQLAlchemy Base class
```

### Структура Frontend (React + TypeScript)

```
frontend/src/
├── App.tsx                           # Router setup, AuthGuard
├── main.tsx                          # Entry point, Telegram WebApp init
├── pages/
│   ├── HomePage.tsx                  # Landing with feature cards
│   ├── FittingPage.tsx               # Try-on wizard (3 steps)
│   ├── EditingPage.tsx               # AI editing with chat
│   ├── ProfilePage.tsx               # User profile + referral stats
│   ├── AdminPage.tsx                 # Admin dashboard (requires secret key)
│   └── MockPaymentEmulator/          # Payment testing tool
├── components/
│   ├── auth/AuthGuard.tsx            # Telegram initData validation wrapper
│   ├── fitting/
│   │   ├── FittingWizard.tsx         # Step navigation
│   │   ├── Step1UserPhoto.tsx        # User photo upload
│   │   ├── Step2ItemPhoto.tsx        # Item photo upload
│   │   ├── Step3Zone.tsx             # Zone selection (head/neck/hands/legs)
│   │   ├── FittingResult.tsx         # Result display with download
│   │   └── GenerationProgress.tsx    # Progress bar with status
│   ├── editing/
│   │   ├── ChatWindow.tsx            # Chat container
│   │   ├── ChatMessage.tsx           # Message bubble (user/assistant)
│   │   ├── ChatInput.tsx             # Text input + send button
│   │   ├── ImageMessage.tsx          # Image display in chat
│   │   └── PromptSelector.tsx        # 3 prompt variants selection
│   ├── payment/
│   │   ├── PaymentWizard.tsx         # Payment flow
│   │   ├── SubscriptionCard.tsx      # Subscription plan card
│   │   └── CreditsCard.tsx           # Credits package card
│   ├── admin/
│   │   ├── StatsCard.tsx             # Dashboard stat card
│   │   └── UsersTable.tsx            # Users list with filters
│   ├── common/
│   │   └── FileUpload.tsx            # Drag-n-drop upload (react-dropzone)
│   └── ui/
│       ├── Button.tsx                # Reusable button
│       ├── Card.tsx                  # Reusable card
│       └── Badge.tsx                 # Status badge
├── store/
│   ├── authStore.ts                  # Auth state: user, token, isLoading
│   ├── fittingStore.ts               # Fitting state: userPhoto, itemPhoto, zone
│   ├── chatStore.ts                  # Chat state: messages, sessionId
│   └── paymentStore.ts               # Payment state: selectedPlan, status
├── api/
│   ├── client.ts                     # Axios instance with JWT interceptor
│   ├── auth.ts                       # login(), getCurrentUser(), refreshProfile()
│   ├── fitting.ts                    # uploadPhotos(), generate(), pollStatus()
│   ├── editing.ts                    # uploadImage(), sendMessage(), generate()
│   ├── payment.ts                    # createPayment(), pollPaymentStatus()
│   ├── referral.ts                   # getLink(), register(), getStats()
│   └── admin.ts                      # getStats(), getUsers(), exportPayments()
└── types/
    ├── user.ts                       # User, SubscriptionType
    ├── generation.ts                 # Generation, GenerationStatus
    ├── chat.ts                       # ChatMessage, PromptVariant
    └── payment.ts                    # Payment, Tariff, PaymentStatus
```

### Поток данных (Data Flow)

**1. Авторизация:**
```
Frontend → Telegram.initDataUnsafe
       → POST /api/v1/auth/telegram (initData)
       → Backend: HMAC SHA-256 validation
       → Create/Update User in DB
       → Return JWT token
       → Frontend: Store token in authStore + localStorage
```

**2. Примерка (Try-on):**
```
User uploads photos → FileUpload validates (JPEG/PNG, ≤5MB)
                   → POST /api/v1/fitting/upload (FormData)
                   → Backend: file_validator.py (MIME + magic bytes)
                   → Save to /uploads with UUID names
                   → POST /api/v1/fitting/generate
                   → credits.py: deduct 2 credits
                   → Celery task: generate_fitting_task.delay()
                   → kie_ai.py: try_on API call (retry 3x)
                   → Save result to /uploads
                   → Frontend: Poll GET /api/v1/fitting/status/{task_id}
                   → Display result with download button
```

**3. AI-редактирование (Editing):**
```
User uploads image → POST /api/v1/editing/upload
                   → POST /api/v1/editing/session (create chat session)
                   → User types message in ChatInput
                   → POST /api/v1/editing/chat
                   → credits.py: deduct 1 credit
                   → chat.py: Save to chat_history (JSONB)
                   → openrouter.py: Send last 10 messages to Claude Haiku
                   → Return 3 prompt variants
                   → User selects/edits prompt
                   → POST /api/v1/editing/generate
                   → credits.py: deduct 1 credit
                   → Celery task: generate_editing_task.delay()
                   → kie_ai.py: image_editing API call
                   → Frontend: Poll status → Display result
```

**4. Монетизация:**
```
User selects plan → PaymentWizard
                  → POST /api/v1/payments/create (tariff_id)
                  → yukassa.py: Create payment in YuKassa
                  → Return payment URL (confirmation_url)
                  → Telegram WebApp: openLink(confirmation_url)
                  → User pays → YuKassa webhook
                  → POST /api/v1/payments/webhook (HMAC verification)
                  → billing.py: Calculate tax (4%) + commission (2.8%)
                  → credits.py: add_credits (idempotent)
                  → Frontend: Poll GET /api/v1/payments/status/{payment_id}
                  → Refresh user profile
```

---

## 📁 Критически важные файлы

### Backend Core
- **backend/app/main.py:1** — FastAPI app init, CORS, routers, middleware
- **backend/app/core/config.py:1** — Settings класс (все env переменные)
- **backend/app/core/security.py:1** — validate_telegram_init_data(), create_jwt_token()
- **backend/app/core/deps.py:1** — get_db(), get_current_user() dependencies

### API Endpoints
- **backend/app/api/v1/endpoints/auth.py:1** — Telegram авторизация
- **backend/app/api/v1/endpoints/fitting.py:1** — Примерка (5 endpoints)
- **backend/app/api/v1/endpoints/editing.py:1** — AI-редактирование (6 endpoints)
- **backend/app/api/v1/endpoints/payments.py:1** — Платежи + webhook

### Services (бизнес-логика)
- **backend/app/services/kie_ai.py:1** — Интеграция с Nano Banana
- **backend/app/services/openrouter.py:1** — Интеграция с Claude Haiku
- **backend/app/services/yukassa.py:1** — Интеграция с YuKassa
- **backend/app/services/credits.py:1** — Логика кредитов
- **backend/app/services/chat.py:1** — Управление чатом (10 сообщений)
- **backend/app/services/file_validator.py:1** — Валидация файлов (MIME + magic bytes)

### Models (БД)
- **backend/app/models/user.py:1** — User модель (credits, subscription)
- **backend/app/models/generation.py:1** — Generation модель
- **backend/app/models/chat.py:1** — ChatHistory модель (JSONB)
- **backend/app/models/payment.py:1** — Payment модель

### Celery Tasks
- **backend/app/tasks/celery_app.py:1** — Celery config + beat schedule
- **backend/app/tasks/fitting.py:1** — generate_fitting_task()
- **backend/app/tasks/editing.py:1** — generate_editing_task()

### Frontend Core
- **frontend/src/App.tsx:1** — Router + AuthGuard
- **frontend/src/main.tsx:1** — Entry point + Telegram WebApp init
- **frontend/src/api/client.ts:1** — Axios instance с JWT interceptor

### Frontend Pages
- **frontend/src/pages/FittingPage.tsx:1** — Wizard для примерки
- **frontend/src/pages/EditingPage.tsx:1** — AI-редактирование с чатом
- **frontend/src/pages/ProfilePage.tsx:1** — Профиль пользователя

### Frontend Stores (Zustand)
- **frontend/src/store/authStore.ts:1** — Авторизация
- **frontend/src/store/fittingStore.ts:1** — Состояние примерки
- **frontend/src/store/chatStore.ts:1** — Состояние чата

---

## 🗄️ База данных (детали)

### Таблица: users
```python
id: Integer (PK)
telegram_id: BigInteger (unique, indexed)
username: String(255), nullable
first_name: String(255)
last_name: String(255), nullable
balance_credits: Integer (default=0)
subscription_type: Enum('BASIC', 'PRO', 'PREMIUM'), nullable
subscription_end: DateTime, nullable
freemium_actions_used: Integer (default=0)
freemium_reset_at: DateTime (default=now + 30 days)
is_active: Boolean (default=True)
is_banned: Boolean (default=False)
created_at: DateTime
updated_at: DateTime
```

### Таблица: generations
```python
id: UUID (PK)
user_id: Integer (FK → users.id, indexed)
type: Enum('fitting', 'editing')
user_photo_url: String(500), nullable
item_photo_url: String(500), nullable
base_image_url: String(500), nullable  # для editing
prompt: Text, nullable
result_image_url: String(500), nullable
status: Enum('pending', 'processing', 'completed', 'failed')
credits_spent: Integer
has_watermark: Boolean (default=False)
error_message: Text, nullable
created_at: DateTime
completed_at: DateTime, nullable
```

### Таблица: chat_history
```python
id: UUID (PK)
user_id: Integer (FK → users.id, indexed)
session_id: UUID (unique, indexed)
base_image_url: String(500)
messages: JSONB  # Array of {role, content, image_url, timestamp}
is_active: Boolean (default=True)
message_count: Integer (default=0)
created_at: DateTime
updated_at: DateTime
```

**messages JSONB структура:**
```json
[
  {
    "role": "user",
    "content": "Сделай фон синим",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  {
    "role": "assistant",
    "content": "Вот 3 варианта промптов...",
    "prompt_variants": [
      {"id": 1, "text": "Blue background..."},
      {"id": 2, "text": "Azure sky background..."},
      {"id": 3, "text": "Deep blue backdrop..."}
    ],
    "image_url": "/uploads/result-uuid.jpg",
    "timestamp": "2024-01-15T10:30:05Z"
  }
]
```

### Таблица: payments
```python
id: UUID (PK)
user_id: Integer (FK → users.id, indexed)
yukassa_payment_id: String(100), unique, indexed
amount: Decimal(10, 2)
currency: String(3) (default='RUB')
status: Enum('pending', 'succeeded', 'canceled', 'refunded')
payment_type: Enum('subscription', 'credits', 'one_time')
tariff_id: String(50), nullable
tax_amount: Decimal(10, 2)  # НПД 4%
commission_amount: Decimal(10, 2)  # YuKassa 2.8%
net_amount: Decimal(10, 2)  # amount - tax - commission
credits_awarded: Integer, nullable
subscription_days: Integer, nullable
idempotency_key: String(100), unique
metadata: JSONB, nullable
created_at: DateTime
paid_at: DateTime, nullable
```

### Таблица: referrals
```python
id: Integer (PK)
referrer_id: Integer (FK → users.id, indexed)
referred_id: Integer (FK → users.id, unique)
referral_code: String(20), unique, indexed
is_active: Boolean (default=True)
is_rewarded: Boolean (default=False)
bonus_credits_earned: Integer (default=10)
created_at: DateTime
rewarded_at: DateTime, nullable
```

---

## 🔌 Интеграции (подробно)

### 1. kie.ai Nano Banana API
**Файл:** `backend/app/services/kie_ai.py`

**Конфигурация:**
- Base URL: `https://api.kie.ai`
- Model: `nano-banana`
- Timeout: 300 секунд (5 минут)
- Retry: 3 попытки, exponential backoff (1s, 2s, 4s)

**Методы:**
```python
async def try_on(user_photo: bytes, item_photo: bytes, zone: str) -> bytes:
    """
    Виртуальная примерка

    Args:
        user_photo: Фото пользователя (JPEG/PNG)
        item_photo: Фото одежды/аксессуара
        zone: 'head' | 'neck' | 'hands' | 'legs'

    Returns:
        bytes: Результирующее изображение

    Raises:
        KieAIError: При ошибке API
        TimeoutError: При превышении таймаута
    """

async def image_editing(base_image: bytes, prompt: str) -> bytes:
    """
    Редактирование изображения по промпту

    Args:
        base_image: Базовое изображение
        prompt: Промпт на английском (от OpenRouter)

    Returns:
        bytes: Отредактированное изображение
    """
```

**Фиксированный промпт для примерки:**
```python
FITTING_PROMPT = """
Virtual try-on of {item_type} on person.
Zone: {zone}
Ensure natural lighting, realistic fit, and proper perspective.
Maintain person's pose and background.
"""
```

### 2. OpenRouter Claude Haiku API
**Файл:** `backend/app/services/openrouter.py`

**Конфигурация:**
- Base URL: `https://openrouter.ai/api/v1`
- Model: `anthropic/claude-3-haiku-20240307`
- Max tokens: 1000
- Temperature: 0.7
- Retry: 3 попытки

**Метод:**
```python
async def generate_prompt_variants(
    user_request: str,
    chat_history: List[Dict[str, str]],
    image_description: Optional[str] = None
) -> List[str]:
    """
    Генерация 3 вариантов промптов для редактирования

    Args:
        user_request: Запрос пользователя на русском
        chat_history: Последние 10 сообщений (role, content)
        image_description: Опционально - описание изображения

    Returns:
        List[str]: 3 промпта на английском для kie.ai

    Пример ответа:
    [
        "Change background to blue sky with clouds",
        "Replace backdrop with azure gradient",
        "Add deep blue background with soft lighting"
    ]
    """
```

**Системный промпт:**
```
You are an AI assistant for image editing.
User will describe desired changes in Russian.
Generate 3 prompt variants in English for image generation API.
Prompts should be:
- Clear and specific
- In English
- Suitable for Stable Diffusion
- Different but related
Return as JSON array of strings.
```

**Контекст чата:**
- Отправляются только последние 10 сообщений
- Структура: `[{role: 'user'|'assistant', content: str}]`
- Учитываются input/output токены для статистики

### 3. ЮKassa Payment API
**Файл:** `backend/app/services/yukassa.py`

**Конфигурация:**
- Base URL: `https://api.yookassa.ru/v3`
- Authentication: Basic Auth (Shop ID + Secret Key)
- Webhook URL: `https://your-domain.com/api/v1/payments/webhook`

**Методы:**
```python
async def create_payment(
    amount: Decimal,
    description: str,
    metadata: Dict[str, Any],
    return_url: str
) -> Dict[str, Any]:
    """
    Создание платежа

    Returns:
        {
            'id': 'payment_id',
            'status': 'pending',
            'confirmation': {
                'type': 'redirect',
                'confirmation_url': 'https://yoomoney.ru/checkout/...'
            }
        }
    """

async def verify_webhook(
    signature: str,
    body: bytes
) -> bool:
    """
    Проверка подписи webhook через HMAC SHA-256

    Args:
        signature: Заголовок X-YooKassa-Signature
        body: Raw request body

    Returns:
        bool: True если подпись валидна
    """
```

**Webhook обработка:**
```python
# POST /api/v1/payments/webhook
1. Verify HMAC signature
2. Parse event: payment.succeeded, payment.canceled, refund.succeeded
3. Check idempotency_key (prevent double crediting)
4. Calculate tax (4%) + commission (2.8%)
5. Add credits to user.balance_credits
6. Update payment.status = 'succeeded'
7. Send Telegram notification
```

**Расчёт налогов (НПД):**
```python
amount = 299.00  # Подписка Basic
tax_rate = 0.04  # НПД 4%
commission_rate = 0.028  # YuKassa 2.8%

tax_amount = amount * tax_rate  # 11.96
commission_amount = amount * commission_rate  # 8.37
net_amount = amount - tax_amount - commission_amount  # 278.67
```

---

## ⚙️ Переменные окружения (критичные)

**Обязательные для работы:**
```bash
# Telegram
TELEGRAM_BOT_TOKEN=123456:ABC...  # От @BotFather

# kie.ai
KIE_AI_API_KEY=sk-...  # API ключ kie.ai
KIE_AI_BASE_URL=https://api.kie.ai

# OpenRouter
OPENROUTER_API_KEY=sk-or-...  # API ключ OpenRouter
OPENROUTER_MODEL=anthropic/claude-3-haiku-20240307

# YuKassa
YUKASSA_SHOP_ID=123456
YUKASSA_SECRET_KEY=test_...  # Secret key

# Security
JWT_SECRET_KEY=random_64_char_string  # Для JWT токенов
SECRET_KEY=random_64_char_string  # Для HMAC
ADMIN_SECRET_KEY=random_32_char_string  # Для админ-панели

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/ai_bot

# Redis
REDIS_URL=redis://localhost:6379/0

# URLs
FRONTEND_URL=http://localhost:5173  # CORS + payment return URL
WEB_APP_URL=https://your-bot.t.me/app  # Telegram WebApp URL
BACKEND_URL=http://localhost:8000
```

**Файл:** `.env.example` — полный список из 40+ переменных

---

## 🔒 Безопасность (важные детали)

### Авторизация через Telegram
```python
# backend/app/core/security.py:validate_telegram_init_data()

1. Получить initData от Telegram WebApp
2. Распарсить query string
3. Извлечь hash
4. Создать data_check_string (sorted key=value pairs)
5. secret_key = HMAC-SHA256(BOT_TOKEN, "WebAppData")
6. data_hash = HMAC-SHA256(secret_key, data_check_string)
7. Compare: data_hash == hash (constant-time comparison)
8. Check timestamp (не старше 24 часов)
```

### Валидация файлов
```python
# backend/app/services/file_validator.py

1. Check extension: .jpg, .jpeg, .png
2. Check MIME type: image/jpeg, image/png
3. Check magic bytes (первые 8 байт файла):
   - JPEG: FF D8 FF
   - PNG: 89 50 4E 47 0D 0A 1A 0A
4. Check size: ≤ 5MB (5 * 1024 * 1024 bytes)
5. Generate UUID filename (prevent path traversal)
```

### Rate Limiting
**Файл:** `backend/app/core/config.py`
```python
RATE_LIMIT_PER_MINUTE = 10  # requests per user per minute
```

---

## 📊 Мониторинг и логирование

### Sentry Integration
```python
# backend/app/main.py
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        traces_sample_rate=0.1
    )
```

### Логирование
```python
# backend/app/core/config.py
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
```

**Логи идут в:**
- Консоль (stdout)
- Sentry (errors only)
- Docker logs: `docker-compose logs -f backend`

---

## 🧪 Тестирование (детали)

### Backend Test Structure
```
backend/tests/
├── conftest.py              # Fixtures: test_db, test_client, test_user
├── test_auth.py             # Telegram validation, JWT (8 tests)
├── test_credits.py          # Credit logic (10 tests)
├── test_file_validator.py   # MIME validation (10 tests)
├── test_tax.py              # Tax calculations (24 tests, 23 passed)
├── test_editing_module.py   # OpenRouter, chat (14 tests, all passed)
├── test_api_integration.py  # API endpoints (24 tests, skipped - need test DB)
└── pytest.ini               # Markers: unit, integration, slow
```

**Запуск:**
```bash
pytest tests/ -v --cov=app           # Все тесты
pytest -m unit                       # Только unit тесты
pytest -m integration                # Только integration
pytest tests/test_auth.py::test_telegram_validation -v  # Конкретный тест
```

### Test DB Setup
```bash
./backend/tests/create_test_db.sh
# Creates: ai_bot_test database
# Runs: alembic upgrade head
```

---

## 🎭 ОБЯЗАТЕЛЬНОЕ ИСПОЛЬЗОВАНИЕ MCP PLAYWRIGHT ДЛЯ ТЕСТИРОВАНИЯ ФРОНТЕНДА

**⚠️ КРИТИЧЕСКИ ВАЖНО:** При тестировании фронтенда ОБЯЗАТЕЛЬНО использовать MCP Playwright для автоматического тестирования в реальном браузере!

### Зачем нужен Playwright MCP?

Playwright MCP позволяет Claude Code:
- **Автоматически открывать** приложение в браузере
- **Видеть** что отображается на экране (скриншоты)
- **Читать** консоль браузера и перехватывать ошибки
- **Взаимодействовать** с элементами (клики, ввод текста)
- **Проверять** localStorage, cookies, network requests
- **Тестировать** весь UI flow от авторизации до генерации

### Когда ОБЯЗАТЕЛЬНО использовать Playwright MCP:

1. **При тестировании новых компонентов/страниц:**
   - После создания HomePage, FittingPage, EditingPage
   - После изменения AuthGuard, роутинга, navigation
   - После изменения UI/UX (кнопки, формы, модальные окна)

2. **При исправлении багов:**
   - Ошибки в консоли браузера
   - Проблемы с авторизацией
   - Проблемы с localStorage/sessionStorage
   - Некорректное отображение компонентов
   - Проблемы с навигацией

3. **При интеграционном тестировании:**
   - Проверка flow примерки (upload → generate → result)
   - Проверка flow редактирования (upload → chat → generate)
   - Проверка flow оплаты
   - Проверка реферальной системы

4. **При DEV режиме:**
   - Проверка что mock данные загружаются корректно
   - Проверка что приложение работает без Telegram

### Доступные MCP Playwright инструменты:

**После перезапуска Claude Desktop будут доступны:**

- `mcp__playwright__navigate` — Открыть URL в браузере
- `mcp__playwright__screenshot` — Сделать скриншот страницы
- `mcp__playwright__click` — Клик по элементу
- `mcp__playwright__fill` — Заполнить форму
- `mcp__playwright__console` — Читать консоль браузера
- `mcp__playwright__evaluate` — Выполнить JavaScript в контексте страницы

### Workflow тестирования фронтенда с Playwright:

#### Шаг 1: Запуск dev сервера (если не запущен)
```bash
cd frontend
npm run dev  # Запуск на http://localhost:5173
```

#### Шаг 2: Открыть приложение в браузере через Playwright
```
ИСПОЛЬЗОВАТЬ: mcp__playwright__navigate
URL: http://localhost:5173
```

#### Шаг 3: Сделать скриншот для анализа
```
ИСПОЛЬЗОВАТЬ: mcp__playwright__screenshot
```

#### Шаг 4: Проверить консоль на ошибки
```
ИСПОЛЬЗОВАТЬ: mcp__playwright__console
```

#### Шаг 5: Проверить localStorage/состояние
```
ИСПОЛЬЗОВАТЬ: mcp__playwright__evaluate
CODE:
  const auth = localStorage.getItem('auth-storage');
  const parsed = auth ? JSON.parse(auth) : null;
  return {
    isAuthenticated: parsed?.state?.isAuthenticated,
    user: parsed?.state?.user,
    token: parsed?.state?.token
  };
```

#### Шаг 6: Взаимодействие с элементами
```
ИСПОЛЬЗОВАТЬ: mcp__playwright__click
SELECTOR: button:has-text("Примерка")
```

### Примеры обязательного использования:

#### Пример 1: Тестирование HomePage после изменений

**Задача:** Проверить что новый дизайн HomePage корректно отображается

**Правильный подход:**
```
1. Запустить dev сервер (если не запущен): npm run dev
2. ИСПОЛЬЗОВАТЬ mcp__playwright__navigate → http://localhost:5173
3. ИСПОЛЬЗОВАТЬ mcp__playwright__screenshot → Анализировать скриншот
4. ИСПОЛЬЗОВАТЬ mcp__playwright__console → Проверить ошибки
5. ИСПОЛЬЗОВАТЬ mcp__playwright__evaluate → Проверить localStorage
6. ИСПОЛЬЗОВАТЬ mcp__playwright__click → Проверить кнопки "Примерка" и "Редактирование"
7. Если найдены ошибки → исправить → повторить тест
```

#### Пример 2: Диагностика ошибки "Something went wrong"

**Задача:** Пользователь сообщил об ошибке при открытии приложения

**Правильный подход:**
```
1. ИСПОЛЬЗОВАТЬ mcp__playwright__navigate → http://localhost:5173
2. ИСПОЛЬЗОВАТЬ mcp__playwright__screenshot → Увидеть ЧТО отображается
3. ИСПОЛЬЗОВАТЬ mcp__playwright__console → Прочитать ошибки
4. ИСПОЛЬЗОВАТЬ mcp__playwright__evaluate → Проверить:
   - window.location.href
   - localStorage['auth-storage']
   - Telegram.WebApp доступен?
   - import.meta.env.DEV
5. Определить root cause
6. Исправить код
7. ПОВТОРИТЬ тест чтобы убедиться что исправление работает
```

#### Пример 3: Тестирование flow примерки

**Задача:** Проверить что весь процесс примерки работает корректно

**Правильный подход:**
```
1. ИСПОЛЬЗОВАТЬ mcp__playwright__navigate → http://localhost:5173
2. ИСПОЛЬЗОВАТЬ mcp__playwright__click → Кнопка "Примерка"
3. ИСПОЛЬЗОВАТЬ mcp__playwright__screenshot → Проверить что открылся FittingPage
4. ИСПОЛЬЗОВАТЬ mcp__playwright__fill → Загрузить тестовое фото (если есть input)
5. ИСПОЛЬЗОВАТЬ mcp__playwright__click → Кнопка "Далее"
6. ИСПОЛЬЗОВАТЬ mcp__playwright__screenshot → Проверить второй шаг
7. Проверить каждый шаг wizard
8. ИСПОЛЬЗОВАТЬ mcp__playwright__console → Проверить ошибки API
```

#### Пример 4: Проверка навигации и роутинга

**Задача:** Убедиться что навигация между страницами работает

**Правильный подход:**
```
1. ИСПОЛЬЗОВАТЬ mcp__playwright__navigate → http://localhost:5173
2. ИСПОЛЬЗОВАТЬ mcp__playwright__screenshot → HomePage
3. ИСПОЛЬЗОВАТЬ mcp__playwright__click → Гамбургер меню
4. ИСПОЛЬЗОВАТЬ mcp__playwright__screenshot → Меню открылось?
5. ИСПОЛЬЗОВАТЬ mcp__playwright__click → "Профиль"
6. ИСПОЛЬЗОВАТЬ mcp__playwright__screenshot → ProfilePage открылся?
7. ИСПОЛЬЗОВАТЬ mcp__playwright__evaluate → window.location.pathname === '/profile'
```

### ❌ ЗАПРЕЩЕНО:

1. **Тестировать фронтенд БЕЗ Playwright:**
   - НЕ полагаться только на чтение кода
   - НЕ предполагать что код работает без проверки в браузере
   - НЕ просить пользователя вручную проверять каждое изменение

2. **Исправлять баги "вслепую":**
   - НЕ исправлять ошибки без предварительной диагностики через Playwright
   - НЕ делать предположения о причине ошибки без консоли браузера

3. **Пропускать тестирование:**
   - НЕ считать задачу завершённой без проверки через Playwright
   - НЕ переходить к следующему этапу пока не убедишься что текущий работает

### ✅ ПРАВИЛЬНО:

1. **ВСЕГДА тестировать изменения через Playwright сразу после их внесения**
2. **Делать скриншоты ДО и ПОСЛЕ изменений для сравнения**
3. **Проверять консоль браузера на каждом этапе**
4. **Сохранять скриншоты критических моментов для документации**
5. **Повторять тесты после исправления багов чтобы убедиться что всё работает**

### Алгоритм работы при получении задачи на фронтенд:

```
1. Получить задачу от пользователя
2. Проанализировать какие компоненты/страницы затронуты
3. Запросить актуальную документацию через context7 (если нужно)
4. Внести изменения в код
5. ⚠️ ОБЯЗАТЕЛЬНО: Протестировать через Playwright:
   a. Navigate → URL
   b. Screenshot → Анализ
   c. Console → Проверка ошибок
   d. Evaluate → Проверка состояния
   e. Click/Fill → Проверка интерактивности
6. Если нашли проблемы → исправить → повторить тест
7. Только после успешного теста → сообщить пользователю о завершении
```

### Важные URL для тестирования:

```
Основное приложение:
http://localhost:5173/

Страницы:
http://localhost:5173/               # HomePage
http://localhost:5173/fitting        # FittingPage
http://localhost:5173/editing        # EditingPage
http://localhost:5173/profile        # ProfilePage
http://localhost:5173/admin          # AdminPage

Диагностика:
file:///путь/к/проекту/frontend/debug.html        # Debug page
file:///путь/к/проекту/frontend/clear-storage.html # Clear storage
```

### Команды для запуска dev сервера:

```bash
# Если dev сервер НЕ запущен:
cd frontend
npm run dev

# Проверить что сервер работает:
curl http://localhost:5173

# Проверить логи dev сервера:
# Смотреть вывод в терминале где запущен npm run dev
```

### Интеграция с TODO.md:

**ПОСЛЕ тестирования каждого этапа через Playwright:**

1. Добавить в TODO.md секцию "Тестирование"
2. Указать какие тесты были выполнены
3. Прикрепить ссылки на скриншоты (если сохранены)
4. Отметить все пройденные тест-кейсы

**Шаблон для TODO.md:**
```markdown
### Тестирование через Playwright

✅ **HomePage:**
- [x] Отображение корректного дизайна
- [x] Кнопки "Примерка" и "Редактирование" работают
- [x] Гамбургер меню открывается
- [x] Отображение баланса и подписки
- [x] Консоль без ошибок

✅ **AuthGuard:**
- [x] DEV режим работает (mock данные загружаются)
- [x] localStorage содержит корректные данные
- [x] Редирект не происходит без Telegram в DEV режиме

⏳ **FittingPage:**
- [ ] Step wizard корректно отображается
- [ ] Загрузка фото работает
- [ ] Навигация между шагами
```

**⚠️ Эти правила ОБЯЗАТЕЛЬНЫ и имеют приоритет наравне с правилами использования context7!**

**Без тестирования через Playwright задача НЕ считается выполненной!**

---

## 🚨 Известные ограничения

1. **Нет миграций Alembic:** `backend/alembic/versions/` пуст (только .gitkeep)
   - Нужно создать: `alembic revision --autogenerate -m "initial"`

2. **WebSocket не реализован:** используется polling для статуса генераций
   - TODO: Заменить на WebSocket для real-time updates

3. **Rate limiting не работает:** настроен в config, но middleware не подключен
   - TODO: Добавить slowapi middleware

4. **Health checks mock:** `/health` возвращает `{"status": "ok"}` без проверки DB/Redis
   - TODO: Реальная проверка подключений

5. **Нет автобэкапа БД:** только ручные команды
   - TODO: Cronjob для pg_dump

6. **Integration tests skipped:** требуют test DB setup
   - TODO: Запустить create_test_db.sh и unskip тесты

---

## 📚 Дополнительная документация

- **README.md** — Quick start, tech stack, features (335 lines)
- **TODO.md** — Detailed roadmap, 15 stages, progress tracking (1248 lines)
- **CODE_RULES.md** — Code quality rules, error fixing process (118 lines)
- **AGENTS.md** — Agent configuration, specialized agents (118 lines)
- **backend/CLAUDE.md** — Backend architecture details (265 lines)
- **telegram_bot/README.md** — Bot setup guide (293 lines)
- **docs/deployment/** — VPS deployment guides (DEPLOY.md, NGINX_SETUP.md)
- **docs/development/** — Testing guides (TESTING.md, OPTIMIZATION.md)

---

## 📞 Поддержка

Swagger UI: http://localhost:8000/docs — интерактивная документация API
