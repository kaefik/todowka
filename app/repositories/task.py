from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.task import Task, TaskStatus, task_tags
from app.repositories.base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    def __init__(self, db: Session):
        super().__init__(db, Task)

    def get_filtered(self, filters: dict) -> tuple[list[Task], int]:
        query = self.db.query(Task)

        if 'status' in filters and filters['status']:
            query = query.filter(Task.status == filters['status'])
        if 'project_id' in filters and filters['project_id']:
            query = query.filter(Task.project_id == filters['project_id'])
        if 'context_id' in filters and filters['context_id']:
            query = query.filter(Task.context_id == filters['context_id'])
        if 'area_id' in filters and filters['area_id']:
            query = query.filter(Task.area_id == filters['area_id'])
        if 'priority' in filters and filters['priority']:
            query = query.filter(Task.priority == filters['priority'])
        if 'tag_ids' in filters and filters['tag_ids']:
            query = query.join(task_tags).filter(
                task_tags.c.tag_id.in_(filters['tag_ids'])
            )
        if 'due_date' in filters and filters['due_date']:
            query = query.filter(Task.due_date <= filters['due_date'])

        total = query.count()
        limit = filters.get('limit', 100)
        offset = filters.get('offset', 0)
        tasks = query.offset(offset).limit(limit).all()

        return tasks, total

    def count(self, filters: dict) -> int:
        tasks, total = self.get_filtered(filters)
        return total

    def get_by_tags(self, tag_ids: List[int]) -> list[Task]:
        return self.db.query(Task).join(task_tags).filter(
            task_tags.c.tag_id.in_(tag_ids)
        ).all()

    def get_next_actions(self) -> list[Task]:
        return self.db.query(Task).filter(
            Task.is_next_action == True,
            Task.completed == False
        ).all()

    def get_inbox(self) -> list[Task]:
        return self.db.query(Task).filter(
            Task.status == TaskStatus.INBOX
        ).all()

    def get_waiting(self) -> list[Task]:
        return self.db.query(Task).filter(
            Task.status == TaskStatus.WAITING
        ).all()

    def get_someday(self) -> list[Task]:
        return self.db.query(Task).filter(
            Task.someday == True
        ).all()
