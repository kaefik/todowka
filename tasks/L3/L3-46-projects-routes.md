# L3-46 — Создать routes для projects (CRUD + complete + задачи проекта)

## Цель
Определить API routes для проектов.

## Вход
ProjectService (L2-37), Project схемы (L1-22).

## Выход
app/routes/projects.py.

## Готово когда
Все endpoints для projects реализованы.

## Подсказка для LLM
Создайте app/routes/projects.py с APIRouter. Endpoints: GET /api/v1/projects (список проектов с пагинацией: page, size, status?, возвращает PaginationResponse[ProjectResponse]), GET /api/v1/projects/{id}, POST /api/v1/projects, PUT /api/v1/projects/{id}, DELETE /api/v1/projects/{id}, POST /api/v1/projects/{id}/complete (завершить проект), GET /api/v1/projects/{id}/tasks (получить задачи проекта, возвращает PaginationResponse[TaskResponse]). Используйте dependency injection для project_service.

## Оценка усилия
M

## Файлы для создания
- app/routes/projects.py

## API Endpoints
```python
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.services.project import ProjectService
from app.services.task import TaskService
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.schemas.task import TaskResponse
from app.schemas.pagination import PaginationResponse

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("", response_model=PaginationResponse[ProjectResponse])
def get_projects(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    project_service: ProjectService = Depends()
):
    """Получить список проектов с пагинацией и фильтрацией"""
    filters = {'limit': size, 'offset': (page - 1) * size}
    if status:
        filters['status'] = status

    projects = project_service.project_repo.get_filtered(filters)
    items = [ProjectResponse.model_validate(p) for p in projects[0]]
    total = projects[1]

    return PaginationResponse(
        items=items,
        total=total,
        page=page,
        size=size
    )

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    project_service: ProjectService = Depends()
):
    """Получить проект по ID"""
    return project_service.get_by_id(project_id)

@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(
    project: ProjectCreate,
    project_service: ProjectService = Depends()
):
    """Создать новый проект"""
    return project_service.create(project)

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    project_service: ProjectService = Depends()
):
    """Обновить проект"""
    return project_service.update(project_id, project)

@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    project_service: ProjectService = Depends()
):
    """Удалить проект"""
    project_service.delete(project_id)
    return None

@router.post("/{project_id}/complete", response_model=ProjectResponse)
def complete_project(
    project_id: int,
    project_service: ProjectService = Depends()
):
    """Завершить проект и все его задачи"""
    return project_service.complete_project(project_id)

@router.post("/{project_id}/progress", response_model=ProjectResponse)
def update_project_progress(
    project_id: int,
    project_service: ProjectService = Depends()
):
    """Пересчитать прогресс проекта"""
    return project_service.update_progress(project_id)

@router.get("/{project_id}/tasks", response_model=PaginationResponse[TaskResponse])
def get_project_tasks(
    project_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    task_service: TaskService = Depends()
):
    """Получить задачи проекта"""
    return task_service.get_tasks(page, size, project_id=project_id)
```
