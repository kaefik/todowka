from sqlalchemy.orm import Session
from app.models.context import Context
from app.repositories.base import BaseRepository


class ContextRepository(BaseRepository[Context]):
    def __init__(self, db: Session):
        super().__init__(db, Context)
