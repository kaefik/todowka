from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task


class Context(Base, TimestampMixin):
    __tablename__ = "contexts"

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    icon: Mapped[str | None] = mapped_column(String, nullable=True)
    color: Mapped[str | None] = mapped_column(String, nullable=True)

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="context")
