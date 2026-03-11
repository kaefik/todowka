# L5-54 — Настроить Celery в app/services/reminders.py

## Цель
Завершить конфигурацию Celery с Redis broker.

## Вход
Config (L0-2), RemindersService (L2-40).

## Выход
Полностью сконфигурированный Celery app с beat schedule.

## Готово когда
Celery worker и beat могут успешно запускаться, напоминания проверяются периодически.

## Подсказка для LLM
В app/services/reminders.py настройте Celery app с broker URL из config (REDIS_URL), backend URL из config (CELERY_RESULT_BACKEND). Настройте beat schedule для запуска check_and_send_reminders каждые REMINDER_CHECK_INTERVAL секунд. Добавьте задачу которая запрашивает задачи с reminder_time в интервале проверки и создаёт/обновляет уведомления через notification_service.

## Оценка усилия
M

## Файлы для изменения
- app/services/reminders.py

## Обновлённый код
```python
from celery import Celery
from datetime import datetime, timedelta
from app.config import Settings
from app.repositories.notification import NotificationRepository
from app.repositories.task import TaskRepository
from app.services.notification import NotificationService

# Конфигурация Celery
settings = Settings()
celery_app = Celery(
    "reminders",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# Beat schedule - планировщик периодических задач
celery_app.conf.beat_schedule = {
    'check-reminders-every-minute': {
        'task': 'app.services.reminders.check_and_send_reminders',
        'schedule': settings.REMINDER_CHECK_INTERVAL,  # 60 секунд по умолчанию
    },
}

celery_app.conf.timezone = 'UTC'
celery_app.conf.task_serializer = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.result_serializer = 'json'
celery_app.conf.enable_utc = True

@celery_app.task
def check_and_send_reminders():
    """
    Периодическая задача для проверки напоминаний.
    Выполняется каждую минуту (или другой интервал из настроек).
    """
    from app.main import SessionLocal

    db = SessionLocal()
    try:
        task_repo = TaskRepository(db)
        notification_repo = NotificationRepository(db)
        notification_service = NotificationService(notification_repo)

        now = datetime.now()
        # Проверяем задачи с reminder_time в ближайшую минуту
        time_threshold = now + timedelta(minutes=1)

        from app.models.task import Task
        tasks = db.query(Task).filter(
            Task.reminder_time.isnot(None),
            Task.reminder_time <= time_threshold,
            Task.reminder_time > now - timedelta(minutes=1)  # Не обрабатываем старые
        ).all()

        for task in tasks:
            # Создаём уведомление
            from app.schemas.notification import NotificationCreate
            notification_service.create_notification(
                NotificationCreate(
                    task_id=task.id,
                    message=f"Reminder: {task.title}",
                    scheduled_at=task.reminder_time
                )
            )

            # Отправляем email (placeholder)
            send_email(task)

            # Отправляем webhook (placeholder)
            send_webhook(task)

    finally:
        db.close()

def send_email(task):
    """Placeholder для отправки email"""
    # TODO: Реализовать отправку email через SMTP или сервис
    print(f"[EMAIL] Reminder sent for task: {task.title}")
    pass

def send_webhook(task):
    """Placeholder для отправки webhook"""
    # TODO: Реализовать отправку webhook
    print(f"[WEBHOOK] Reminder sent for task: {task.title}")
    pass
```

## Запуск Celery

```bash
# Worker (обработчик задач)
celery -A app.services.reminders worker --loglevel=info

# Beat (планировщик периодических задач)
celery -A app.services.reminders beat --loglevel=info
```

## Проверка работы

```bash
# Проверка что Celery worker запущен
celery -A app.services.reminders inspect active

# Проверка что Celery beat запущен
celery -A app.services.reminders inspect registered
```

## Примечание
- Убедитесь что Redis сервер запущен: `redis-server`
- Проверьте настройки в .env: REDIS_URL, CELERY_BROKER_URL, CELERY_RESULT_BACKEND
- Интервал проверки задаётся в REMINDER_CHECK_INTERVAL (по умолчанию 60 секунд)
- Email и webhook отправка — placeholder для будущей реализации
- Все уведомления сохраняются в БД в таблице notifications
