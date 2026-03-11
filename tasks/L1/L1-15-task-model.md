# L1-15 — Создать модель Task с m2m к Tag

## Цель
Определить модель БД Task с полями GTD и relationship к Tag.

## Вход
Базовая модель (L1-09), Tag модель (L1-10), Context (L1-11), Area (L1-12), Project (L1-13).

## Выход
app/models/task.py с many-to-many к Tag.

## Готово когда
Модель Task extends Base со всеми полями: id, title, description, completed, status (Enum), priority (Enum), due_date, reminder_time, is_next_action, waiting_for, delegated_to, someday, created_at, updated_at, project_id, context_id, area_id. M2M relationship к Tag через таблицу task_tags.

## Подсказка для LLM
Создайте app/models/task.py с моделью Task наследующей Base. Определите enum TaskStatus (INBOX="inbox", ACTIVE="active", SOMEDAY="someday", WAITING="waiting", DELEGATED="delegated"). Определите enum TaskPriority (LOW="low", MEDIUM="medium", HIGH="high"). Создайте ассоциационную таблицу task_tags с task_id и tag_id. Поля: id (унаследован), title (String, nullable=False), description (String, nullable=True), completed (Boolean, default=False), status (Enum TaskStatus, default=TaskStatus.ACTIVE), priority (Enum TaskPriority, default=TaskPriority.MEDIUM), due_date (DateTime, nullable=True), reminder_time (DateTime, nullable=True), is_next_action (Boolean, default=False), waiting_for (String, nullable=True), delegated_to (String, nullable=True), someday (Boolean, default=False), created_at, updated_at (унаследованы), project_id (Integer, ForeignKey("projects.id"), nullable=True), context_id (Integer, ForeignKey("contexts.id"), nullable=True), area_id (Integer, ForeignKey("areas.id"), nullable=True), tags (relationship к Tag, secondary=task_tags).

## Оценка усилия
M

## Файлы для создания
- app/models/task.py

## Enum и ассоциационная таблица
```python
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin
from app.models.tag import Tag

# Ассоциационная таблица для many-to-many Task <-> Tag
task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class TaskStatus(str):
    INBOX = "inbox"
    ACTIVE = "active"
    SOMEDAY = "someday"
    WAITING = "waiting"
    DELEGATED = "delegated"

class TaskPriority(str):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
```

## Поля модели Task
```python
class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String, default=TaskStatus.ACTIVE)
    priority: Mapped[str] = mapped_column(String, default=TaskPriority.MEDIUM)
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    reminder_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_next_action: Mapped[bool] = mapped_column(Boolean, default=False)
    waiting_for: Mapped[str | None] = mapped_column(String, nullable=True)
    delegated_to: Mapped[str | None] = mapped_column(String, nullable=True)
    someday: Mapped[bool] = mapped_column(Boolean, default=False)

    # Foreign Keys
    project_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("projects.id"), nullable=True)
    context_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("contexts.id"), nullable=True)
    area_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("areas.id"), nullable=True)

    # Relationships
    tags: Mapped[list[Tag]] = relationship("Tag", secondary=task_tags, back_populates="tasks")
    subtasks: Mapped[list["Subtask"]] = relationship("Subtask", back_populates="task")
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")
    context: Mapped["Context"] = relationship("Context", back_populates="tasks")
    area: Mapped["Area"] = relationship("Area", back_populates="tasks")
    notifications: Mapped[list["Notification"]] = relationship("Notification", back_populates="task")
```

## Примечание
После создания этой задачи нужно обновить модели Project, Context, Area, Tag, Subtask с обратными relationships (back_populates).
