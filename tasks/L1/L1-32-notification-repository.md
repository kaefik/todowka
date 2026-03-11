# L1-32 — Создать репозиторий Notification

## Цель
Определить NotificationRepository расширяющий BaseRepository.

## Вход
Базовый репозиторий (L1-26), Notification модель (L1-16).

## Выход
app/repositories/notification.py.

## Готово когда
NotificationRepository extends BaseRepository с методами get_pending, mark_sent, mark_failed.

## Подсказка для LLM
Создайте app/repositories/notification.py с классом NotificationRepository наследующим BaseRepository. Добавьте методы: get_pending(self) возвращающий список ожидающих уведомлений, mark_sent(self, id: int), mark_failed(self, id: int, error: str).

## Оценка усилия
S

## Файлы для создания
- app/repositories/notification.py

## Класс NotificationRepository
```python
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
```
