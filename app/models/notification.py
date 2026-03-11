from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin


class NotificationStatus(str):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"

    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id"), nullable=False)
    message: Mapped[str] = mapped_column(String, nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String, default=NotificationStatus.PENDING)

    task: Mapped["Task"] = relationship("Task", back_populates="notifications")
