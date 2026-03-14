from fastapi import APIRouter, Depends, Query
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.services.task import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.pagination import PaginationResponse
from app.dependencies import get_task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


class NextActionRequest(BaseModel):
    flag: bool


class ReminderRequest(BaseModel):
    time: datetime


@router.get("/next-actions", response_model=list[TaskResponse])
def get_next_actions(
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.get_next_actions()


@router.get("", response_model=PaginationResponse[TaskResponse])
def get_tasks(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    project_id: Optional[int] = Query(None),
    context_id: Optional[int] = Query(None),
    area_id: Optional[int] = Query(None),
    priority: Optional[str] = Query(None),
    tag_ids: Optional[str] = Query(None),
    task_service: TaskService = Depends(get_task_service)
):
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
        filters['tag_ids'] = [int(t) for t in tag_ids.split(',')]

    return task_service.get_tasks(page, size, **filters)


@router.get("/deleted", response_model=list[TaskResponse])
def get_deleted_tasks(
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.get_deleted_tasks()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.get_task(task_id)


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(
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
        task.status,
        task.is_next_action,
        task.waiting_for,
        task.delegated_to,
        task.someday
    )


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskCreate,
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.update_task(
        task_id,
        task.title,
        task.description,
        task.completed,
        task.priority,
        task.due_date,
        task.reminder_time,
        task.project_id,
        task.context_id,
        task.area_id,
        task.tag_ids,
        task.status,
        task.is_next_action,
        task.waiting_for,
        task.delegated_to,
        task.someday,
        task.completed_at
    )


@router.patch("/{task_id}", response_model=TaskResponse)
def partial_update_task(
    task_id: int,
    task: TaskUpdate,
    task_service: TaskService = Depends(get_task_service)
):
    update_data = task.model_dump(exclude_unset=True)
    return task_service.patch_task(task_id, update_data)


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    task_service.delete_task(task_id)


@router.post("/{task_id}/next-action", response_model=TaskResponse)
def set_next_action(
    task_id: int,
    request: NextActionRequest,
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.set_next_action(task_id, request.flag)


@router.post("/{task_id}/complete", response_model=TaskResponse)
def toggle_complete(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.toggle_complete(task_id)


@router.post("/{task_id}/schedule-reminder", response_model=TaskResponse)
def schedule_reminder(
    task_id: int,
    request: ReminderRequest,
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.schedule_reminder(task_id, request.time)


@router.post("/{task_id}/restore", response_model=TaskResponse)
def restore_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.restore_task(task_id)


@router.delete("/{task_id}/permanent", status_code=204)
def permanent_delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    task_service.permanent_delete_task(task_id)


@router.delete("/deleted/all", status_code=204)
def delete_all_from_trash(
    task_service: TaskService = Depends(get_task_service)
):
    task_service.delete_all_from_trash()
