from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)
