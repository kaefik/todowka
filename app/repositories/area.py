from sqlalchemy.orm import Session
from app.models.area import Area
from app.repositories.base import BaseRepository


class AreaRepository(BaseRepository[Area]):
    def __init__(self, db: Session):
        super().__init__(db, Area)
