# L2-40 — Создать RemindersService (Celery)

## Цель
Определить Celery сервис фоновых задач для напоминаний.

## Вход
NotificationService (L2-39).

## Выход
app/services/reminders.py.

## Готово когда
Celery app сконфигурирован, периодическая задача check_and_send_reminders определена.

## Подсказка для LLM
Создайте app/services/reminders.py с экземпляром Celery app. Методы: check_and_send_reminders() - периодическая задача которая проверяет задачи с reminder_time в ближайшее время и создаёт/обновляет уведомления. send_email(self, task: Task) - placeholder для отправки email. send_webhook(self, task: Task) - placeholder для отправки webhook. Настройте Celery beat schedule для запуска check_and_send_reminders каждые REMINDER_CHECK_INTERVAL секунд.

## Оценка усилия
L

## Файлы для создания
- app/services/reminders.py

## Структура RemindersService
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

# Beat schedule
celery_app.conf.beat_schedule = {
    'check-reminders-every-minute': {
        'task': 'app.services.reminders.check_and_send_reminders',
        'schedule': settings.REMINDER_CHECK_INTERVAL,  # 60 секунд по умолчанию
    },
}

celery_app.conf.timezone = 'UTC'

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

## Примечание
- Celery требует работающий Redis сервер
- Настройки берутся из app.config.Settings
- Интервал проверки задаётся в REMINDER_CHECK_INTERVAL (по умолчанию 60 секунд)
- Email и webhook отправка — placeholder для будущей реализации
