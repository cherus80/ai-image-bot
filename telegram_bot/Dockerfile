# Telegram Bot Dockerfile для AI Image Generator Bot

FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода бота
COPY . .

# Создание пользователя для запуска
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

USER botuser

# Health check
HEALTHCHECK --interval=60s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import sys; sys.exit(0)"

# Запуск бота
CMD ["python", "run_bot.py"]
