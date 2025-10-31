# 🚀 Подготовка проекта к GitHub и деплою

## ✅ Выполненные действия

### 1. Оптимизация .env файлов
- ✅ Создан единый корневой `.env.example` со всеми переменными
- ✅ Удалены дублирующие `.env` файлы из `backend/` и `frontend/`
- ✅ Корневой `.env` теперь используется всеми сервисами через docker-compose

### 2. Обновлен .gitignore
- ✅ Добавлены правила для исключения всех `.env` файлов
- ✅ Исключена папка `agents/` (VS Code internal)
- ✅ Добавлены правила для `venv/`, `node_modules/`, `logs/`, `*.pyc`
- ✅ Исключены временные файлы (.DS_Store, *.log, uploads/)

### 3. Удалены лишние файлы
- ✅ Удален `.DS_Store` из корня
- ✅ Удалены все логи из `logs/`
- ✅ Удалены старые `.env` файлы из подпапок

### 4. Реорганизована документация
Перемещено в `docs/`:
- ✅ `docs/deployment/` — DEPLOY.md, NGINX_SETUP.md, DEPLOYMENT_FILES.md
- ✅ `docs/development/` — TESTING.md, TESTING_RESULTS.md, LOCAL_TESTING_GUIDE.md, OPTIMIZATION.md
- ✅ `docs/guides/` — QUICKSTART.md, LOCAL_TELEGRAM_SETUP.md, TUNNEL_SETUP.md

Удалены дублирующие файлы:
- ✅ QUICK_START.md
- ✅ QUICK_DEPLOY.md
- ✅ QUICK_TELEGRAM_START.md
- ✅ BUGFIXES.md
- ✅ PROJECT_STRUCTURE_ANALYSIS.md

### 5. Создан GitHub-ready README.md
- ✅ Современный дизайн с badges
- ✅ Эмодзи для навигации
- ✅ Четкая структура (Quickstart, Tech Stack, Features)
- ✅ Ссылки на документацию в `docs/`

### 6. Оптимизирован docker-compose.prod.yml
- ✅ Использует корневой `.env` вместо отдельных файлов
- ✅ Все сервисы читают переменные из одного места

### 7. Созданы GitHub Actions workflows
- ✅ `.github/workflows/ci.yml` — CI/CD pipeline (тесты, линтер, сборка)
- ✅ `.github/workflows/deploy.yml` — автодеплой на VPS

---

## 📋 Что нужно сделать ПЕРЕД коммитом

### 1. ⚠️ КРИТИЧЕСКИ ВАЖНО: Проверьте .env файл

```bash
# Убедитесь, что корневой .env НЕ будет закоммичен:
git status

# Если .env показывается в списке файлов:
git rm --cached .env

# Или если .env уже был закоммичен ранее, удалите его из истории:
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
```

**⚠️ ВАЖНО**: В `.env` хранятся РЕАЛЬНЫЕ API ключи! Не коммитьте этот файл!

### 2. Проверьте, что venv и node_modules не попадут в git

```bash
# Должны быть в .gitignore (уже добавлены):
backend/venv/
frontend/node_modules/
```

### 3. Создайте корневой .env из .env.example

```bash
cp .env.example .env
# Заполните все значения в .env вашими реальными API ключами
```

---

## 🔑 Настройка GitHub Secrets для CI/CD

Для работы автоматического деплоя добавьте следующие secrets в GitHub:

**Settings → Secrets and variables → Actions → New repository secret**

### Обязательные secrets:

```bash
VPS_HOST=your-vps-ip-or-domain
VPS_USERNAME=root
VPS_SSH_KEY=<содержимое вашего SSH private key>
VPS_PORT=22
```

### Опциональные secrets (для production):

```bash
TELEGRAM_BOT_TOKEN=your_real_bot_token
KIE_AI_API_KEY=your_real_kie_api_key
OPENROUTER_API_KEY=your_real_openrouter_key
YUKASSA_SHOP_ID=your_shop_id
YUKASSA_SECRET_KEY=your_secret_key
```

---

## 🚀 Первый коммит в GitHub

### 1. Инициализация Git (если еще не сделано)

```bash
git init
git add .
git commit -m "Initial commit: AI Image Generator Bot v0.12.0

✨ Features:
- Virtual try-on (step-by-step wizard)
- AI-powered image editing with Claude Haiku
- Freemium + subscriptions monetization
- Referral program
- Admin panel
- Telegram Bot integration

🏗️ Tech Stack:
- Backend: FastAPI + PostgreSQL + Celery
- Frontend: React + TypeScript + Vite + Tailwind
- Docker + Docker Compose for deployment

📚 Full feature list in CHANGELOG.md"
```

### 2. Создание репозитория на GitHub

1. Перейдите на https://github.com/new
2. Создайте новый **private** репозиторий
3. **НЕ создавайте** README, .gitignore, LICENSE (они уже есть)

### 3. Связывание с GitHub

```bash
git remote add origin https://github.com/yourusername/ai-image-bot.git
git branch -M main
git push -u origin main
```

### 4. Проверка GitHub Actions

После push проверьте вкладку **Actions** в репозитории:
- ✅ CI workflow должен запуститься автоматически
- ✅ Должны пройти тесты backend и frontend
- ✅ Должны собраться Docker образы

---

## 📦 Деплой на VPS

### Подготовка VPS (один раз)

```bash
# SSH на VPS
ssh root@your-vps-ip

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установка Docker Compose
apt install docker-compose -y

# Клонирование репозитория
git clone https://github.com/yourusername/ai-image-bot.git /var/www/ai-image-bot
cd /var/www/ai-image-bot

# Создание .env файла
cp .env.example .env
nano .env  # Заполните все переменные
```

### Запуск проекта

```bash
# Production запуск
docker-compose -f docker-compose.prod.yml up -d

# Применение миграций
docker-compose exec backend alembic upgrade head

# Просмотр логов
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f telegram_bot
```

### Настройка автодеплоя (опционально)

После настройки GitHub Secrets (см. выше), каждый push в `main` будет автоматически деплоиться на VPS.

---

## 🔍 Проверка перед деплоем

### Checklist:

- [ ] `.env` файл НЕ закоммичен в Git
- [ ] `backend/venv/` и `frontend/node_modules/` НЕ в репозитории
- [ ] GitHub Secrets настроены (VPS_HOST, VPS_SSH_KEY и т.д.)
- [ ] На VPS создан `.env` файл с production переменными
- [ ] На VPS установлен Docker и Docker Compose
- [ ] CI/CD workflow прошел успешно (зеленый статус в Actions)
- [ ] Production переменные в `.env` на VPS (ENVIRONMENT=production, DEBUG=False)
- [ ] HTTPS сертификаты настроены (Let's Encrypt)
- [ ] Nginx настроен как reverse proxy (см. docs/deployment/NGINX_SETUP.md)

---

## 📚 Дополнительная документация

- [docs/deployment/DEPLOY.md](docs/deployment/DEPLOY.md) — детальные инструкции по деплою
- [docs/deployment/NGINX_SETUP.md](docs/deployment/NGINX_SETUP.md) — настройка Nginx
- [docs/guides/QUICKSTART.md](docs/guides/QUICKSTART.md) — быстрый старт для разработчиков
- [CHANGELOG.md](CHANGELOG.md) — полная история изменений

---

## 🎉 Готово!

Ваш проект готов к выгрузке на GitHub и деплою на VPS!

**Следующие шаги:**
1. Создайте GitHub репозиторий
2. Сделайте первый commit и push
3. Настройте GitHub Secrets для автодеплоя
4. Задеплойте на VPS
5. Настройте Telegram Bot через @BotFather
6. Откройте Web App в Telegram и протестируйте!

---

**Сделано с ❤️ с помощью Claude Code**
