# L1-22 — Создать схемы Project

## Цель
Определить Pydantic схемы для Project.

## Вход
Project модель (L1-13), схема пагинации (L1-18).

## Выход
app/schemas/project.py.

## Готово когда
ProjectCreate, ProjectUpdate, ProjectResponse со всеми полями.

## Подсказка для LLM
Создайте app/schemas/project.py с классом ProjectCreate (name: str, description: Optional[str] = None, status: Optional[ProjectStatus] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, color: Optional[str] = None), классом ProjectUpdate (все поля Optional включая progress), классом ProjectResponse (все поля).

## Оценка усилия
S

## Файлы для создания
- app/schemas/project.py

## Схемы
```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.project import ProjectStatus

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[str] = None  # ProjectStatus enum values
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    color: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    progress: Optional[int] = None
    color: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    progress: int
    color: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```
