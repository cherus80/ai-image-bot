# Настройка nginx для AI Image Generator Bot

Пошаговая инструкция по настройке nginx как reverse proxy для вашего приложения.

---

## Что нужно настроить в nginx

Nginx будет выступать в роли reverse proxy, перенаправляя запросы:

- `/api/*` → Backend (FastAPI на порту 8000)
- `/ws/*` → WebSocket (для real-time updates)
- `/uploads/*` → Статические файлы (загруженные изображения)
- `/*` → Frontend (React на порту 3000)

---

## Шаг 1: Копирование конфигурации

```bash
# Копируем готовую конфигурацию
sudo cp nginx/ai-image-bot.conf /etc/nginx/sites-available/ai-image-bot.conf
```

---

## Шаг 2: Редактирование конфигурации

Откройте файл:

```bash
sudo nano /etc/nginx/sites-available/ai-image-bot.conf
```

### Что нужно изменить:

#### 1. Доменное имя (3 места)

Найдите и замените `your-domain.com` на ваш реальный домен:

```nginx
# Строка ~15 (HTTP сервер)
server_name your-domain.com www.your-domain.com;

# Строка ~33 (HTTPS сервер)
server_name your-domain.com www.your-domain.com;
```

#### 2. Пути к SSL сертификатам (3 места)

```nginx
# Строки ~36-38
ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
ssl_trusted_certificate /etc/letsencrypt/live/your-domain.com/chain.pem;
```

**Замените `your-domain.com` на ваш домен.**

#### 3. (Опционально) Отключить Swagger в production

Найдите секцию `# Swagger UI` (строка ~102) и закомментируйте:

```nginx
# ОТКЛЮЧИТЬ В PRODUCTION!
# location /docs {
#     proxy_pass http://backend_api;
#     ...
# }
#
# location /openapi.json {
#     proxy_pass http://backend_api;
#     ...
# }
```

---

## Шаг 3: Создание симлинка

```bash
# Создаём симлинк в sites-enabled
sudo ln -s /etc/nginx/sites-available/ai-image-bot.conf /etc/nginx/sites-enabled/

# Проверяем, что симлинк создан
ls -la /etc/nginx/sites-enabled/
```

---

## Шаг 4: Удаление дефолтной конфигурации (опционально)

Если вы не используете дефолтный сайт nginx:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

---

## Шаг 5: Проверка конфигурации

```bash
sudo nginx -t
```

**Ожидаемый вывод:**

```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

**Если есть ошибки:**

- Проверьте синтаксис (пропущенные `;`, скобки)
- Проверьте пути к SSL сертификатам
- Убедитесь, что доменное имя правильное

---

## Шаг 6: Перезагрузка nginx

```bash
# Перезагрузить конфигурацию (без простоя)
sudo systemctl reload nginx

# Или полный перезапуск
sudo systemctl restart nginx

# Проверить статус
sudo systemctl status nginx
```

---

## Проверка работы

### 1. Проверка HTTP → HTTPS редиректа

```bash
curl -I http://your-domain.com
```

Должно вернуть:

```
HTTP/1.1 301 Moved Permanently
Location: https://your-domain.com/
```

### 2. Проверка HTTPS

```bash
curl -I https://your-domain.com
```

Должно вернуть:

```
HTTP/2 200
```

### 3. Проверка API

```bash
curl https://your-domain.com/api/v1/health
```

Должно вернуть:

```json
{"status": "ok"}
```

### 4. Проверка в браузере

Откройте:
- https://your-domain.com — должен открыться frontend
- https://your-domain.com/api/v1 — должен вернуть API
- https://your-domain.com/docs — Swagger UI (если не отключили)

---

## Структура конфигурации

```
/etc/nginx/
├── nginx.conf                          # Главная конфигурация nginx
├── sites-available/
│   └── ai-image-bot.conf              # Наша конфигурация (исходник)
├── sites-enabled/
│   └── ai-image-bot.conf -> ../sites-available/ai-image-bot.conf  # Симлинк
└── conf.d/
```

---

## Основные блоки конфигурации

### 1. Upstream (строки 5-12)

Определяет backend серверы:

```nginx
upstream backend_api {
    server localhost:8000;  # FastAPI backend
    keepalive 32;
}

upstream frontend_app {
    server localhost:3000;  # React frontend
    keepalive 32;
}
```

### 2. HTTP сервер (строки 15-25)

Редирект HTTP → HTTPS:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### 3. HTTPS сервер (строки 28-186)

Основной сервер с SSL:

- SSL сертификаты и настройки
- Security headers
- Gzip compression
- Proxy для API, WebSocket, статики, frontend

### 4. Proxy для API (строки 80-95)

```nginx
location /api/ {
    proxy_pass http://backend_api;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    # ... другие headers
}
```

### 5. WebSocket (строки 113-126)

```nginx
location /ws/ {
    proxy_pass http://backend_api;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    # ...
}
```

### 6. Статические файлы (строки 128-138)

```nginx
location /uploads/ {
    alias /var/www/ai-image-bot/uploads/;
    expires 24h;
}
```

### 7. Frontend (строки 140-153)

```nginx
location / {
    proxy_pass http://frontend_app;
    # ...
}
```

---

## Важные настройки

### Security Headers (строки 55-60)

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
```

### Максимальный размер загрузки (строка 66)

```nginx
client_max_body_size 5M;  # Для загрузки изображений до 5MB
```

### Таймауты (строки 69-71)

```nginx
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;
```

### Gzip compression (строки 74-80)

```nginx
gzip on;
gzip_types text/plain text/css application/javascript application/json;
```

---

## Логи

Логи nginx находятся в:

```bash
# Access log (все запросы)
/var/log/nginx/ai-image-bot-access.log

# Error log (ошибки)
/var/log/nginx/ai-image-bot-error.log

# Просмотр логов в реальном времени
sudo tail -f /var/log/nginx/ai-image-bot-access.log
sudo tail -f /var/log/nginx/ai-image-bot-error.log

# Поиск ошибок за последний час
sudo grep "error" /var/log/nginx/ai-image-bot-error.log | tail -n 50
```

---

## Troubleshooting

### Проблема: 502 Bad Gateway

**Причина:** Backend не запущен или недоступен

**Решение:**

```bash
# Проверьте, что backend работает
curl http://localhost:8000/health

# Проверьте Docker контейнеры
docker ps | grep backend

# Проверьте логи backend
./deploy.sh logs backend
```

### Проблема: 404 Not Found для /api/*

**Причина:** Неправильный proxy_pass

**Решение:**

Проверьте, что в конфигурации nginx:

```nginx
location /api/ {
    proxy_pass http://backend_api;  # БЕЗ trailing slash!
}
```

### Проблема: SSL certificate not found

**Причина:** Сертификат не получен или неправильный путь

**Решение:**

```bash
# Проверьте наличие сертификатов
sudo ls -la /etc/letsencrypt/live/your-domain.com/

# Получите сертификат заново
sudo certbot certonly --standalone -d your-domain.com
```

### Проблема: WebSocket не работает

**Причина:** Неправильные headers для WebSocket

**Решение:**

Убедитесь, что в конфигурации nginx:

```nginx
location /ws/ {
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

---

## Полезные команды nginx

```bash
# Проверка синтаксиса конфигурации
sudo nginx -t

# Перезагрузка конфигурации без простоя
sudo systemctl reload nginx

# Полный перезапуск
sudo systemctl restart nginx

# Остановка
sudo systemctl stop nginx

# Запуск
sudo systemctl start nginx

# Статус
sudo systemctl status nginx

# Просмотр текущей конфигурации
sudo nginx -T

# Включение автозапуска
sudo systemctl enable nginx
```

---

## Безопасность

### 1. Отключите Swagger в production

Закомментируйте в конфигурации:

```nginx
# location /docs { ... }
# location /openapi.json { ... }
```

### 2. Настройте firewall

```bash
# Разрешите только HTTP, HTTPS, SSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

### 3. Ограничьте доступ к /admin

Добавьте в конфигурацию:

```nginx
location /admin {
    # Разрешить только с вашего IP
    allow 1.2.3.4;  # Ваш IP
    deny all;

    proxy_pass http://frontend_app;
    # ...
}
```

### 4. Rate limiting

Добавьте в конфигурацию:

```nginx
# В блоке http {}
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

# В блоке location /api/
limit_req zone=api burst=20 nodelay;
```

---

## Резюме

✅ Скопировали конфигурацию: `nginx/ai-image-bot.conf` → `/etc/nginx/sites-available/`
✅ Изменили доменное имя и пути к SSL
✅ Создали симлинк в `sites-enabled/`
✅ Проверили синтаксис: `sudo nginx -t`
✅ Перезагрузили nginx: `sudo systemctl reload nginx`
✅ Проверили работу: `curl https://your-domain.com`

**nginx настроен и готов к работе! 🚀**

Полная инструкция по деплою: [DEPLOY.md](DEPLOY.md)
