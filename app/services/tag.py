from typing import List
from sqlalchemy.orm import Session
from app.repositories.tag import TagRepository
from app.repositories.task import TaskRepository
from app.schemas.tag import TagCreate, TagResponse
from app.exceptions import NotFoundException


class TagService:
    def __init__(self, tag_repo: TagRepository, task_repo: TaskRepository, db: Session):
        self.tag_repo = tag_repo
        self.task_repo = task_repo
        self.db = db

    def create(self, name: str, color: str = None) -> TagResponse:
        tag = self.tag_repo.create(name=name, color=color)
        return TagResponse.model_validate(tag)

    def get_all(self) -> List[TagResponse]:
        tags = self.tag_repo.get_all()
        return [TagResponse.model_validate(tag) for tag in tags]

    def get_by_id(self, id: int) -> TagResponse:
        tag = self.tag_repo.get(id)
        if not tag:
            raise NotFoundException(f"Tag with id {id} not found")
        return TagResponse.model_validate(tag)

    def update(self, id: int, name: str = None, color: str = None) -> TagResponse:
        tag = self.tag_repo.get(id)
        if not tag:
            raise NotFoundException(f"Tag with id {id} not found")
        updated = self.tag_repo.update(id, name=name, color=color)
        return TagResponse.model_validate(updated)

    def delete(self, id: int) -> None:
        if not self.tag_repo.exists(id):
            raise NotFoundException(f"Tag with id {id} not found")
        self.tag_repo.delete(id)

    def assign_tags(self, task_id: int, tag_ids: List[int]) -> None:
        task = self.task_repo.get(task_id)
        if not task:
            raise NotFoundException(f"Task with id {task_id} not found")

        from app.models.tag import Tag
        for tag_id in tag_ids:
            tag = self.tag_repo.get(tag_id)
            if tag and tag not in task.tags:
                task.tags.append(tag)

        self.db.commit()

    def get_task_tags(self, task_id: int) -> List[TagResponse]:
        task = self.task_repo.get(task_id)
        if not task:
            raise NotFoundException(f"Task with id {task_id} not found")
        return [TagResponse.model_validate(tag) for tag in task.tags]
