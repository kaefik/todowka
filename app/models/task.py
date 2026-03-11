from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin
from app.models.tag import Tag


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

    project_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("projects.id"), nullable=True)
    context_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("contexts.id"), nullable=True)
    area_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("areas.id"), nullable=True)

    tags: Mapped[list[Tag]] = relationship("Tag", secondary=task_tags, back_populates="tasks")
    subtasks: Mapped[list["Subtask"]] = relationship("Subtask", back_populates="task")
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")
    context: Mapped["Context"] = relationship("Context", back_populates="tasks")
    area: Mapped["Area"] = relationship("Area", back_populates="tasks")
    notifications: Mapped[list["Notification"]] = relationship("Notification", back_populates="task")
