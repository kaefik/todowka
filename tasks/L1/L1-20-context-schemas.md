# L1-20 — Создать схемы Context

## Цель
Определить Pydantic схемы для Context.

## Вход
Context модель (L1-11), схема пагинации (L1-18).

## Выход
app/schemas/context.py.

## Готово когда
ContextCreate с полями name, icon, color; ContextResponse с полями id, name, icon, color, created_at, updated_at.

## Подсказка для LLM
Создайте app/schemas/context.py с классом ContextCreate (name: str, icon: Optional[str] = None, color: Optional[str] = None) и классом ContextResponse (id: int, name: str, icon: Optional[str], color: Optional[str], created_at: datetime, updated_at: datetime).

## Оценка усилия
S

## Файлы для создания
- app/schemas/context.py

## Схемы
```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ContextCreate(BaseModel):
    name: str
    icon: Optional[str] = None
    color: Optional[str] = None

class ContextResponse(BaseModel):
    id: int
    name: str
    icon: Optional[str]
    color: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```
