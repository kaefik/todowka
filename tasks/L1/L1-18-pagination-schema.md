# L1-18 — Создать схему пагинации (schemas/pagination.py)

## Цель
Определить generic схему ответа с пагинацией.

## Вход
Структура проекта из L0-01.

## Выход
app/schemas/pagination.py.

## Готово когда
Класс PaginationResponse generic с полями items, total, page, size.

## Подсказка для LLM
Создайте app/schemas/pagination.py с generic классом PaginationResponse наследующим BaseModel. Поля: items (List[T]), total (int), page (int), size (int). Используйте TypeVar T для generic типа.

## Оценка усилия
S

## Файлы для создания
- app/schemas/pagination.py

## Класс PaginationResponse
```python
from typing import TypeVar, List, Generic
from pydantic import BaseModel

T = TypeVar('T')

class PaginationResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int

    class Config:
        from_attributes = True
```

## Примечание
Этот generic класс будет использоваться во всех list endpoints для возвращения пагинированных данных.
