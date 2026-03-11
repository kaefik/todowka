# L3-50 — Создать routes для tasks (CRUD + next-action + complete + schedule-reminder)

## Цель
Определить API routes для задач с GTD операциями.

## Вход
TaskService (L2-41), Task схемы (L1-25).

## Выход
app/routes/tasks.py.

## Готово когда
Все endpoints для tasks реализованы.

## Подсказка для LLM
Создайте app/routes/tasks.py с APIRouter. Endpoints: GET /api/v1/tasks (список задач с пагинацией: page, size, status?, project_id?, context_id?, area_id?, priority?, tag_ids?, возвращает PaginationResponse[TaskResponse]), GET /api/v1/tasks/{id}, POST /api/v1/tasks, PUT /api/v1/tasks/{id}, PATCH /api/v1/tasks/{id}, DELETE /api/v1/tasks/{id}, POST /api/v1/tasks/{id}/next-action (пометить как next action, принимает body {"flag": bool}), POST /api/v1/tasks/{id}/complete (переключить завершение), POST /api/v1/tasks/{id}/schedule-reminder (запланировать напоминание, принимает body {"time": datetime}). Используйте dependency injection для task_service.

## Оценка усилия
L

## Файлы для создания
- app/routes/tasks.py

## API Endpoints
```python
from fastapi import APIRouter, Depends, Query, Body
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from app.services.task import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.pagination import PaginationResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Request модели для операций
class NextActionRequest(BaseModel):
    flag: bool

class ReminderRequest(BaseModel):
    time: datetime

@router.get("", response_model=PaginationResponse[TaskResponse])
def get_tasks(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    project_id: Optional[int] = Query(None),
    context_id: Optional[int] = Query(None),
    area_id: Optional[int] = Query(None),
    priority: Optional[str] = Query(None),
    tag_ids: Optional[List[int]] = Query(None),
    task_service: TaskService = Depends()
):
    """Получить список задач с пагинацией и фильтрацией"""
    filters = {}
    if status:
        filters['status'] = status
    if project_id:
        filters['project_id'] = project_id
    if context_id:
        filters['context_id'] = context_id
    if area_id:
        filters['area_id'] = area_id
    if priority:
        filters['priority'] = priority
    if tag_ids:
        filters['tag_ids'] = tag_ids

    return task_service.get_tasks(page, size, **filters)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    task_service: TaskService = Depends()
):
    """Получить задачу по ID"""
    return task_service.get_task(task_id)

@router.post("", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    task_service: TaskService = Depends()
):
    """Создать новую задачу"""
    return task_service.create_task(task)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskCreate,
    task_service: TaskService = Depends()
):
    """Обновить задачу (все поля)"""
    return task_service.update_task(task_id, TaskUpdate(**task.model_dump()))

@router.patch("/{task_id}", response_model=TaskResponse)
def partial_update_task(
    task_id: int,
    task: TaskUpdate,
    task_service: TaskService = Depends()
):
    """Частичное обновление задачи"""
    return task_service.update_task(task_id, task)

@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    task_service: TaskService = Depends()
):
    """Удалить задачу"""
    task_service.delete_task(task_id)
    return None

@router.post("/{task_id}/next-action", response_model=TaskResponse)
def set_next_action(
    task_id: int,
    request: NextActionRequest,
    task_service: TaskService = Depends()
):
    """Пометить задачу как следующее действие"""
    return task_service.set_next_action(task_id, request.flag)

@router.post("/{task_id}/complete", response_model=TaskResponse)
def toggle_complete(
    task_id: int,
    task_service: TaskService = Depends()
):
    """Переключить статус завершения задачи"""
    return task_service.toggle_complete(task_id)

@router.post("/{task_id}/schedule-reminder", response_model=TaskResponse)
def schedule_reminder(
    task_id: int,
    request: ReminderRequest,
    task_service: TaskService = Depends()
):
    """Запланировать напоминание для задачи"""
    return task_service.schedule_reminder(task_id, request.time)
```
