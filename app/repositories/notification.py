from typing import Optional
from sqlalchemy.orm import Session
from app.models.notification import Notification, NotificationStatus
from app.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, db: Session):
        super().__init__(db, Notification)

    def get_pending(self) -> list[Notification]:
        return self.db.query(Notification).filter(
            Notification.status == NotificationStatus.PENDING
        ).all()

    def mark_sent(self, id: int) -> Optional[Notification]:
        return self.update(id, status=NotificationStatus.SENT)

    def mark_failed(self, id: int, error: str) -> Optional[Notification]:
        notification = self.get(id)
        if notification:
            notification.status = NotificationStatus.FAILED
            notification.message = f"{notification.message} [Error: {error}]"
            self.db.commit()
            self.db.refresh(notification)
        return notification
