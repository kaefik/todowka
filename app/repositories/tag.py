from typing import Optional
from sqlalchemy.orm import Session
from app.models.tag import Tag
from app.repositories.base import BaseRepository


class TagRepository(BaseRepository[Tag]):
    def __init__(self, db: Session):
        super().__init__(db, Tag)

    def get_by_name(self, name: str) -> Optional[Tag]:
        return self.db.query(Tag).filter(Tag.name == name).first()

    def get_or_create(self, name: str, color: Optional[str] = None) -> Tag:
        tag = self.get_by_name(name)
        if not tag:
            tag = self.create(name=name, color=color)
        return tag
