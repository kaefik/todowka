# L2-38 — Создать SubtaskService (CRUD)

## Цель
Определить SubtaskService с бизнес-логикой.

## Вход
Subtask репозиторий (L1-31), Subtask схемы (L1-23).

## Выход
app/services/subtask.py.

## Готово когда
SubtaskService с методами CRUD плюс get_subtasks.

## Подсказка для LLM
Создайте app/services/subtask.py с классом SubtaskService. Методы: __init__(self, subtask_repo: SubtaskRepository), create(self, task_id: int, title: str, order: Optional[int] = None) -> SubtaskResponse (проверяет что task_id существует), get_subtasks(self, task_id: int) -> List[SubtaskResponse], get_by_id(self, id: int) -> SubtaskResponse (бросает NotFoundException), update(self, id: int, **kwargs) -> SubtaskResponse, delete(self, id: int).

## Оценка усилия
S

## Файлы для создания
- app/services/subtask.py

## Класс SubtaskService
```python
from typing import List
from app.repositories.subtask import SubtaskRepository
from app.repositories.task import TaskRepository
from app.schemas.subtask import SubtaskCreate, SubtaskUpdate, SubtaskResponse
from app.exceptions import NotFoundException

class SubtaskService:
    def __init__(self, subtask_repo: SubtaskRepository, task_repo: TaskRepository):
        self.subtask_repo = subtask_repo
        self.task_repo = task_repo

    def create(self, task_id: int, data: SubtaskCreate) -> SubtaskResponse:
        # Проверяем что задача существует
        if not self.task_repo.exists(task_id):
            raise NotFoundException(f"Task with id {task_id} not found")

        subtask = self.subtask_repo.create(
            task_id=task_id,
            title=data.title,
            order=data.order
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

    def update(self, id: int, data: SubtaskUpdate) -> SubtaskResponse:
        if not self.subtask_repo.exists(id):
            raise NotFoundException(f"Subtask with id {id} not found")
        updated = self.subtask_repo.update(id, **data.model_dump(exclude_unset=True))
        return SubtaskResponse.model_validate(updated)

    def delete(self, id: int) -> None:
        if not self.subtask_repo.exists(id):
            raise NotFoundException(f"Subtask with id {id} not found")
        self.subtask_repo.delete(id)
```
