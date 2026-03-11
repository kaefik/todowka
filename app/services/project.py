from typing import List
from datetime import datetime
from app.repositories.project import ProjectRepository
from app.repositories.task import TaskRepository
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.exceptions import NotFoundException, ConflictException


class ProjectService:
    def __init__(self, project_repo: ProjectRepository, task_repo: TaskRepository):
        self.project_repo = project_repo
        self.task_repo = task_repo

    def create(self, name: str, description: str = None, status: str = None,
               start_date: datetime = None, end_date: datetime = None, color: str = None) -> ProjectResponse:
        project = self.project_repo.create(
            name=name,
            description=description,
            status=status or "active",
            start_date=start_date,
            end_date=end_date,
            color=color
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

    def update(self, id: int, name: str = None, description: str = None, status: str = None,
               start_date: datetime = None, end_date: datetime = None, progress: int = None,
               color: str = None) -> ProjectResponse:
        if not self.project_repo.exists(id):
            raise NotFoundException(f"Project with id {id} not found")

        update_data = {}
        if name is not None:
            update_data['name'] = name
        if description is not None:
            update_data['description'] = description
        if status is not None:
            update_data['status'] = status
        if start_date is not None:
            update_data['start_date'] = start_date
        if end_date is not None:
            update_data['end_date'] = end_date
        if progress is not None:
            update_data['progress'] = progress
        if color is not None:
            update_data['color'] = color

        updated = self.project_repo.update(id, **update_data)
        return ProjectResponse.model_validate(updated)

    def delete(self, id: int) -> None:
        if not self.project_repo.exists(id):
            raise NotFoundException(f"Project with id {id} not found")

        tasks = self.task_repo.get_filtered({'project_id': id})[0]
        if tasks:
            raise ConflictException("Cannot delete project with tasks")

        self.project_repo.delete(id)

    def complete_project(self, id: int) -> ProjectResponse:
        project = self.project_repo.get(id)
        if not project:
            raise NotFoundException(f"Project with id {id} not found")

        self.project_repo.update(id, status="completed", end_date=datetime.now())

        tasks = self.task_repo.get_filtered({'project_id': id})[0]
        for task in tasks:
            self.task_repo.update(task.id, completed=True)

        return self.get_by_id(id)

    def update_progress(self, id: int) -> ProjectResponse:
        self.project_repo.update_progress(id)
        return self.get_by_id(id)
