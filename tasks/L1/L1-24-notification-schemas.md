# L1-24 — Создать схемы Notification

## Цель
Определить Pydantic схемы для Notification.

## Вход
Notification модель (L1-16), схема пагинации (L1-18).

## Выход
app/schemas/notification.py.

## Готово когда
NotificationCreate, NotificationResponse со всеми полями.

## Подсказка для LLM
Создайте app/schemas/notification.py с классом NotificationCreate (task_id: int, message: str, scheduled_at: datetime) и классом NotificationResponse (id: int, task_id: int, message: str, scheduled_at: datetime, sent_at: Optional[datetime], status: NotificationStatus, created_at: datetime).

## Оценка усилия
S

## Файлы для создания
- app/schemas/notification.py

## Схемы
```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.notification import NotificationStatus

class NotificationCreate(BaseModel):
    task_id: int
    message: str
    scheduled_at: datetime

class NotificationResponse(BaseModel):
    id: int
    task_id: int
    message: str
    scheduled_at: datetime
    sent_at: Optional[datetime]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
```
