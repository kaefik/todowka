from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class SubtaskCreate(BaseModel):
    title: str
    order: Optional[int] = None


class SubtaskUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
    order: Optional[int] = None


class SubtaskResponse(BaseModel):
    id: int
    task_id: int
    title: str
    completed: bool
    order: Optional[int]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
