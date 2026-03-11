# L3-44 — Создать routes для contexts (CRUD + задачи по контексту)

## Цель
Определить API routes для контекстов.

## Вход
ContextService (L2-35), Context схемы (L1-20).

## Выход
app/routes/contexts.py.

## Готово когда
Все endpoints для contexts реализованы.

## Подсказка для LLM
Создайте app/routes/contexts.py с APIRouter. Endpoints: GET /api/v1/contexts (список всех контекстов, возвращает List[ContextResponse]), GET /api/v1/contexts/{id}, POST /api/v1/contexts, PUT /api/v1/contexts/{id}, DELETE /api/v1/contexts/{id}, GET /api/v1/contexts/{id}/tasks (получить задачи с этим контекстом, возвращает PaginationResponse[TaskResponse]). Используйте dependency injection для context_service.

## Оценка усилия
M

## Файлы для создания
- app/routes/contexts.py

## API Endpoints
```python
from fastapi import APIRouter, Depends, Query
from typing import List
from app.services.context import ContextService
from app.services.task import TaskService
from app.schemas.context import ContextCreate, ContextResponse
from app.schemas.task import TaskResponse
from app.schemas.pagination import PaginationResponse

router = APIRouter(prefix="/contexts", tags=["Contexts"])

@router.get("", response_model=List[ContextResponse])
def get_all_contexts(
    context_service: ContextService = Depends()
):
    """Получить список всех контекстов"""
    return context_service.get_all()

@router.get("/{context_id}", response_model=ContextResponse)
def get_context(
    context_id: int,
    context_service: ContextService = Depends()
):
    """Получить контекст по ID"""
    return context_service.get_by_id(context_id)

@router.post("", response_model=ContextResponse, status_code=201)
def create_context(
    context: ContextCreate,
    context_service: ContextService = Depends()
):
    """Создать новый контекст"""
    return context_service.create(context.name, context.icon, context.color)

@router.put("/{context_id}", response_model=ContextResponse)
def update_context(
    context_id: int,
    context: ContextCreate,
    context_service: ContextService = Depends()
):
    """Обновить контекст"""
    return context_service.update(context_id, context.name, context.icon, context.color)

@router.delete("/{context_id}", status_code=204)
def delete_context(
    context_id: int,
    context_service: ContextService = Depends()
):
    """Удалить контекст"""
    context_service.delete(context_id)
    return None

@router.get("/{context_id}/tasks", response_model=PaginationResponse[TaskResponse])
def get_context_tasks(
    context_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    task_service: TaskService = Depends()
):
    """Получить задачи с этим контекстом"""
    return task_service.get_tasks(page, size, context_id=context_id)
```
