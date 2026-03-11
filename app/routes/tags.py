from fastapi import APIRouter, Depends, Query
from app.services.tag import TagService
from app.services.task import TaskService
from app.schemas.tag import TagCreate, TagResponse
from app.schemas.task import TaskResponse
from app.schemas.pagination import PaginationResponse
from app.dependencies import get_tag_service, get_task_service

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("", response_model=list[TagResponse])
def get_all_tags(
    tag_service: TagService = Depends(get_tag_service)
):
    return tag_service.get_all()

@router.get("/{tag_id}", response_model=TagResponse)
def get_tag(
    tag_id: int,
    tag_service: TagService = Depends(get_tag_service)
):
    return tag_service.get_by_id(tag_id)

@router.post("", response_model=TagResponse, status_code=201)
def create_tag(
    tag: TagCreate,
    tag_service: TagService = Depends(get_tag_service)
):
    return tag_service.create(tag.name, tag.color)

@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(
    tag_id: int,
    tag: TagCreate,
    tag_service: TagService = Depends(get_tag_service)
):
    return tag_service.update(tag_id, tag.name, tag.color)

@router.delete("/{tag_id}", status_code=204)
def delete_tag(
    tag_id: int,
    tag_service: TagService = Depends(get_tag_service)
):
    tag_service.delete(tag_id)

@router.get("/{tag_id}/tasks", response_model=PaginationResponse[TaskResponse])
def get_tag_tasks(
    tag_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.get_tasks(page, size, tag_ids=[tag_id])
