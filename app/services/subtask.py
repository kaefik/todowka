from typing import List
from app.repositories.subtask import SubtaskRepository
from app.repositories.task import TaskRepository
from app.schemas.subtask import SubtaskCreate, SubtaskUpdate, SubtaskResponse
from app.exceptions import NotFoundException


class SubtaskService:
    def __init__(self, subtask_repo: SubtaskRepository, task_repo: TaskRepository):
        self.subtask_repo = subtask_repo
        self.task_repo = task_repo

    def create(self, task_id: int, title: str, order: int = None) -> SubtaskResponse:
        if not self.task_repo.exists(task_id):
            raise NotFoundException(f"Task with id {task_id} not found")

        subtask = self.subtask_repo.create(
            task_id=task_id,
            title=title,
            order=order
        )
        return SubtaskResponse.model_validate(subtask)

    def get_subtasks(self, task_id: int) -> List[SubtaskResponse]:
        subtasks = self.subtask_repo.get_by_task(task_id)
        return [SubtaskResponse.model_validate(st) for st in subtasks]

    def get_by_id(self, id: int) -> SubtaskResponse:
        subtask = self.subtask_repo.get(id)
        if not subtask:
            raise NotFoundException(f"Subtask with id {id} not found")
        return SubtaskResponse.model_validate(subtask)

    def update(self, id: int, title: str = None, completed: bool = None, order: int = None) -> SubtaskResponse:
        if not self.subtask_repo.exists(id):
            raise NotFoundException(f"Subtask with id {id} not found")

        update_data = {}
        if title is not None:
            update_data['title'] = title
        if completed is not None:
            update_data['completed'] = completed
        if order is not None:
            update_data['order'] = order

        updated = self.subtask_repo.update(id, **update_data)
        return SubtaskResponse.model_validate(updated)

    def delete(self, id: int) -> None:
        if not self.subtask_repo.exists(id):
            raise NotFoundException(f"Subtask with id {id} not found")
        self.subtask_repo.delete(id)
