# L1-21 — Создать схемы Area

## Цель
Определить Pydantic схемы для Area.

## Вход
Area модель (L1-12), схема пагинации (L1-18).

## Выход
app/schemas/area.py.

## Готово когда
AreaCreate с полями name, description, color; AreaResponse с полями id, name, description, color, created_at, updated_at.

## Подсказка для LLM
Создайте app/schemas/area.py с классом AreaCreate (name: str, description: Optional[str] = None, color: Optional[str] = None) и классом AreaResponse (id: int, name: str, description: Optional[str], color: Optional[str], created_at: datetime, updated_at: datetime).

## Оценка усилия
S

## Файлы для создания
- app/schemas/area.py

## Схемы
```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class AreaCreate(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None

class AreaResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    color: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```
