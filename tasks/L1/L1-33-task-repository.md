# L1-33 — Создать репозиторий Task с фильтрами

## Цель
Определить TaskRepository расширяющий BaseRepository с фильтрацией.

## Вход
Базовый репозиторий (L1-26), Task модель (L1-15).

## Выход
app/repositories/task.py.

## Готово когда
TaskRepository extends BaseRepository с методами get_filtered, count, get_by_tags, get_next_actions, get_inbox, get_waiting, get_someday.

## Подсказка для LLM
Создайте app/repositories/task.py с классом TaskRepository наследующим BaseRepository. Добавьте методы: get_filtered(self, filters: dict) фильтрующий по status, project_id, context_id, area_id, priority, tag_ids, due_date; count(self, filters: dict) возвращающий количество; get_by_tags(self, tag_ids: List[int]) возвращающий задачи с этими тегами; get_next_actions(self) возвращающий задачи где is_next_action=True; get_inbox(self) возвращающий задачи со статусом=inbox; get_waiting(self) возвращающий задачи со статусом=waiting; get_someday(self) возвращающий задачи где someday=True.

## Оценка усилия
M

## Файлы для создания
- app/repositories/task.py

## Класс TaskRepository
```python
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.task import Task, TaskStatus
from app.models.notification import task_tags
from app.repositories.base import BaseRepository

class TaskRepository(BaseRepository[Task]):
    def __init__(self, db: Session):
        super().__init__(db, Task)

    def get_filtered(self, filters: dict) -> tuple[list[Task], int]:
        """
        Фильтрует задачи по параметрам.
        Возвращает кортеж (список задач, общее количество)
        """
        query = self.db.query(Task)

        # Фильтры
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

        # Пагинация
        total = query.count()
        limit = filters.get('limit', 100)
        offset = filters.get('offset', 0)
        tasks = query.offset(offset).limit(limit).all()

        return tasks, total

    def count(self, filters: dict) -> int:
        """Подсчитывает количество задач с фильтрами"""
        tasks, total = self.get_filtered(filters)
        return total

    def get_by_tags(self, tag_ids: List[int]) -> list[Task]:
        """Возвращает задачи с указанными тегами"""
        return self.db.query(Task).join(task_tags).filter(
            task_tags.c.tag_id.in_(tag_ids)
        ).all()

    def get_next_actions(self) -> list[Task]:
        """Возвращает задачи помеченные как следующие действия"""
        return self.db.query(Task).filter(
            Task.is_next_action == True,
            Task.completed == False
        ).all()

    def get_inbox(self) -> list[Task]:
        """Возвращает inbox задачи"""
        return self.db.query(Task).filter(
            Task.status == TaskStatus.INBOX
        ).all()

    def get_waiting(self) -> list[Task]:
        """Возвращает задачи в ожидании"""
        return self.db.query(Task).filter(
            Task.status == TaskStatus.WAITING
        ).all()

    def get_someday(self) -> list[Task]:
        """Возвращает отложенные задачи"""
        return self.db.query(Task).filter(
            Task.someday == True
        ).all()
```
