from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task


class Subtask(Base, TimestampMixin):
    __tablename__ = "subtasks"

    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    order: Mapped[int | None] = mapped_column(Integer, nullable=True)

    task: Mapped["Task"] = relationship("Task", back_populates="subtasks")
