# L1-12 — Создать модель Area

## Цель
Определить модель БД Area (GTD).

## Вход
Базовая модель из L1-09.

## Выход
app/models/area.py.

## Готово когда
Модель Area extends Base с полями id, name (String, required, unique), description (String, nullable), color (String hex, nullable), created_at, updated_at.

## Подсказка для LLM
Создайте app/models/area.py с моделью Area наследующей Base. Поля: id (унаследован), name (String, nullable=False, unique=True), description (String, nullable=True), color (String, nullable=True), created_at, updated_at (унаследованы).

## Оценка усилия
S

## Файлы для создания
- app/models/area.py

## Поля модели
```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin

class Area(Base, TimestampMixin):
    __tablename__ = "areas"

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    color: Mapped[str | None] = mapped_column(String, nullable=True)
```
