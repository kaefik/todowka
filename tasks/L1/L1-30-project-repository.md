# L1-30 — Создать репозиторий Project

## Цель
Определить ProjectRepository расширяющий BaseRepository.

## Вход
Базовый репозиторий (L1-26), Project модель (L1-13).

## Выход
app/repositories/project.py.

## Готово когда
ProjectRepository extends BaseRepository с методами get_by_status и update_progress.

## Подсказка для LLM
Создайте app/repositories/project.py с классом ProjectRepository наследующим BaseRepository. Добавьте методы: get_by_status(self, status: ProjectStatus) возвращающий список Projects, update_progress(self, project_id: int) рассчитывающий прогресс на основе завершённых задач в этом проекте.

## Оценка усилия
S

## Файлы для создания
- app/repositories/project.py

## Класс ProjectRepository
```python
from typing import Optional
from sqlalchemy.orm import Session
from app.models.project import Project, ProjectStatus
from app.repositories.base import BaseRepository

class ProjectRepository(BaseRepository[Project]):
    def __init__(self, db: Session):
        super().__init__(db, Project)

    def get_by_status(self, status: str) -> list[Project]:
        return self.db.query(Project).filter(Project.status == status).all()

    def update_progress(self, project_id: int) -> Optional[Project]:
        project = self.get(project_id)
        if project:
            from app.models.task import Task
            total_tasks = self.db.query(Task).filter(Task.project_id == project_id).count()
            completed_tasks = self.db.query(Task).filter(
                Task.project_id == project_id,
                Task.completed == True
            ).count()
            progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
            project.progress = progress
            self.db.commit()
            self.db.refresh(project)
        return project
```
