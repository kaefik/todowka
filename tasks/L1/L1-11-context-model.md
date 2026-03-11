# L1-11 — Создать модель Context

## Цель
Определить модель БД Context (GTD).

## Вход
Базовая модель из L1-09.

## Выход
app/models/context.py.

## Готово когда
Модель Context extends Base с полями id, name (String, required, unique), icon (String, nullable), color (String hex, nullable), created_at, updated_at.

## Подсказка для LLM
Создайте app/models/context.py с моделью Context наследующей Base. Поля: id (унаследован), name (String, nullable=False, unique=True), icon (String, nullable=True), color (String, nullable=True), created_at, updated_at (унаследованы).

## Оценка усилия
S

## Файлы для создания
- app/models/context.py

## Поля модели
```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin

class Context(Base, TimestampMixin):
    __tablename__ = "contexts"

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    icon: Mapped[str | None] = mapped_column(String, nullable=True)
    color: Mapped[str | None] = mapped_column(String, nullable=True)
```
