from sqlalchemy.orm import Session
from app.models.subtask import Subtask
from app.repositories.base import BaseRepository


class SubtaskRepository(BaseRepository[Subtask]):
    def __init__(self, db: Session):
        super().__init__(db, Subtask)

    def get_by_task(self, task_id: int) -> list[Subtask]:
        return self.db.query(Subtask).filter(Subtask.task_id == task_id).all()
