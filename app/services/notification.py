from typing import List
from datetime import datetime
from app.repositories.notification import NotificationRepository
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.exceptions import NotFoundException


class NotificationService:
    def __init__(self, notification_repo: NotificationRepository):
        self.notification_repo = notification_repo

    def create_notification(self, task_id: int, message: str, scheduled_at: datetime) -> NotificationResponse:
        notification = self.notification_repo.create(
            task_id=task_id,
            message=message,
            scheduled_at=scheduled_at,
            status="pending"
        )
        return NotificationResponse.model_validate(notification)

    def get_pending_notifications(self) -> List[NotificationResponse]:
        notifications = self.notification_repo.get_pending()
        return [NotificationResponse.model_validate(n) for n in notifications]

    def send_notification(self, notification_id: int) -> NotificationResponse:
        if not self.notification_repo.exists(notification_id):
            raise NotFoundException(f"Notification with id {notification_id} not found")

        updated = self.notification_repo.mark_sent(notification_id)
        return NotificationResponse.model_validate(updated)
