from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.services.notification import NotificationService
from app.schemas.notification import NotificationResponse
from app.schemas.pagination import PaginationResponse
from app.dependencies import get_notification_service
from app.exceptions import NotFoundException

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=PaginationResponse[NotificationResponse])
def get_notifications(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    notification_service: NotificationService = Depends(get_notification_service)
):
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
    notification_service: NotificationService = Depends(get_notification_service)
):
    if not notification_service.notification_repo.exists(notification_id):
        raise NotFoundException(f"Notification with id {notification_id} not found")

    notification = notification_service.notification_repo.get(notification_id)
    return NotificationResponse.model_validate(notification)
