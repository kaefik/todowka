# L1-16 — Создать модель Notification

## Цель
Определить модель БД Notification.

## Вход
Базовая модель (L1-09), Task модель (L1-15).

## Выход
app/models/notification.py.

## Готово когда
Модель Notification extends Base с полями id, task_id (FK к Task, required), message (String, required), scheduled_at (DateTime, required), sent_at (DateTime, nullable), status (Enum: pending/sent/failed, default=pending), created_at.

## Подсказка для LLM
Создайте app/models/notification.py с моделью Notification наследующей Base. Определите enum NotificationStatus (PENDING="pending", SENT="sent", FAILED="failed"). Поля: id (унаследован), task_id (Integer, ForeignKey("tasks.id"), nullable=False), message (String, nullable=False), scheduled_at (DateTime, nullable=False), sent_at (DateTime, nullable=True), status (Enum NotificationStatus, default=NotificationStatus.PENDING), created_at (унаследован).

## Оценка усилия
S

## Файлы для создания
- app/models/notification.py

## Поля модели
```python
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

class NotificationStatus(str):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"

class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"

    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id"), nullable=False)
    message: Mapped[str] = mapped_column(String, nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String, default=NotificationStatus.PENDING)

    # Relationship к Task
    task: Mapped["Task"] = relationship("Task", back_populates="notifications")
```
