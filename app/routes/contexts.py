from fastapi import APIRouter, Depends, Query
from app.services.context import ContextService
from app.services.task import TaskService
from app.schemas.context import ContextCreate, ContextResponse
from app.schemas.task import TaskResponse
from app.schemas.pagination import PaginationResponse
from app.dependencies import get_context_service, get_task_service

router = APIRouter(prefix="/contexts", tags=["Contexts"])

@router.get("", response_model=list[ContextResponse])
def get_all_contexts(
    context_service: ContextService = Depends(get_context_service)
):
    return context_service.get_all()

@router.get("/{context_id}", response_model=ContextResponse)
def get_context(
    context_id: int,
    context_service: ContextService = Depends(get_context_service)
):
    return context_service.get_by_id(context_id)

@router.post("", response_model=ContextResponse, status_code=201)
def create_context(
    context: ContextCreate,
    context_service: ContextService = Depends(get_context_service)
):
    return context_service.create(context.name, context.icon, context.color)

@router.put("/{context_id}", response_model=ContextResponse)
def update_context(
    context_id: int,
    context: ContextCreate,
    context_service: ContextService = Depends(get_context_service)
):
    return context_service.update(context_id, context.name, context.icon, context.color)

@router.delete("/{context_id}", status_code=204)
def delete_context(
    context_id: int,
    context_service: ContextService = Depends(get_context_service)
):
    context_service.delete(context_id)

@router.get("/{context_id}/tasks", response_model=PaginationResponse[TaskResponse])
def get_context_tasks(
    context_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.get_tasks(page, size, context_id=context_id)
