from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task


class Tag(Base, TimestampMixin):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    color: Mapped[str | None] = mapped_column(String, nullable=True)

    tasks: Mapped[list["Task"]] = relationship("Task", secondary="task_tags", back_populates="tags")
