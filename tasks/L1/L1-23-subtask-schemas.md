# L1-23 — Создать схемы Subtask

## Цель
Определить Pydantic схемы для Subtask.

## Вход
Subtask модель (L1-14), схема пагинации (L1-18).

## Выход
app/schemas/subtask.py.

## Готово когда
SubtaskCreate, SubtaskUpdate, SubtaskResponse со всеми полями.

## Подсказка для LLM
Создайте app/schemas/subtask.py с классом SubtaskCreate (title: str, order: Optional[int] = None), классом SubtaskUpdate (title: Optional[str] = None, completed: Optional[bool] = None, order: Optional[int] = None), классом SubtaskResponse (id: int, task_id: int, title: str, completed: bool, order: Optional[int], created_at: datetime, updated_at: datetime).

## Оценка усилия
S

## Файлы для создания
- app/schemas/subtask.py

## Схемы
```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

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

    class Config:
        from_attributes = True
```
