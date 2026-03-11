from fastapi import APIRouter, Depends
from app.services.subtask import SubtaskService
from app.schemas.subtask import SubtaskCreate, SubtaskUpdate, SubtaskResponse
from app.dependencies import get_subtask_service

router = APIRouter(prefix="/tasks/{task_id}/subtasks", tags=["Subtasks"])

@router.get("", response_model=list[SubtaskResponse])
def get_subtasks(
    task_id: int,
    subtask_service: SubtaskService = Depends(get_subtask_service)
):
    return subtask_service.get_subtasks(task_id)

@router.post("", response_model=SubtaskResponse, status_code=201)
def create_subtask(
    task_id: int,
    subtask: SubtaskCreate,
    subtask_service: SubtaskService = Depends(get_subtask_service)
):
    return subtask_service.create(task_id, subtask.title, subtask.order)

@router.put("/{subtask_id}", response_model=SubtaskResponse)
def update_subtask(
    task_id: int,
    subtask_id: int,
    subtask: SubtaskUpdate,
    subtask_service: SubtaskService = Depends(get_subtask_service)
):
    return subtask_service.update(
        subtask_id,
        subtask.title,
        subtask.completed,
        subtask.order
    )

@router.delete("/{subtask_id}", status_code=204)
def delete_subtask(
    task_id: int,
    subtask_id: int,
    subtask_service: SubtaskService = Depends(get_subtask_service)
):
    subtask_service.delete(subtask_id)
