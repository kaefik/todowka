# L3-45 — Создать routes для areas (CRUD + задачи по области)

## Цель
Определить API routes для областей.

## Вход
AreaService (L2-36), Area схемы (L1-21).

## Выход
app/routes/areas.py.

## Готово когда
Все endpoints для areas реализованы.

## Подсказка для LLM
Создайте app/routes/areas.py с APIRouter. Endpoints: GET /api/v1/areas (список всех областей, возвращает List[AreaResponse]), GET /api/v1/areas/{id}, POST /api/v1/areas, PUT /api/v1/areas/{id}, DELETE /api/v1/areas/{id}, GET /api/v1/areas/{id}/tasks (получить задачи в этой области, возвращает PaginationResponse[TaskResponse]). Используйте dependency injection для area_service.

## Оценка усилия
M

## Файлы для создания
- app/routes/areas.py

## API Endpoints
```python
from fastapi import APIRouter, Depends, Query
from typing import List
from app.services.area import AreaService
from app.services.task import TaskService
from app.schemas.area import AreaCreate, AreaResponse
from app.schemas.task import TaskResponse
from app.schemas.pagination import PaginationResponse

router = APIRouter(prefix="/areas", tags=["Areas"])

@router.get("", response_model=List[AreaResponse])
def get_all_areas(
    area_service: AreaService = Depends()
):
    """Получить список всех областей"""
    return area_service.get_all()

@router.get("/{area_id}", response_model=AreaResponse)
def get_area(
    area_id: int,
    area_service: AreaService = Depends()
):
    """Получить область по ID"""
    return area_service.get_by_id(area_id)

@router.post("", response_model=AreaResponse, status_code=201)
def create_area(
    area: AreaCreate,
    area_service: AreaService = Depends()
):
    """Создать новую область"""
    return area_service.create(area.name, area.description, area.color)

@router.put("/{area_id}", response_model=AreaResponse)
def update_area(
    area_id: int,
    area: AreaCreate,
    area_service: AreaService = Depends()
):
    """Обновить область"""
    return area_service.update(area_id, area.name, area.description, area.color)

@router.delete("/{area_id}", status_code=204)
def delete_area(
    area_id: int,
    area_service: AreaService = Depends()
):
    """Удалить область"""
    area_service.delete(area_id)
    return None

@router.get("/{area_id}/tasks", response_model=PaginationResponse[TaskResponse])
def get_area_tasks(
    area_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    task_service: TaskService = Depends()
):
    """Получить задачи в этой области"""
    return task_service.get_tasks(page, size, area_id=area_id)
```
