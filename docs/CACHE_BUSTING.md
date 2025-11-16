# 🔄 Решение проблемы кэширования Telegram WebApp

## Проблема

Telegram WebApp агрессивно кэширует статические файлы (HTML, JS, CSS), из-за чего пользователи не видят новые изменения после деплоя.

## Причины

1. **Telegram кэширует WebApp на стороне клиента** (iOS/Android/Desktop)
2. **Nginx кэширует статические файлы** на сервере (по умолчанию 1 год)
3. **Отсутствие версионирования файлов** (нет cache busting)

## Решение (3-уровневое)

### 1. ✅ Cache Busting в Vite (ГОТОВО)

**Файл:** `frontend/vite.config.ts`

Добавлено автоматическое версионирование файлов:
```typescript
build: {
  rollupOptions: {
    output: {
      entryFileNames: 'assets/[name].[hash].js',
      chunkFileNames: 'assets/[name].[hash].js',
      assetFileNames: 'assets/[name].[hash].[ext]'
    }
  }
}
```

**Результат:**
- `index.js` → `index.a1b2c3d4.js`
- `main.css` → `main.e5f6g7h8.css`

При каждой сборке генерируются новые хеши → файлы уникальны → нет кэша.

### 2. ✅ Правильное кэширование в Nginx (ГОТОВО)

**Файл:** `frontend/nginx.conf`

**НЕ кэшируем index.html:**
```nginx
location / {
    try_files $uri $uri/ /index.html;
    add_header Cache-Control "no-cache, no-store, must-revalidate";
    add_header Pragma "no-cache";
    add_header Expires "0";
}
```

**Агрессивно кэшируем файлы с хешами:**
```nginx
location ~* \.[0-9a-f]{8,}\.(js|css|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

**Короткое кэширование для файлов БЕЗ хешей:**
```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
    expires 1h;
    add_header Cache-Control "public, max-age=3600";
}
```

### 3. 🔄 Деплой с пересборкой

**Использовать скрипт:**
```bash
./redeploy-frontend.sh
```

**Что делает скрипт:**
1. Пересобирает фронтенд с новыми хешами
2. Пересобирает Docker образ БЕЗ кэша (`--no-cache`)
3. Перезапускает контейнер frontend
4. Проверяет статус

## 📋 Чек-лист деплоя новых изменений

1. **Внесли изменения в код**
   ```bash
   # Например, изменили HomePage.tsx
   ```

2. **Запустили скрипт деплоя**
   ```bash
   ./redeploy-frontend.sh
   ```

3. **Проверили что контейнер работает**
   ```bash
   docker ps | grep frontend
   docker logs ai-image-bot-frontend
   ```

4. **Очистили кэш Telegram на клиенте** (см. ниже)

## 🔍 Как проверить что изменения применились

### На сервере (VPS):

1. **Проверить что файлы с хешами созданы:**
   ```bash
   ls -la frontend/dist/assets/
   # Должны быть файлы типа: index.a1b2c3d4.js
   ```

2. **Проверить nginx headers:**
   ```bash
   curl -I https://your-domain.com/
   # Должен быть: Cache-Control: no-cache, no-store, must-revalidate

   curl -I https://your-domain.com/assets/index.a1b2c3d4.js
   # Должен быть: Cache-Control: public, immutable
   ```

3. **Проверить что контейнер использует новый образ:**
   ```bash
   docker images | grep frontend
   # Дата создания должна быть свежая
   ```

### На клиенте (Telegram):

#### iOS/Android:

1. **Метод 1: Принудительное закрытие Telegram**
   - Полностью закройте Telegram (свайп вверх/force close)
   - Подождите 5 секунд
   - Откройте снова
   - Откройте WebApp

2. **Метод 2: Очистка кэша Telegram**
   - iOS: Settings → Data and Storage → Storage Usage → Clear Cache
   - Android: Settings → Data and Storage → Storage Usage → Clear Cache

3. **Метод 3: Переустановка Telegram** (крайний случай)
   - Удалите Telegram
   - Переустановите из App Store/Google Play
   - Войдите в аккаунт
   - Откройте бота

#### Desktop (macOS/Windows/Linux):

1. **Метод 1: Очистка кэша**
   - macOS: `~/Library/Application Support/Telegram Desktop/tdata/user_data`
   - Windows: `%APPDATA%\Telegram Desktop\tdata\user_data`
   - Linux: `~/.local/share/TelegramDesktop/tdata/user_data`
   - Удалите папку `webview_cache`

2. **Метод 2: DevTools** (только Desktop)
   - Откройте WebApp
   - Правый клик → Inspect Element
   - Application → Clear Storage → Clear site data
   - Перезагрузите страницу (Cmd+R / Ctrl+R)

## 🚨 Что делать если изменения ВСЁ ЕЩЁ не видны

### 1. Проверить URL WebApp в BotFather

Telegram кэширует по URL. Если добавить query параметр, кэш сбросится:

```bash
# Было:
https://your-domain.com

# Стало:
https://your-domain.com?v=2
```

**Как изменить:**
1. Откройте @BotFather
2. /mybots → ваш бот → Edit Bot → Edit Bot WebApp URL
3. Добавьте `?v=2` (или `?v=3`, `?v=4` при следующих деплоях)

### 2. Проверить что index.html обновился

**На сервере:**
```bash
# Проверить содержимое index.html
curl https://your-domain.com/ | grep -o 'src="[^"]*\.js"'

# Должны быть файлы с хешами:
# src="/assets/index.a1b2c3d4.js"
```

**Если там старые файлы БЕЗ хешей:**
```bash
# Пересобрать фронтенд
cd frontend
npm run build

# Проверить что dist/index.html содержит хеши
cat dist/index.html | grep -o 'src="[^"]*\.js"'
```

### 3. Проверить nginx конфигурацию

```bash
# Зайти в контейнер
docker exec -it ai-image-bot-frontend sh

# Проверить nginx.conf
cat /etc/nginx/conf.d/default.conf

# Должно быть:
# location / {
#     add_header Cache-Control "no-cache, no-store, must-revalidate";
# }
```

### 4. Принудительная очистка кэша на сервере

```bash
# Остановить контейнер
docker-compose down frontend

# Удалить образ
docker rmi ai-image-bot-frontend

# Очистить Docker cache
docker system prune -af

# Пересобрать с нуля
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

## 📊 Мониторинг кэша

### Проверка headers в production:

```bash
# index.html (должен быть no-cache)
curl -I https://your-domain.com/

# JS с хешом (должен быть immutable, 1 год)
curl -I https://your-domain.com/assets/index.a1b2c3d4.js

# Изображение БЕЗ хеша (должен быть 1 час)
curl -I https://your-domain.com/logo.png
```

**Ожидаемые результаты:**

```
# index.html:
Cache-Control: no-cache, no-store, must-revalidate
Pragma: no-cache
Expires: 0

# index.a1b2c3d4.js:
Cache-Control: public, immutable
Expires: Thu, 31 Dec 2099 23:59:59 GMT

# logo.png:
Cache-Control: public, max-age=3600
Expires: [через 1 час]
```

## 🎯 Best Practices

1. **ВСЕГДА используйте `./redeploy-frontend.sh` для деплоя**
2. **НЕ забывайте инкрементировать `?v=X` в URL WebApp при критичных обновлениях**
3. **Проверяйте headers после деплоя** (`curl -I`)
4. **Тестируйте на ВСЕХ платформах** (iOS, Android, Desktop)
5. **Информируйте пользователей** о необходимости перезапуска Telegram
6. **Добавляйте версию в package.json** при каждом релизе

## 📝 Changelog

### v0.11.3 (2024-01-15)
- ✅ Добавлен cache busting через Vite (хеши в именах файлов)
- ✅ Обновлён nginx.conf (no-cache для index.html)
- ✅ Создан скрипт `redeploy-frontend.sh`
- ✅ Создана документация `CACHE_BUSTING.md`

## 🔗 Полезные ссылки

- [Telegram WebApp Docs](https://core.telegram.org/bots/webapps)
- [Vite Build Options](https://vitejs.dev/config/build-options.html)
- [Nginx Caching Guide](https://nginx.org/en/docs/http/ngx_http_headers_module.html)
- [HTTP Cache Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)
