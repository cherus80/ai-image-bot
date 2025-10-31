# Руководство по тестированию AI Image Generator Bot

Этот документ содержит инструкции по запуску и написанию тестов для проекта.

---

## Содержание

1. [Структура тестов](#структура-тестов)
2. [Backend тестирование](#backend-тестирование)
3. [Frontend тестирование](#frontend-тестирование)
4. [E2E тестирование](#e2e-тестирование)
5. [Continuous Integration](#continuous-integration)
6. [Написание новых тестов](#написание-новых-тестов)

---

## Структура тестов

```
project/
├── backend/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py           # Pytest фикстуры
│   │   ├── test_auth.py          # Тесты авторизации
│   │   ├── test_credits.py       # Тесты кредитов
│   │   ├── test_file_validator.py # Тесты валидации файлов
│   │   ├── test_tax.py           # Тесты налогов
│   │   ├── test_editing_module.py # Тесты редактирования
│   │   └── test_api_integration.py # Integration тесты API
│   └── pytest.ini               # Конфигурация pytest
├── frontend/
│   ├── src/
│   │   └── __tests__/           # Frontend тесты
│   └── jest.config.js           # Конфигурация Jest
├── e2e/
│   └── tests/                   # E2E тесты Playwright
└── TESTING.md                   # Этот файл
```

---

## Backend тестирование

### Установка зависимостей

Все зависимости для тестирования уже включены в `requirements.txt`:

```bash
cd backend
pip install -r requirements.txt
```

Основные зависимости для тестирования:
- `pytest==7.4.4` — фреймворк для тестирования
- `pytest-asyncio==0.23.3` — поддержка async тестов
- `pytest-cov==4.1.0` — покрытие кода
- `httpx` — HTTP клиент для тестирования API

### Запуск тестов

#### Все тесты

```bash
cd backend
pytest
```

#### Только unit-тесты

```bash
pytest -m unit
```

#### Только integration-тесты

```bash
pytest -m integration
```

#### Конкретный файл

```bash
pytest tests/test_auth.py
```

#### Конкретный тест

```bash
pytest tests/test_auth.py::TestJWT::test_verify_token_valid
```

#### С подробным выводом

```bash
pytest -v
```

#### С покрытием кода

```bash
pytest --cov=app --cov-report=html
```

После выполнения откройте `htmlcov/index.html` для просмотра отчёта о покрытии.

### Существующие тесты

#### 1. Тесты авторизации (`test_auth.py`)

- **TestTelegramValidation**: Валидация Telegram initData
  - `test_validate_telegram_init_data_valid` — правильный initData
  - `test_validate_telegram_init_data_invalid_hash` — неправильная подпись
  - `test_validate_telegram_init_data_expired` — истёкший auth_date
  - `test_validate_telegram_init_data_missing_params` — отсутствуют параметры

- **TestJWT**: JWT токены
  - `test_create_access_token_default_expiry` — создание токена
  - `test_create_access_token_custom_expiry` — кастомный срок действия
  - `test_verify_token_valid` — верификация валидного токена
  - `test_verify_token_invalid` — верификация невалидного токена
  - `test_verify_token_expired` — истёкший токен

#### 2. Тесты кредитов (`test_credits.py`)

- **TestCheckUserCanPerformAction**: Проверка возможности действия
  - `test_user_with_credits` — пользователь с кредитами
  - `test_user_with_insufficient_credits` — недостаточно кредитов
  - `test_user_with_active_subscription` — активная подписка
  - `test_user_with_expired_subscription` — истёкшая подписка
  - `test_user_with_freemium_available` — доступен Freemium
  - `test_user_with_freemium_exhausted` — Freemium исчерпан

- **TestDeductCredits**: Списание кредитов
  - `test_deduct_from_balance_credits` — списание с баланса
  - `test_deduct_from_subscription` — списание с подписки
  - `test_deduct_from_freemium` — списание с Freemium
  - `test_deduct_insufficient_credits` — недостаточно средств

- **TestAwardCredits**: Начисление кредитов
  - `test_award_credits_success` — успешное начисление

- **TestAwardSubscription**: Начисление подписки
  - `test_award_subscription_new` — новая подписка
  - `test_award_subscription_renewal` — продление подписки

#### 3. Тесты валидации файлов (`test_file_validator.py`)

- **TestValidateImageFile**: Валидация изображений
  - `test_valid_jpeg_file` — корректный JPEG
  - `test_valid_png_file` — корректный PNG
  - `test_invalid_mime_type` — неподдерживаемый MIME-тип
  - `test_file_too_large` — файл больше 5MB
  - `test_invalid_magic_bytes_jpeg` — неправильные magic bytes JPEG
  - `test_invalid_magic_bytes_png` — неправильные magic bytes PNG
  - `test_mime_type_mismatch` — несоответствие MIME-типа

- **TestGetFileExtension**: Получение расширения файла

- **TestGetImageDimensions**: Получение размеров изображения

#### 4. Тесты налогов (`test_tax.py`)

- **TestCalculateNPDTax**: Расчёт НПД (4%)
  - `test_npd_tax_integer_amount` — целая сумма
  - `test_npd_tax_decimal_amount` — с копейками
  - `test_npd_tax_small_amount` — малая сумма
  - `test_npd_tax_zero` — нулевая сумма

- **TestCalculateYuKassaCommission**: Расчёт комиссии ЮKassa (2.8%)
  - `test_yukassa_commission_integer_amount` — целая сумма
  - `test_yukassa_commission_decimal_amount` — с копейками
  - `test_yukassa_commission_custom_rate` — кастомная ставка
  - `test_yukassa_commission_zero` — нулевая сумма

- **TestCalculateTotalDeductions**: Общие вычеты (НПД + комиссия)

- **TestCalculateNetAmount**: Чистая сумма (после вычетов)

- **TestCalculateGrossAmount**: Обратный расчёт

- **TestFormatTaxBreakdown**: Форматирование разбивки

- **TestRealWorldScenarios**: Реальные сценарии с тарифами
  - `test_subscription_basic_299` — базовая подписка 299₽
  - `test_subscription_standard_499` — стандартная подписка 499₽
  - `test_subscription_premium_899` — премиум подписка 899₽
  - `test_credits_package_199` — пакет кредитов 199₽
  - `test_profit_margin_basic_subscription` — чистая прибыль

#### 5. Тесты редактирования (`test_editing_module.py`)

Полный набор unit-тестов для модуля редактирования изображений (14 тестов).

#### 6. Integration тесты (`test_api_integration.py`)

**Примечание**: Эти тесты требуют настройки тестовой БД и помечены как `skip`.

- **TestAuthAPIIntegration**: Auth API
- **TestFittingAPIIntegration**: Fitting API
- **TestEditingAPIIntegration**: Editing API
- **TestPaymentsAPIIntegration**: Payments API
- **TestReferralsAPIIntegration**: Referrals API
- **TestAdminAPIIntegration**: Admin API

### Настройка тестовой БД

**TODO**: Инструкции по настройке тестовой PostgreSQL БД для integration тестов.

```bash
# Создать тестовую БД
createdb ai_image_generator_test

# Применить миграции
cd backend
alembic upgrade head
```

---

## Frontend тестирование

### Установка зависимостей

**TODO**: Настройка Jest и React Testing Library для frontend.

```bash
cd frontend
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event jest
```

### Запуск тестов

```bash
cd frontend
npm test
```

### Структура тестов

**TODO**: Создать тесты для критических компонентов:

- `src/__tests__/components/auth/AuthGuard.test.tsx`
- `src/__tests__/components/fitting/FittingWizard.test.tsx`
- `src/__tests__/store/authStore.test.ts`
- `src/__tests__/api/auth.test.ts`

---

## E2E тестирование

### Установка Playwright

```bash
npm init playwright@latest
```

### Запуск E2E тестов

```bash
npx playwright test
```

### Планируемые E2E сценарии

**TODO**: Создать E2E тесты для:

1. **Полный flow авторизации**:
   - Открыть Web App из Telegram
   - Автоматическая авторизация
   - Проверка профиля

2. **Полный flow примерки**:
   - Загрузка фото пользователя
   - Загрузка фото одежды
   - Выбор зоны
   - Запуск генерации
   - Ожидание результата
   - Просмотр результата

3. **Полный flow редактирования**:
   - Загрузка базового изображения
   - Отправка сообщения AI
   - Выбор промпта
   - Генерация
   - Просмотр результата

4. **Полный flow оплаты**:
   - Выбор тарифа
   - Создание платежа
   - Редирект на ЮKassa (mock)
   - Возврат и начисление кредитов

---

## Continuous Integration

### GitHub Actions

**TODO**: Создать `.github/workflows/test.yml` для автоматического запуска тестов при push и PR.

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r backend/requirements.txt
      - run: cd backend && pytest

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm install
      - run: cd frontend && npm test
```

---

## Написание новых тестов

### Правила написания тестов

1. **Один тест = одна проверка**
   - Каждый тест должен проверять одну конкретную вещь

2. **Понятные названия тестов**
   ```python
   def test_user_can_login_with_valid_credentials():
       # Хорошо: понятно, что тестируем
       pass

   def test_login():
       # Плохо: непонятно, что именно тестируем
       pass
   ```

3. **AAA паттерн**
   - **Arrange**: Подготовка данных
   - **Act**: Выполнение действия
   - **Assert**: Проверка результата

   ```python
   def test_award_credits_success():
       # Arrange
       user = create_test_user(balance=10)

       # Act
       result = await award_credits(user, amount=50)

       # Assert
       assert result["success"] is True
       assert user.balance_credits == 60
   ```

4. **Изоляция тестов**
   - Каждый тест должен быть независимым
   - Не полагайтесь на порядок выполнения тестов

5. **Использование фикстур**
   ```python
   @pytest.fixture
   async def test_user():
       """Создать тестового пользователя"""
       user = User(
           telegram_id=123456,
           username="testuser",
           balance_credits=10
       )
       return user
   ```

6. **Тестирование граничных случаев**
   - Проверяйте не только "happy path", но и:
     - Пустые значения
     - Некорректные данные
     - Граничные значения
     - Ошибки

### Примеры написания тестов

#### Unit тест для функции

```python
def test_calculate_npd_tax_standard():
    """Расчёт НПД для стандартной суммы"""
    result = calculate_npd_tax(1000)

    assert result == Decimal("40.00")
```

#### Async тест для сервиса

```python
@pytest.mark.asyncio
async def test_deduct_credits_success():
    """Успешное списание кредитов"""
    # Arrange
    user = Mock(spec=User)
    user.balance_credits = 10
    db_mock = AsyncMock()

    # Act
    result = await deduct_credits(db_mock, user, cost=3)

    # Assert
    assert result["success"] is True
    assert user.balance_credits == 7
    db_mock.commit.assert_called_once()
```

#### Integration тест для API

```python
@pytest.mark.asyncio
async def test_auth_endpoint(client: AsyncClient):
    """Тест авторизации через API"""
    # Arrange
    init_data = create_valid_init_data()

    # Act
    response = await client.post(
        "/api/v1/auth/telegram",
        json={"init_data": init_data}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "user" in data
```

---

## Метрики покрытия кода

### Цели покрытия

- **Unit тесты**: ≥80% покрытие критических модулей
- **Integration тесты**: Все основные API endpoints
- **E2E тесты**: Все основные user flows

### Приоритеты тестирования

1. **Критично (должно быть 100% покрытие)**:
   - Авторизация и безопасность
   - Управление кредитами и платежами
   - Валидация файлов

2. **Высокий приоритет (≥90% покрытие)**:
   - API endpoints
   - Celery задачи
   - Интеграции с внешними API

3. **Средний приоритет (≥70% покрытие)**:
   - UI компоненты
   - Вспомогательные функции

---

## Текущее состояние тестирования

### ✅ Реализовано

1. **Backend Unit тесты**:
   - ✅ `test_auth.py` — авторизация (8 тестов)
   - ✅ `test_credits.py` — кредиты (10+ тестов)
   - ✅ `test_file_validator.py` — валидация файлов (10+ тестов)
   - ✅ `test_tax.py` — налоги (18 тестов)
   - ✅ `test_editing_module.py` — редактирование (14 тестов)
   - ✅ Конфигурация pytest (`pytest.ini`)

2. **Backend Integration тесты**:
   - ✅ `test_api_integration.py` — шаблоны для всех API endpoints (требуют настройку БД)

### ⏳ В процессе разработки

3. **Frontend тесты**:
   - ⏳ Настройка Jest + React Testing Library
   - ⏳ Тесты для критических компонентов
   - ⏳ Тесты для Zustand stores

4. **E2E тесты**:
   - ⏳ Настройка Playwright
   - ⏳ Основные user flows

5. **CI/CD**:
   - ⏳ GitHub Actions workflow

---

## Контакты и поддержка

Если у вас возникли вопросы по тестированию, обратитесь к:
- Backend тесты: `backend/tests/`
- Документация pytest: https://docs.pytest.org/
- Документация Jest: https://jestjs.io/
- Документация Playwright: https://playwright.dev/

---

**Последнее обновление**: 2025-10-30 (Этап 13)
