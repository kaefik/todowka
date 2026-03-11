# L1-19 — Создать схемы Tag (Create, Response)

## Цель
Определить Pydantic схемы для Tag.

## Вход
Tag модель (L1-10), схема пагинации (L1-18).

## Выход
app/schemas/tag.py.

## Готово когда
TagCreate с полями name, color; TagResponse с полями id, name, color, created_at, updated_at.

## Подсказка для LLM
Создайте app/schemas/tag.py с классом TagCreate (name: str, color: Optional[str] = None) и классом TagResponse (id: int, name: str, color: Optional[str], created_at: datetime, updated_at: datetime).

## Оценка усилия
S

## Файлы для создания
- app/schemas/tag.py

## Схемы
```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class TagCreate(BaseModel):
    name: str
    color: Optional[str] = None

class TagResponse(BaseModel):
    id: int
    name: str
    color: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```
