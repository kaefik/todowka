# L2-39 — Создать NotificationService

## Цель
Определить NotificationService с управлением уведомлениями.

## Вход
Notification репозиторий (L1-32), Notification схемы (L1-24).

## Выход
app/services/notification.py.

## Готово когда
NotificationService с методами create, get_pending, send_notification.

## Подсказка для LLM
Создайте app/services/notification.py с классом NotificationService. Методы: __init__(self, notification_repo: NotificationRepository), create_notification(self, task_id: int, message: str, scheduled_at: datetime) -> NotificationResponse, get_pending_notifications(self) -> List[NotificationResponse], send_notification(self, notification: Notification) (делегирует в RemindersService).

## Оценка усилия
S

## Файлы для создания
- app/services/notification.py

## Класс NotificationService
```python
from typing import List
from app.repositories.notification import NotificationRepository
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.exceptions import NotFoundException

class NotificationService:
    def __init__(self, notification_repo: NotificationRepository):
        self.notification_repo = notification_repo

    def create_notification(self, data: NotificationCreate) -> NotificationResponse:
        notification = self.notification_repo.create(
            task_id=data.task_id,
            message=data.message,
            scheduled_at=data.scheduled_at,
            status="pending"
        )
        return NotificationResponse.model_validate(notification)

    def get_pending_notifications(self) -> List[NotificationResponse]:
        notifications = self.notification_repo.get_pending()
        return [NotificationResponse.model_validate(n) for n in notifications]

    def send_notification(self, notification_id: int) -> NotificationResponse:
        """Отправляет уведомление (делегируется в RemindersService)"""
        if not self.notification_repo.exists(notification_id):
            raise NotFoundException(f"Notification with id {notification_id} not found")

        # Здесь будет логика отправки через RemindersService
        # В этой задаче просто помечаем как отправленное
        updated = self.notification_repo.mark_sent(notification_id)
        return NotificationResponse.model_validate(updated)
```
