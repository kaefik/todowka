from celery import Celery
from datetime import datetime, timedelta
from app.config import settings
from app.repositories.notification import NotificationRepository
from app.repositories.task import TaskRepository
from app.services.notification import NotificationService


celery_app = Celery(
    "reminders",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)


celery_app.conf.beat_schedule = {
    'check-reminders-every-minute': {
        'task': 'app.services.reminders.check_and_send_reminders',
        'schedule': settings.REMINDER_CHECK_INTERVAL,
    },
}

celery_app.conf.timezone = 'UTC'


@celery_app.task
def check_and_send_reminders():
    from app.main import SessionLocal

    db = SessionLocal()
    try:
        task_repo = TaskRepository(db)
        notification_repo = NotificationRepository(db)
        notification_service = NotificationService(notification_repo)

        now = datetime.now()
        time_threshold = now + timedelta(minutes=1)

        from app.models.task import Task
        tasks = db.query(Task).filter(
            Task.reminder_time.isnot(None),
            Task.reminder_time <= time_threshold,
            Task.reminder_time > now - timedelta(minutes=1)
        ).all()

        for task in tasks:
            notification_service.create_notification(
                task.id,
                f"Reminder: {task.title}",
                task.reminder_time
            )

            send_email(task)
            send_webhook(task)

    finally:
        db.close()


def send_email(task):
    print(f"[EMAIL] Reminder sent for task: {task.title}")


def send_webhook(task):
    print(f"[WEBHOOK] Reminder sent for task: {task.title}")
