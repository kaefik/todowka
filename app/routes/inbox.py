from fastapi import APIRouter, Depends, Query
from app.services.task import TaskService
from app.schemas.task import TaskCreate, TaskResponse
from app.schemas.pagination import PaginationResponse
from app.dependencies import get_task_service

router = APIRouter(tags=["GTD"])

@router.get("/inbox", response_model=PaginationResponse[TaskResponse])
def get_inbox(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.get_tasks(page, size, status="inbox")

@router.post("/inbox", response_model=TaskResponse, status_code=201)
def create_inbox_task(
    task: TaskCreate,
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.create_task(
        task.title,
        task.description,
        task.priority,
        task.due_date,
        task.reminder_time,
        task.project_id,
        task.context_id,
        task.area_id,
        task.tag_ids,
        "inbox",
        task.is_next_action,
        task.waiting_for,
        task.delegated_to,
        task.someday
    )

@router.get("/next-actions", response_model=PaginationResponse[TaskResponse])
def get_next_actions(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    task_service: TaskService = Depends(get_task_service)
):
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
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.get_tasks(page, size, status="waiting")

@router.get("/someday", response_model=PaginationResponse[TaskResponse])
def get_someday(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.get_tasks(page, size, someday=True)
