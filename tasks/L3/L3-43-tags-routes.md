# L3-43 — Создать routes для tags (CRUD + задачи по тегу)

## Цель
Определить API routes для тегов.

## Вход
TagService (L2-34), Tag схемы (L1-19).

## Выход
app/routes/tags.py.

## Готово когда
Все endpoints для tags реализованы: GET /api/v1/tags, GET /api/v1/tags/{id}, POST /api/v1/tags, PUT /api/v1/tags/{id}, DELETE /api/v1/tags/{id}, GET /api/v1/tags/{id}/tasks.

## Подсказка для LLM
Создайте app/routes/tags.py с APIRouter. Endpoints: GET /api/v1/tags (список всех тегов, возвращает List[TagResponse]), GET /api/v1/tags/{id} (получить тег по id, возвращает TagResponse), POST /api/v1/tags (создать тег, принимает TagCreate, возвращает TagResponse), PUT /api/v1/tags/{id} (обновить тег, принимает TagCreate, возвращает TagResponse), DELETE /api/v1/tags/{id} (удалить тег), GET /api/v1/tags/{id}/tasks (получить задачи с этим тегом, возвращает PaginationResponse[TaskResponse]). Используйте dependency injection для tag_service.

## Оценка усилия
M

## Файлы для создания
- app/routes/tags.py

## API Endpoints
```python
from fastapi import APIRouter, Depends, Query
from typing import List
from app.services.tag import TagService
from app.services.task import TaskService
from app.schemas.tag import TagCreate, TagResponse
from app.schemas.task import TaskResponse
from app.schemas.pagination import PaginationResponse

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("", response_model=List[TagResponse])
def get_all_tags(
    tag_service: TagService = Depends()
):
    """Получить список всех тегов"""
    return tag_service.get_all()

@router.get("/{tag_id}", response_model=TagResponse)
def get_tag(
    tag_id: int,
    tag_service: TagService = Depends()
):
    """Получить тег по ID"""
    return tag_service.get_by_id(tag_id)

@router.post("", response_model=TagResponse, status_code=201)
def create_tag(
    tag: TagCreate,
    tag_service: TagService = Depends()
):
    """Создать новый тег"""
    return tag_service.create(tag.name, tag.color)

@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(
    tag_id: int,
    tag: TagCreate,
    tag_service: TagService = Depends()
):
    """Обновить тег"""
    return tag_service.update(tag_id, tag.name, tag.color)

@router.delete("/{tag_id}", status_code=204)
def delete_tag(
    tag_id: int,
    tag_service: TagService = Depends()
):
    """Удалить тег"""
    tag_service.delete(tag_id)
    return None

@router.get("/{tag_id}/tasks", response_model=PaginationResponse[TaskResponse])
def get_tag_tasks(
    tag_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    task_service: TaskService = Depends()
):
    """Получить задачи с этим тегом"""
    return task_service.get_tasks(page, size, tag_ids=[tag_id])
```
