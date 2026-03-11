# L1-10 — Создать модель Tag

## Цель
Определить модель БД Tag.

## Вход
Базовая модель из L1-09.

## Выход
app/models/tag.py.

## Готово когда
Модель Tag extends Base с полями id, name (String, required, unique), color (String hex, nullable), created_at, updated_at.

## Подсказка для LLM
Создайте app/models/tag.py с моделью Tag наследующей Base. Поля: id (унаследован), name (String, nullable=False, unique=True), color (String, nullable=True), created_at, updated_at (унаследованы).

## Оценка усилия
S

## Файлы для создания
- app/models/tag.py

## Поля модели
```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin

class Tag(Base, TimestampMixin):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    color: Mapped[str | None] = mapped_column(String, nullable=True)
```
