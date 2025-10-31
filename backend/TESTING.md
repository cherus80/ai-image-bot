# Testing Guide — Backend

## Этап 2: Авторизация через Telegram

### Запуск сервера

```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

Сервер будет доступен по адресу: [http://localhost:8000](http://localhost:8000)

### Swagger UI

Откройте [http://localhost:8000/docs](http://localhost:8000/docs) для интерактивной документации API.

### Доступные эндпоинты

#### 1. POST /api/v1/auth/telegram

Авторизация через Telegram WebApp initData.

**Request:**
```json
{
  "init_data": "query_id=AAHd...&user=%7B%22id%22%3A123456789%2C%22first_name%22%3A%22John%22%7D&auth_date=1698765432&hash=abc123..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "telegram_id": 123456789,
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "language_code": null,
    "balance_credits": 0,
    "subscription_type": null,
    "subscription_expires_at": null,
    "freemium_actions_used": 0,
    "freemium_reset_at": "2025-10-29T00:00:00Z",
    "can_use_freemium": true,
    "is_premium": false,
    "is_blocked": false,
    "created_at": "2025-10-29T00:00:00Z",
    "last_activity_at": "2025-10-29T00:00:00Z",
    "referral_code": "789XYZABC",
    "referred_by_id": null
  }
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Invalid Telegram initData: Invalid hash signature"
}
```

#### 2. GET /api/v1/auth/me

Получение текущего профиля пользователя (требует авторизации).

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "telegram_id": 123456789,
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "balance_credits": 0,
    "subscription_type": null,
    "freemium_actions_used": 0,
    "can_use_freemium": true,
    ...
  }
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Invalid token: Signature has expired"
}
```

**Response (403 Forbidden):**
```json
{
  "detail": "User is banned"
}
```

### Тестирование через cURL

#### Авторизация

```bash
curl -X POST "http://localhost:8000/api/v1/auth/telegram" \
  -H "Content-Type: application/json" \
  -d '{
    "init_data": "YOUR_TELEGRAM_INIT_DATA_HERE"
  }'
```

#### Получение профиля

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### Получение валидного Telegram initData

Для тестирования вам потребуется валидный Telegram initData. Есть несколько способов его получить:

1. **Через Telegram WebApp SDK** (рекомендуется):
   - Создайте простой HTML файл с Telegram WebApp SDK
   - Используйте `window.Telegram.WebApp.initData`
   - Откройте его в Telegram через бота

2. **Через Bot API** (для разработки):
   - Используйте Telegram Bot API для создания тестового WebApp
   - Получите initData из запроса

3. **Временное решение для локальной разработки**:
   - Создайте тестового пользователя напрямую в БД
   - Используйте mock initData (⚠️ только для development!)

### Проверка работы БД

```bash
psql -U postgres -d ai_image_bot
```

```sql
-- Просмотр всех пользователей
SELECT id, telegram_id, username, balance_credits, created_at FROM users;

-- Проверка создания пользователя после авторизации
SELECT * FROM users WHERE telegram_id = 123456789;
```

### Логирование

Все запросы логируются в консоль. При ошибках вы увидите:

- 401 Unauthorized — невалидный initData или токен
- 403 Forbidden — пользователь заблокирован
- 500 Internal Server Error — ошибка сервера (проверьте БД)

### Следующие шаги

После успешного тестирования Backend авторизации:

1. ✅ Реализовать Frontend часть (Этап 2 — Frontend)
2. ✅ Создать unit-тесты для auth endpoints
3. ✅ Создать integration тесты
4. ✅ Перейти к Этапу 3: API для примерки одежды
