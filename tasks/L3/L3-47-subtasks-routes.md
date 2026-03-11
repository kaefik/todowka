# L3-47 — Создать routes для subtasks (CRUD вложенные под задачу)

## Цель
Определить API routes для подзадач.

## Вход
SubtaskService (L2-38), Subtask схемы (L1-23).

## Выход
app/routes/subtasks.py.

## Готово когда
Все endpoints для subtasks реализованы с task_id в пути.

## Подсказка для LLM
Создайте app/routes/subtasks.py с APIRouter. Endpoints: GET /api/v1/tasks/{task_id}/subtasks (список подзадач для задачи, возвращает List[SubtaskResponse]), POST /api/v1/tasks/{task_id}/subtasks (создать подзадачу, принимает SubtaskCreate, возвращает SubtaskResponse), PUT /api/v1/tasks/{task_id}/subtasks/{id} (обновить подзадачу, принимает SubtaskUpdate, возвращает SubtaskResponse), DELETE /api/v1/tasks/{task_id}/subtasks/{id}. Используйте dependency injection для subtask_service.

## Оценка усилия
M

## Файлы для создания
- app/routes/subtasks.py

## API Endpoints
```python
from fastapi import APIRouter, Depends
from typing import List
from app.services.subtask import SubtaskService
from app.schemas.subtask import SubtaskCreate, SubtaskUpdate, SubtaskResponse

router = APIRouter(prefix="/tasks/{task_id}/subtasks", tags=["Subtasks"])

@router.get("", response_model=List[SubtaskResponse])
def get_subtasks(
    task_id: int,
    subtask_service: SubtaskService = Depends()
):
    """Получить список подзадач для задачи"""
    return subtask_service.get_subtasks(task_id)

@router.post("", response_model=SubtaskResponse, status_code=201)
def create_subtask(
    task_id: int,
    subtask: SubtaskCreate,
    subtask_service: SubtaskService = Depends()
):
    """Создать новую подзадачу"""
    return subtask_service.create(task_id, subtask)

@router.put("/{subtask_id}", response_model=SubtaskResponse)
def update_subtask(
    task_id: int,
    subtask_id: int,
    subtask: SubtaskUpdate,
    subtask_service: SubtaskService = Depends()
):
    """Обновить подзадачу"""
    return subtask_service.update(subtask_id, subtask)

@router.delete("/{subtask_id}", status_code=204)
def delete_subtask(
    task_id: int,
    subtask_id: int,
    subtask_service: SubtaskService = Depends()
):
    """Удалить подзадачу"""
    subtask_service.delete(subtask_id)
    return None
```
