# L3-48 — Создать routes для notifications (GET список, GET по id)

## Цель
Определить API routes для уведомлений.

## Вход
NotificationService (L2-39), Notification схемы (L1-24).

## Выход
app/routes/notifications.py.

## Готово когда
Endpoints для списка уведомлений и получения по id реализованы.

## Подсказка для LLM
Создайте app/routes/notifications.py с APIRouter. Endpoints: GET /api/v1/notifications (список уведомлений с пагинацией: page, size, status?, возвращает PaginationResponse[NotificationResponse]), GET /api/v1/notifications/{id} (получить уведомление по id, возвращает NotificationResponse). Используйте dependency injection для notification_service.

## Оценка усилия
S

## Файлы для создания
- app/routes/notifications.py

## API Endpoints
```python
from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.services.notification import NotificationService
from app.schemas.notification import NotificationResponse
from app.schemas.pagination import PaginationResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=PaginationResponse[NotificationResponse])
def get_notifications(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    notification_service: NotificationService = Depends()
):
    """Получить список уведомлений с пагинацией"""
    filters = {'limit': size, 'offset': (page - 1) * size}
    if status:
        filters['status'] = status

    notifications = notification_service.notification_repo.get_filtered(filters)
    items = [NotificationResponse.model_validate(n) for n in notifications[0]]
    total = notifications[1]

    return PaginationResponse(
        items=items,
        total=total,
        page=page,
        size=size
    )

@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(
    notification_id: int,
    notification_service: NotificationService = Depends()
):
    """Получить уведомление по ID"""
    from app.exceptions import NotFoundException
    if not notification_service.notification_repo.exists(notification_id):
        raise NotFoundException(f"Notification with id {notification_id} not found")

    notification = notification_service.notification_repo.get(notification_id)
    return NotificationResponse.model_validate(notification)
```
