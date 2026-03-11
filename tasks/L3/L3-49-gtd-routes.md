# L3-49 — Создать GTD routes (inbox, next-actions, waiting, someday)

## Цель
Определить GTD-специфичные routes.

## Вход
TaskService (L2-41), Task схемы (L1-25).

## Выход
app/routes/inbox.py.

## Готово когда
Все GTD endpoints реализованы: GET /api/v1/inbox, POST /api/v1/inbox, GET /api/v1/next-actions, GET /api/v1/waiting, GET /api/v1/someday.

## Подсказка для LLM
Создайте app/routes/inbox.py с APIRouter. Endpoints: GET /api/v1/inbox (получить inbox задачи с пагинацией, возвращает PaginationResponse[TaskResponse]), POST /api/v1/inbox (создать задачу с автоматическим статусом inbox, принимает TaskCreate с опциональными полями, возвращает TaskResponse), GET /api/v1/next-actions (получить next action задачи с пагинацией), GET /api/v1/waiting (получить waiting задачи с пагинацией), GET /api/v1/someday (получить someday задачи с пагинацией). Используйте dependency injection для task_service.

## Оценка усилия
M

## Файлы для создания
- app/routes/inbox.py

## API Endpoints
```python
from fastapi import APIRouter, Depends, Query
from app.services.task import TaskService
from app.schemas.task import TaskCreate, TaskResponse
from app.schemas.pagination import PaginationResponse

router = APIRouter(tags=["GTD"])

@router.get("/inbox", response_model=PaginationResponse[TaskResponse])
def get_inbox(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    task_service: TaskService = Depends()
):
    """Получить inbox задачи (входящие)"""
    return task_service.get_tasks(page, size, status="inbox")

@router.post("/inbox", response_model=TaskResponse, status_code=201)
def create_inbox_task(
    task: TaskCreate,
    task_service: TaskService = Depends()
):
    """Создать задачу в inbox (автоматически status=inbox)"""
    task_data = task.model_copy(update={"status": "inbox"})
    return task_service.create_task(task_data)

@router.get("/next-actions", response_model=PaginationResponse[TaskResponse])
def get_next_actions(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    task_service: TaskService = Depends()
):
    """Получить следующие действия (next actions)"""
    tasks = task_service.task_repo.get_next_actions()
    total = len(tasks)
    offset = (page - 1) * size
    items = [TaskResponse.model_validate(t) for t in tasks[offset:offset+size]]

    return PaginationResponse(
        items=items,
        total=total,
        page=page,
        size=size
    )

@router.get("/waiting", response_model=PaginationResponse[TaskResponse])
def get_waiting(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    task_service: TaskService = Depends()
):
    """Получить задачи в ожидании (waiting for)"""
    return task_service.get_tasks(page, size, status="waiting")

@router.get("/someday", response_model=PaginationResponse[TaskResponse])
def get_someday(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    task_service: TaskService = Depends()
):
    """Получить отложенные задачи (someday/maybe)"""
    return task_service.get_tasks(page, size, someday=True)
```
