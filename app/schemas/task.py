from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.schemas.tag import TagResponse


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    project_id: Optional[int] = None
    context_id: Optional[int] = None
    area_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    status: Optional[str] = None
    is_next_action: Optional[bool] = None
    waiting_for: Optional[str] = None
    delegated_to: Optional[str] = None
    someday: Optional[bool] = None
    completed_at: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    project_id: Optional[int] = None
    context_id: Optional[int] = None
    area_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    status: Optional[str] = None
    is_next_action: Optional[bool] = None
    waiting_for: Optional[str] = None
    delegated_to: Optional[str] = None
    someday: Optional[bool] = None
    completed_at: Optional[datetime] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    status: str
    priority: str
    due_date: Optional[datetime]
    reminder_time: Optional[datetime]
    is_next_action: bool
    waiting_for: Optional[str]
    delegated_to: Optional[str]
    someday: bool
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    project_id: Optional[int]
    context_id: Optional[int]
    area_id: Optional[int]
    tags: List[TagResponse]
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
