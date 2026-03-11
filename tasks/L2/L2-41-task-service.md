# L2-41 — Создать TaskService (CRUD + операции GTD)

## Цель
Определить TaskService с CRUD и GTD-операциями.

## Вход
Task репозиторий (L1-33), TagService (L2-34), ProjectService (L2-37), SubtaskService (L2-38), NotificationService (L2-39), Task схемы (L1-25).

## Выход
app/services/task.py.

## Готово когда
TaskService с методами CRUD, toggle_complete, set_next_action, schedule_reminder, set_waiting.

## Подсказка для LLM
Создайте app/services/task.py с классом TaskService. Методы: __init__(self, task_repo: TaskRepository, tag_service: TagService, project_service: ProjectService, subtask_service: SubtaskService, notification_service: NotificationService), get_tasks(self, page: int, size: int, filters: dict) -> PaginationResponse[TaskResponse], get_task(self, id: int) -> TaskResponse (бросает NotFoundException), create_task(self, data: TaskCreate) -> TaskResponse (назначает теги через tag_service), update_task(self, id: int, data: TaskUpdate) -> TaskResponse, delete_task(self, id: int), toggle_complete(self, id: int) -> TaskResponse, set_next_action(self, id: int, flag: bool) -> TaskResponse, schedule_reminder(self, id: int, time: datetime) -> TaskResponse (создаёт уведомление через notification_service), set_waiting(self, id: int, waiting_for: str) -> TaskResponse.

## Оценка усилия
L

## Файлы для создания
- app/services/task.py

## Класс TaskService
```python
from typing import Optional
from datetime import datetime
from app.repositories.task import TaskRepository
from app.services.tag import TagService
from app.services.project import ProjectService
from app.services.subtask import SubtaskService
from app.services.notification import NotificationService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.pagination import PaginationResponse
from app.exceptions import NotFoundException

class TaskService:
    def __init__(
        self,
        task_repo: TaskRepository,
        tag_service: TagService,
        project_service: ProjectService,
        subtask_service: SubtaskService,
        notification_service: NotificationService
    ):
        self.task_repo = task_repo
        self.tag_service = tag_service
        self.project_service = project_service
        self.subtask_service = subtask_service
        self.notification_service = notification_service

    def get_tasks(self, page: int, size: int, **filters) -> PaginationResponse[TaskResponse]:
        """Получает список задач с пагинацией и фильтрацией"""
        filters['limit'] = size
        filters['offset'] = (page - 1) * size

        tasks, total = self.task_repo.get_filtered(filters)
        items = [TaskResponse.model_validate(task) for task in tasks]

        return PaginationResponse(
            items=items,
            total=total,
            page=page,
            size=size
        )

    def get_task(self, id: int) -> TaskResponse:
        """Получает задачу по ID"""
        task = self.task_repo.get(id)
        if not task:
            raise NotFoundException(f"Task with id {id} not found")
        return TaskResponse.model_validate(task)

    def create_task(self, data: TaskCreate) -> TaskResponse:
        """Создаёт новую задачу"""
        # Проверяем существование связанных сущностей
        if data.project_id and not self.project_service.project_repo.exists(data.project_id):
            raise NotFoundException(f"Project with id {data.project_id} not found")

        task = self.task_repo.create(
            title=data.title,
            description=data.description,
            priority=data.priority or "medium",
            due_date=data.due_date,
            reminder_time=data.reminder_time,
            project_id=data.project_id,
            context_id=data.context_id,
            area_id=data.area_id,
            status=data.status or "active",
            is_next_action=data.is_next_action or False,
            waiting_for=data.waiting_for,
            delegated_to=data.delegated_to,
            someday=data.someday or False
        )

        # Назначаем теги
        if data.tag_ids:
            self.tag_service.assign_tags(task.id, data.tag_ids)

        return self.get_task(task.id)

    def update_task(self, id: int, data: TaskUpdate) -> TaskResponse:
        """Обновляет задачу"""
        if not self.task_repo.exists(id):
            raise NotFoundException(f"Task with id {id} not found")

        update_data = data.model_dump(exclude_unset=True)

        # Проверяем существование связанных сущностей
        if 'project_id' in update_data and update_data['project_id']:
            if not self.project_service.project_repo.exists(update_data['project_id']):
                raise NotFoundException(f"Project with id {update_data['project_id']} not found")

        self.task_repo.update(id, **update_data)

        # Обновляем теги если указаны
        if 'tag_ids' in update_data:
            self.tag_service.assign_tags(id, update_data['tag_ids'])

        return self.get_task(id)

    def delete_task(self, id: int) -> None:
        """Удаляет задачу"""
        if not self.task_repo.exists(id):
            raise NotFoundException(f"Task with id {id} not found")
        self.task_repo.delete(id)

    def toggle_complete(self, id: int) -> TaskResponse:
        """Переключает статус завершения задачи"""
        task = self.task_repo.get(id)
        if not task:
            raise NotFoundException(f"Task with id {id} not found")

        updated = self.task_repo.update(id, completed=not task.completed)
        return TaskResponse.model_validate(updated)

    def set_next_action(self, id: int, flag: bool) -> TaskResponse:
        """Помечает задачу как следующее действие"""
        if not self.task_repo.exists(id):
            raise NotFoundException(f"Task with id {id} not found")

        updated = self.task_repo.update(id, is_next_action=flag)
        return TaskResponse.model_validate(updated)

    def schedule_reminder(self, id: int, time: datetime) -> TaskResponse:
        """Планирует напоминание для задачи"""
        task = self.task_repo.get(id)
        if not task:
            raise NotFoundException(f"Task with id {id} not found")

        # Обновляем reminder_time в задаче
        self.task_repo.update(id, reminder_time=time)

        # Создаём уведомление
        from app.schemas.notification import NotificationCreate
        self.notification_service.create_notification(
            NotificationCreate(
                task_id=id,
                message=f"Reminder: {task.title}",
                scheduled_at=time
            )
        )

        return self.get_task(id)

    def set_waiting(self, id: int, waiting_for: str) -> TaskResponse:
        """Устанавливает статус ожидания для задачи"""
        if not self.task_repo.exists(id):
            raise NotFoundException(f"Task with id {id} not found")

        updated = self.task_repo.update(
            id,
            status="waiting",
            waiting_for=waiting_for
        )
        return TaskResponse.model_validate(updated)
```
