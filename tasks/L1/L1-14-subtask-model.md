# L1-14 — Создать модель Subtask

## Цель
Определить модель БД Subtask.

## Вход
Базовая модель из L1-09, ссылка на модель Project.

## Выход
app/models/subtask.py.

## Готово когда
Модель Subtask extends Base с полями id, task_id (FK к Task, required), title (String, required), completed (Boolean, default=False), order (Integer), created_at, updated_at.

## Подсказка для LLM
Создайте app/models/subtask.py с моделью Subtask наследующей Base. Поля: id (унаследован), task_id (Integer, ForeignKey("tasks.id"), nullable=False), title (String, nullable=False), completed (Boolean, default=False), order (Integer), created_at, updated_at (унаследованы). Добавьте relationship к Task.

## Оценка усилия
S

## Файлы для создания
- app/models/subtask.py

## Поля модели
```python
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

class Subtask(Base, TimestampMixin):
    __tablename__ = "subtasks"

    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    order: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Relationship к Task будет добавлен после создания модели Task (L1-15)
```
