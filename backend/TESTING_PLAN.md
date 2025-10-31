# План тестирования и оптимизации — Этап 13

## Дата создания
30 октября 2025

## Цели этапа
1. **Unit-тестирование**: Покрыть все ключевые сервисы и утилиты тестами
2. **Integration тесты**: Проверить взаимодействие компонентов
3. **Оптимизация Backend**: Улучшить производительность БД и API
4. **Оптимизация Frontend**: Code splitting, lazy loading
5. **E2E тесты**: Полные user flows (опционально)

---

## 1. Текущее состояние тестирования

### ✅ Уже протестировано

**Модуль editing** (14 тестов):
- ✅ Pydantic схемы (3 теста)
- ✅ OpenRouter клиент (3 теста)
- ✅ Chat сервис (2 теста)
- ✅ ChatHistory модель (5 тестов)
- ✅ Импорты (1 тест)

**Telegram Bot** (5 тестов):
- ✅ Импорты модулей
- ✅ Создание экземпляра бота
- ✅ Методы бота
- ✅ Переменные окружения
- ✅ Скрипт запуска

**Итого**: 19 тестов

### ⏳ Требует тестирования

**Backend модули**:
- ⏳ Auth (telegram validation, JWT)
- ⏳ Fitting (file validation, storage, generation)
- ⏳ Credits (deduct, award, calculations)
- ⏳ Payments (YuKassa, billing, tax)
- ⏳ Referrals (code generation, registration)
- ⏳ Admin (stats, exports)
- ⏳ Watermark service

---

## 2. План Unit-тестов для Backend

### 2.1. Авторизация (app/utils/telegram.py, app/utils/jwt.py)

**Приоритет**: Высокий

**Файл**: `tests/test_auth.py`

**Тесты**:
```python
# Telegram validation
- test_validate_telegram_init_data_valid()
- test_validate_telegram_init_data_invalid_hash()
- test_validate_telegram_init_data_expired()
- test_validate_telegram_init_data_missing_fields()

# JWT
- test_create_access_token()
- test_verify_token_valid()
- test_verify_token_expired()
- test_verify_token_invalid()
```

### 2.2. File Validation & Storage (app/services/file_validator.py, app/services/file_storage.py)

**Приоритет**: Высокий

**Файл**: `tests/test_file_services.py`

**Тесты**:
```python
# File validator
- test_validate_image_file_valid_jpeg()
- test_validate_image_file_valid_png()
- test_validate_image_file_invalid_mime()
- test_validate_image_file_too_large()
- test_validate_image_file_invalid_magic_bytes()

# File storage
- test_save_upload_file()
- test_get_file_by_id()
- test_delete_file()
- test_delete_old_files()
```

### 2.3. Credits Management (app/services/credits.py)

**Приоритет**: Высокий

**Файл**: `tests/test_credits.py`

**Тесты**:
```python
- test_check_user_can_perform_action_with_credits()
- test_check_user_can_perform_action_with_subscription()
- test_check_user_can_perform_action_with_freemium()
- test_deduct_credits_success()
- test_deduct_credits_insufficient_balance()
- test_award_credits_idempotency()
- test_award_subscription()
```

### 2.4. Payments & Billing (app/services/yukassa.py, app/services/billing.py)

**Приоритет**: Средний

**Файл**: `tests/test_payments.py`

**Тесты**:
```python
# YuKassa
- test_yukassa_create_payment()
- test_yukassa_get_payment_info()
- test_yukassa_verify_webhook_signature_valid()
- test_yukassa_verify_webhook_signature_invalid()

# Billing
- test_calculate_credits_for_tariff()
- test_calculate_price_for_tariff()
- test_get_all_tariffs()

# Tax calculations
- test_calculate_npd_tax()
- test_calculate_yukassa_commission()
- test_calculate_net_amount()
```

### 2.5. Watermark Service (app/services/watermark.py)

**Приоритет**: Средний

**Файл**: `tests/test_watermark.py`

**Тесты**:
```python
- test_add_watermark_to_image()
- test_add_watermark_to_bytes()
- test_watermark_positions()
- test_watermark_transparency()
```

### 2.6. Referrals (app/api/v1/endpoints/referrals.py)

**Приоритет**: Низкий

**Файл**: `tests/test_referrals.py`

**Тесты**:
```python
- test_generate_referral_code_unique()
- test_register_referral_valid()
- test_register_referral_self_invite()
- test_register_referral_already_invited()
- test_get_referral_stats()
```

---

## 3. Конфигурация pytest

### 3.1. Создать pytest.ini

```ini
[pytest]
minversion = 7.0
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function

# Настройки покрытия
addopts =
    --verbose
    --strict-markers
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-report=xml
    --cov-fail-under=60

# Маркеры
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
    auth: Authentication tests
    payments: Payment tests
```

### 3.2. Создать conftest.py

```python
# Фикстуры для тестов
- mock_db_session()
- mock_redis_client()
- mock_openrouter_client()
- mock_yukassa_client()
- test_user()
- test_chat_session()
```

---

## 4. Оптимизация Backend

### 4.1. Индексы БД

**Проверить существующие индексы**:
```sql
SELECT tablename, indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
```

**Добавить недостающие индексы**:
```sql
-- Users
CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_users_referral_code ON users(referral_code);

-- Generations
CREATE INDEX IF NOT EXISTS idx_generations_user_id_created_at ON generations(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_generations_task_id ON generations(task_id);
CREATE INDEX IF NOT EXISTS idx_generations_status ON generations(status);

-- ChatHistory
CREATE INDEX IF NOT EXISTS idx_chat_history_user_id_created_at ON chat_history(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_chat_history_is_active ON chat_history(is_active);

-- Payments
CREATE INDEX IF NOT EXISTS idx_payments_user_id_created_at ON payments(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_payments_payment_id ON payments(payment_id);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);

-- Referrals
CREATE INDEX IF NOT EXISTS idx_referrals_referrer_id ON referrals(referrer_id);
CREATE INDEX IF NOT EXISTS idx_referrals_referred_id ON referrals(referred_id);
```

### 4.2. Оптимизация запросов

**N+1 проблемы**:
- Использовать `selectinload()` для related objects
- Добавить `lazy='selectin'` в relationships

**Пример**:
```python
# До
users = await session.execute(select(User))
for user in users:
    generations = user.generations  # N+1 query

# После
users = await session.execute(
    select(User).options(selectinload(User.generations))
)
```

### 4.3. Кэширование

**Redis кэш для частых запросов**:
- Тарифы (TTL: 1 час)
- Статистика админки (TTL: 5 минут)
- Реферальные ссылки (TTL: 24 часа)

### 4.4. Rate Limiting

**Настроить rate limiting для API**:
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/fitting/generate")
@limiter.limit("10/minute")
async def generate_fitting(...):
    ...
```

---

## 5. Оптимизация Frontend

### 5.1. Code Splitting

**React.lazy() для страниц**:
```typescript
const FittingPage = lazy(() => import('./pages/FittingPage'));
const EditingPage = lazy(() => import('./pages/EditingPage'));
const ProfilePage = lazy(() => import('./pages/ProfilePage'));
const AdminPage = lazy(() => import('./pages/AdminPage'));
```

### 5.2. Lazy Loading изображений

**Intersection Observer API**:
```typescript
<img loading="lazy" src={imageUrl} alt="..." />
```

### 5.3. Bundle Analysis

```bash
# Анализ размера бандла
npm run build -- --analyze

# Оптимизация
- Удалить неиспользуемые зависимости
- Tree-shaking для lodash (используйте lodash-es)
- Минификация изображений
```

---

## 6. E2E тесты (опционально)

### 6.1. Playwright setup

```bash
npm install -D @playwright/test
npx playwright install
```

### 6.2. Тест-кейсы

**User flows**:
1. Авторизация через Telegram
2. Загрузка фото → Примерка → Скачивание
3. Редактирование → Чат с AI → Генерация
4. Покупка подписки → Оплата → Проверка баланса
5. Реферальная программа → Приглашение → Получение бонуса

---

## 7. Метрики успеха

### 7.1. Покрытие тестами
- ✅ **Цель**: ≥60% coverage
- ⏳ **Текущее**: ~20% (только editing module)

### 7.2. Производительность Backend
- ✅ **Цель**: API response time <200ms (95th percentile)
- ⏳ **Текущее**: не измерено

### 7.3. Производительность Frontend
- ✅ **Цель**: First Contentful Paint <1.5s
- ✅ **Цель**: Time to Interactive <3s
- ⏳ **Текущее**: не измерено

### 7.4. Стабильность
- ✅ **Цель**: 0 критичных багов
- ✅ **Цель**: Все тесты проходят

---

## 8. Приоритизация работ

### Высокий приоритет (сделать обязательно)
1. ✅ Создать pytest.ini и conftest.py
2. ✅ Unit-тесты для auth (telegram, JWT)
3. ✅ Unit-тесты для file services
4. ✅ Unit-тесты для credits
5. ✅ Добавить индексы БД
6. ✅ Запустить все тесты и проверить coverage

### Средний приоритет (желательно сделать)
7. ⏳ Unit-тесты для payments
8. ⏳ Unit-тесты для watermark
9. ⏳ Оптимизация N+1 запросов
10. ⏳ Frontend code splitting

### Низкий приоритет (можно отложить)
11. ⏳ Unit-тесты для referrals
12. ⏳ E2E тесты (Playwright)
13. ⏳ Нагрузочное тестирование

---

## 9. Инструкции по запуску тестов

### Запуск всех тестов
```bash
cd backend
source venv/bin/activate  # или venv\Scripts\activate на Windows
pytest
```

### Запуск конкретного файла
```bash
pytest tests/test_auth.py -v
```

### Запуск с покрытием
```bash
pytest --cov=app --cov-report=html
# Открыть htmlcov/index.html в браузере
```

### Запуск только быстрых тестов
```bash
pytest -m "not slow"
```

---

## 10. Следующие шаги

1. ✅ Создать pytest.ini
2. ✅ Создать conftest.py с фикстурами
3. ✅ Написать тесты для auth модуля
4. ✅ Написать тесты для file services
5. ✅ Написать тесты для credits
6. ✅ Запустить все тесты
7. ✅ Проверить coverage
8. ✅ Добавить недостающие индексы в БД
9. ✅ Документировать результаты

---

**Ответственный**: AI Agent
**Дата начала**: 30 октября 2025
**Планируемая дата завершения**: 31 октября 2025
