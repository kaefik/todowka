from fastapi import APIRouter, Depends, Query
from app.services.area import AreaService
from app.services.task import TaskService
from app.schemas.area import AreaCreate, AreaResponse
from app.schemas.task import TaskResponse
from app.schemas.pagination import PaginationResponse
from app.dependencies import get_area_service, get_task_service

router = APIRouter(prefix="/areas", tags=["Areas"])

@router.get("", response_model=list[AreaResponse])
def get_all_areas(
    area_service: AreaService = Depends(get_area_service)
):
    return area_service.get_all()

@router.get("/{area_id}", response_model=AreaResponse)
def get_area(
    area_id: int,
    area_service: AreaService = Depends(get_area_service)
):
    return area_service.get_by_id(area_id)

@router.post("", response_model=AreaResponse, status_code=201)
def create_area(
    area: AreaCreate,
    area_service: AreaService = Depends(get_area_service)
):
    return area_service.create(area.name, area.description, area.color)

@router.put("/{area_id}", response_model=AreaResponse)
def update_area(
    area_id: int,
    area: AreaCreate,
    area_service: AreaService = Depends(get_area_service)
):
    return area_service.update(area_id, area.name, area.description, area.color)

@router.delete("/{area_id}", status_code=204)
def delete_area(
    area_id: int,
    area_service: AreaService = Depends(get_area_service)
):
    area_service.delete(area_id)

@router.get("/{area_id}/tasks", response_model=PaginationResponse[TaskResponse])
def get_area_tasks(
    area_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.get_tasks(page, size, area_id=area_id)
