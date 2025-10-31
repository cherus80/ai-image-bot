"""
Конфигурация Celery для асинхронных задач.

Настройка брокера сообщений (Redis) и backend для хранения результатов.
"""

from celery import Celery

from app.core.config import settings

# Создание экземпляра Celery
celery_app = Celery(
    "ai_image_bot",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.fitting",
        "app.tasks.editing",
        "app.tasks.maintenance",
    ]
)

# Конфигурация Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 минут максимум на задачу
    task_soft_time_limit=25 * 60,  # 25 минут мягкий лимит
    worker_prefetch_multiplier=1,  # Один воркер обрабатывает одну задачу
    worker_max_tasks_per_child=100,  # Перезапуск воркера после 100 задач
    task_acks_late=True,  # Подтверждение задачи после выполнения
    task_reject_on_worker_lost=True,  # Отклонение задачи при потере воркера
    result_expires=3600,  # Хранение результатов 1 час

    # Beat schedule для периодических задач
    beat_schedule={
        "delete-old-files-daily": {
            "task": "app.tasks.maintenance.delete_old_files_task",
            "schedule": 86400.0,  # Каждые 24 часа
        },
        "reset-freemium-counters-daily": {
            "task": "app.tasks.maintenance.reset_freemium_counters_task",
            "schedule": 86400.0,  # Каждые 24 часа
        },
    },
)


# Настройка логирования
celery_app.conf.update(
    worker_redirect_stdouts=True,
    worker_redirect_stdouts_level="INFO",
)


# Task routes для распределения задач по очередям
celery_app.conf.task_routes = {
    "app.tasks.fitting.*": {"queue": "fitting"},
    "app.tasks.editing.*": {"queue": "editing"},
    "app.tasks.maintenance.*": {"queue": "maintenance"},
}


if __name__ == "__main__":
    celery_app.start()
