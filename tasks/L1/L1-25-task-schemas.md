# L1-25 — Создать схемы Task (Create, Update, Response)

## Цель
Определить Pydantic схемы для Task с полями GTD.

## Вход
Task модель (L1-15), схема пагинации (L1-18).

## Выход
app/schemas/task.py.

## Готово когда
TaskCreate, TaskUpdate, TaskResponse со всеми полями GTD и tag_ids в Create.

## Подсказка для LLM
Создайте app/schemas/task.py с классом TaskCreate (title: str, description: Optional[str] = None, priority: Optional[TaskPriority] = None, due_date: Optional[datetime] = None, reminder_time: Optional[datetime] = None, project_id: Optional[int] = None, context_id: Optional[int] = None, area_id: Optional[int] = None, tag_ids: Optional[List[int]] = None, status: Optional[TaskStatus] = None, is_next_action: Optional[bool] = None, waiting_for: Optional[str] = None, delegated_to: Optional[str] = None, someday: Optional[bool] = None), классом TaskUpdate (все поля Optional включая completed: Optional[bool]), классом TaskResponse (все поля плюс tags: List[TagResponse]).

## Оценка усилия
M

## Файлы для создания
- app/schemas/task.py

## Схемы
```python
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.models.task import TaskStatus, TaskPriority
from app.schemas.tag import TagResponse

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = None  # TaskPriority enum values
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    project_id: Optional[int] = None
    context_id: Optional[int] = None
    area_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    status: Optional[str] = None  # TaskStatus enum values
    is_next_action: Optional[bool] = None
    waiting_for: Optional[str] = None
    delegated_to: Optional[str] = None
    someday: Optional[bool] = None

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
    project_id: Optional[int]
    context_id: Optional[int]
    area_id: Optional[int]
    tags: List[TagResponse]

    class Config:
        from_attributes = True
```
