# VK OAuth Setup Guide

Руководство по настройке VK ID OAuth для авторизации пользователей через VK.com.

## Оглавление
1. [Создание VK Mini App](#1-создание-vk-mini-app)
2. [Настройка Backend](#2-настройка-backend)
3. [Настройка Frontend](#3-настройка-frontend)
4. [Тестирование](#4-тестирование)
5. [Production Deployment](#5-production-deployment)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. Создание VK Mini App

### Шаг 1.1: Создайте приложение в VK Developers
1. Перейдите на [VK Developers](https://dev.vk.com/)
2. Нажмите **"Создать приложение"**
3. Выберите **"Mini App"** или **"Standalone"**
4. Заполните форму:
   - **Название**: AI Image Generator (или ваше название)
   - **Платформа**: Выберите "Website" или "Standalone"
   - **Категория**: Развлечения / Утилиты

### Шаг 1.2: Получите App ID и Service Key
1. После создания приложения перейдите в **"Настройки"**
2. Скопируйте **App ID** (например, `51234567`)
3. Перейдите в **"Ключи доступа"** (Access Tokens)
4. Создайте **Service Key** (секретный ключ для backend)
   - Выберите права доступа: `email` (минимум)
   - Скопируйте **Service Key** (начинается с `vk1.a...`)

### Шаг 1.3: Настройте Redirect URI
1. В разделе **"Настройки"** → **"Redirect URI"**
2. Добавьте разрешенные URL:
   - **Development**: `http://localhost:5173` (или ваш dev URL)
   - **Production**: `https://yourdomain.com`

### Шаг 1.4: Настройте Trusted Domains
1. В разделе **"Настройки"** → **"Доверенные домены"**
2. Добавьте домены:
   - `localhost` (для разработки)
   - `yourdomain.com` (для production)

---

## 2. Настройка Backend

### Шаг 2.1: Добавьте переменные окружения
Отредактируйте файл **`backend/.env`**:

```env
# VK OAuth Configuration
VK_APP_ID=51234567
VK_SERVICE_KEY=vk1.a.your-service-key-here
```

Пример `.env.example` уже обновлен с этими переменными.

### Шаг 2.2: Проверьте backend код
Backend уже настроен и включает:

- **`backend/app/utils/vk_oauth.py`**: Утилита для проверки VK silent token
- **`backend/app/api/v1/endpoints/auth_web.py`**: Endpoint `/api/v1/auth-web/vk`
- **`backend/app/models/user.py`**: Добавлен `AuthProvider.VK`
- **`backend/alembic/versions/20251126_1500_add_vk_auth_provider.py`**: Миграция БД

### Шаг 2.3: Примените миграцию базы данных
```bash
cd backend
alembic upgrade head
```

### Шаг 2.4: Перезапустите backend
```bash
# Development
cd backend
uvicorn app.main:app --reload

# Production (Docker)
docker-compose -f docker-compose.prod.yml restart backend
```

---

## 3. Настройка Frontend

### Шаг 3.1: Добавьте переменные окружения
Отредактируйте файл **`frontend/.env`**:

```env
# VK OAuth (required for VK Sign-In)
VITE_VK_APP_ID=51234567
```

Пример `.env.example` уже обновлен.

### Шаг 3.2: Проверьте frontend код
Frontend уже настроен и включает:

- **`frontend/index.html`**: VK ID SDK script добавлен
- **`frontend/src/types/auth.ts`**: Типы для VK OAuth
- **`frontend/src/api/authWeb.ts`**: API client `loginWithVK()`
- **`frontend/src/store/authStore.ts`**: Store метод `loginWithVK()`
- **`frontend/src/components/auth/VKSignInButton.tsx`**: Компонент кнопки VK
- **`frontend/src/pages/LoginPage.tsx`**: Добавлена кнопка VK
- **`frontend/src/pages/RegisterPage.tsx`**: Добавлена кнопка VK

### Шаг 3.3: Установите зависимости (если еще не установлены)
```bash
cd frontend
npm install
```

### Шаг 3.4: Перезапустите frontend
```bash
# Development
cd frontend
npm run dev

# Production (Docker)
docker-compose -f docker-compose.prod.yml restart frontend
```

---

## 4. Тестирование

### Тест 1: Проверка загрузки VK SDK
1. Откройте браузер Dev Tools (F12)
2. Перейдите на страницу `/login` или `/register`
3. В консоли должно быть сообщение: `VK ID SDK loaded`
4. Проверьте, что `window.VKID` существует:
   ```javascript
   console.log(window.VKID); // должен вернуть объект
   ```

### Тест 2: Проверка кнопки VK ID
1. На странице `/login` или `/register` должна появиться кнопка VK
2. Кнопка должна иметь официальный дизайн VK ID
3. Если VK_APP_ID не настроен, должна появиться заглушка: "VK вход не настроен"

### Тест 3: Авторизация через VK
1. Нажмите на кнопку VK Sign-In
2. Должно открыться окно VK авторизации (или One Tap если пользователь уже авторизован в VK)
3. Разрешите доступ к данным
4. Проверьте:
   - Перенаправление на главную страницу `/`
   - Токен сохранен в localStorage (`auth-storage`)
   - Пользователь авторизован (можно проверить в Redux/Zustand DevTools)

### Тест 4: Backend endpoint
Проверьте через curl или Postman:

```bash
curl -X POST http://localhost:8000/api/v1/auth-web/vk \
  -H "Content-Type: application/json" \
  -d '{
    "token": "vk_silent_token_example",
    "uuid": "uuid_example"
  }'
```

Ожидаемый ответ:
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "user": { ... },
  "is_new_user": true
}
```

---

## 5. Production Deployment

### Шаг 5.1: Настройте environment variables
На production сервере (VPS) обновите `.env` файлы:

```bash
# Backend .env
VK_APP_ID=51234567
VK_SERVICE_KEY=vk1.a.your-production-service-key

# Frontend .env
VITE_VK_APP_ID=51234567
```

### Шаг 5.2: Обновите VK App настройки
В VK Developers:
1. Добавьте production redirect URL: `https://yourdomain.com`
2. Добавьте production домен в trusted domains

### Шаг 5.3: Deploy
```bash
# На VPS
cd /root/ai-media-generator
./vps-deploy-script.sh
```

---

## 6. Troubleshooting

### Проблема: "VK вход не настроен"
**Причина**: VITE_VK_APP_ID не установлен или не загружен в runtime
**Решение**:
1. Проверьте `.env` файл в `frontend/`
2. Перезапустите dev server: `npm run dev`
3. Проверьте что переменная загружается:
   ```javascript
   console.log(import.meta.env.VITE_VK_APP_ID);
   ```

### Проблема: "VK ID SDK не загружается"
**Причина**: Скрипт заблокирован ad-blocker или проблемы с сетью
**Решение**:
1. Отключите ad-blocker для localhost
2. Проверьте Network tab в DevTools
3. Убедитесь что CDN доступен: `https://unpkg.com/@vkid/sdk@latest/dist/index.min.js`

### Проблема: "Invalid VK token" на backend
**Причина**: VK_SERVICE_KEY неверный или expired
**Решение**:
1. Проверьте VK_SERVICE_KEY в `backend/.env`
2. Создайте новый Service Key в VK Developers
3. Убедитесь что Service Key имеет права доступа `email`

### Проблема: "Redirect URI mismatch"
**Причина**: URL не совпадает с настройками в VK App
**Решение**:
1. В VK Developers проверьте Redirect URI
2. Убедитесь что `window.location.origin` совпадает с настроенным URL
3. Для localhost используйте `http://localhost:5173` (с портом)

### Проблема: Silent token verification failed
**Причина**: Token невалиден или истек
**Решение**:
1. Проверьте backend logs: `docker-compose logs backend`
2. Убедитесь что VK API доступен (проверьте VK service status)
3. Попробуйте создать новую авторизацию

---

## Дополнительные ресурсы

- [VK ID SDK Documentation](https://id.vk.com/about/business/go/docs/en/vkid/latest/vk-id/intro/plan)
- [VK Developers Portal](https://dev.vk.com/)
- [VK ID SDK GitHub](https://github.com/VKCOM/vkid-js-sdk)

---

**Версия**: 1.0
**Дата создания**: 2025-11-26
**Автор**: AI Media Generator Team
