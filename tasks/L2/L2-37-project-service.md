# L2-37 — Создать ProjectService (CRUD + complete)

## Цель
Определить ProjectService с логикой завершения проекта.

## Вход
Project репозиторий (L1-30), Project схемы (L1-22).

## Выход
app/services/project.py.

## Готово когда
ProjectService с методами CRUD плюс complete_project, update_progress.

## Подсказка для LLM
Создайте app/services/project.py с классом ProjectService. Методы: __init__(self, project_repo: ProjectRepository), create(self, name: str, description: Optional[str] = None, status: Optional[ProjectStatus] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, color: Optional[str] = None) -> ProjectResponse, get_all(self) -> List[ProjectResponse], get_by_id(self, id: int) -> ProjectResponse (бросает NotFoundException), update(self, id: int, **kwargs) -> ProjectResponse, delete(self, id: int) (проверяет что проект не используется), complete_project(self, id: int) (устанавливает статус COMPLETED и помечает все задачи как завершённые), update_progress(self, id: int) (пересчитывает прогресс на основе задач).

## Оценка усилия
M

## Файлы для создания
- app/services/project.py

## Класс ProjectService
```python
from typing import List
from app.repositories.project import ProjectRepository
from app.repositories.task import TaskRepository
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.exceptions import NotFoundException, ConflictException

class ProjectService:
    def __init__(self, project_repo: ProjectRepository, task_repo: TaskRepository):
        self.project_repo = project_repo
        self.task_repo = task_repo

    def create(self, data: ProjectCreate) -> ProjectResponse:
        project = self.project_repo.create(
            name=data.name,
            description=data.description,
            status=data.status or "active",
            start_date=data.start_date,
            end_date=data.end_date,
            color=data.color
        )
        return ProjectResponse.model_validate(project)

    def get_all(self) -> List[ProjectResponse]:
        projects = self.project_repo.get_all()
        return [ProjectResponse.model_validate(p) for p in projects]

    def get_by_id(self, id: int) -> ProjectResponse:
        project = self.project_repo.get(id)
        if not project:
            raise NotFoundException(f"Project with id {id} not found")
        return ProjectResponse.model_validate(project)

    def update(self, id: int, data: ProjectUpdate) -> ProjectResponse:
        if not self.project_repo.exists(id):
            raise NotFoundException(f"Project with id {id} not found")
        updated = self.project_repo.update(id, **data.model_dump(exclude_unset=True))
        return ProjectResponse.model_validate(updated)

    def delete(self, id: int) -> None:
        if not self.project_repo.exists(id):
            raise NotFoundException(f"Project with id {id} not found")

        # Проверка что проект не используется
        tasks = self.task_repo.get_filtered({'project_id': id})[0]
        if tasks:
            raise ConflictException("Cannot delete project with tasks")

        self.project_repo.delete(id)

    def complete_project(self, id: int) -> ProjectResponse:
        """Завершает проект и все его задачи"""
        project = self.project_repo.get(id)
        if not project:
            raise NotFoundException(f"Project with id {id} not found")

        # Устанавливаем статус проекта как завершённый
        self.project_repo.update(id, status="completed", end_date=datetime.now())

        # Завершаем все задачи проекта
        tasks = self.task_repo.get_filtered({'project_id': id})[0]
        for task in tasks:
            self.task_repo.update(task.id, completed=True)

        return self.get_by_id(id)

    def update_progress(self, id: int) -> ProjectResponse:
        """Пересчитывает прогресс проекта"""
        self.project_repo.update_progress(id)
        return self.get_by_id(id)
```
