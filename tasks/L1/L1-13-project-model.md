# L1-13 — Создать модель Project

## Цель
Определить модель БД Project.

## Вход
Базовая модель из L1-09.

## Выход
app/models/project.py.

## Готово когда
Модель Project extends Base с полями id, name (String, required), description (String, nullable), status (Enum: active/completed/paused, default=active), start_date (DateTime, nullable), end_date (DateTime, nullable), progress (Integer 0-100, default=0), color (String hex, nullable), created_at, updated_at.

## Подсказка для LLM
Создайте app/models/project.py с моделью Project наследующей Base. Определите enum ProjectStatus (ACTIVE="active", COMPLETED="completed", PAUSED="paused"). Поля: id (унаследован), name (String, nullable=False), description (String, nullable=True), status (Enum ProjectStatus, default=ProjectStatus.ACTIVE), start_date (DateTime, nullable=True), end_date (DateTime, nullable=True), progress (Integer, default=0), color (String, nullable=True), created_at, updated_at (унаследованы).

## Оценка усилия
S

## Файлы для создания
- app/models/project.py

## Поля модели
```python
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin

class ProjectStatus(str):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"

class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default=ProjectStatus.ACTIVE)
    start_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    progress: Mapped[int] = mapped_column(Integer, default=0)
    color: Mapped[str | None] = mapped_column(String, nullable=True)
```
