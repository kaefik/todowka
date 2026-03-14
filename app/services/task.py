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
        task = self.task_repo.get(id)
        if not task:
            raise NotFoundException(f"Task with id {id} not found")
        return TaskResponse.model_validate(task)

    def get_next_actions(self) -> list[TaskResponse]:
        tasks = self.task_repo.get_next_actions()
        return [TaskResponse.model_validate(task) for task in tasks]

    def create_task(self, title: str, description: Optional[str] = None, priority: Optional[str] = None,
                    due_date: Optional[datetime] = None, reminder_time: Optional[datetime] = None,
                    project_id: Optional[int] = None, context_id: Optional[int] = None, area_id: Optional[int] = None,
                    tag_ids: Optional[list] = None, status: Optional[str] = None, is_next_action: Optional[bool] = None,
                    waiting_for: Optional[str] = None, delegated_to: Optional[str] = None, someday: Optional[bool] = None) -> TaskResponse:
        if project_id and not self.project_service.project_repo.exists(project_id):
            raise NotFoundException(f"Project with id {project_id} not found")

        task = self.task_repo.create(
            title=title,
            description=description,
            priority=priority or "medium",
            due_date=due_date,
            reminder_time=reminder_time,
            project_id=project_id,
            context_id=context_id,
            area_id=area_id,
            status=status or "active",
            is_next_action=is_next_action or False,
            waiting_for=waiting_for,
            delegated_to=delegated_to,
            someday=someday or False
        )

        if tag_ids:
            self.tag_service.assign_tags(task.id, tag_ids)

        return self.get_task(task.id)

    def update_task(self, id: int, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None,
                    priority: Optional[str] = None, due_date: Optional[datetime] = None, reminder_time: Optional[datetime] = None,
                    project_id: Optional[int] = None, context_id: Optional[int] = None, area_id: Optional[int] = None,
                    tag_ids: Optional[list] = None, status: Optional[str] = None, is_next_action: Optional[bool] = None,
                    waiting_for: Optional[str] = None, delegated_to: Optional[str] = None, someday: Optional[bool] = None) -> TaskResponse:
        if not self.task_repo.exists(id):
            raise NotFoundException(f"Task with id {id} not found")

        update_data = {}
        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description
        if completed is not None:
            update_data['completed'] = completed
        if priority is not None:
            update_data['priority'] = priority
        if due_date is not None:
            update_data['due_date'] = due_date
        if reminder_time is not None:
            update_data['reminder_time'] = reminder_time
        if project_id is not None:
            if project_id and not self.project_service.project_repo.exists(project_id):
                raise NotFoundException(f"Project with id {project_id} not found")
            update_data['project_id'] = project_id
        if context_id is not None:
            update_data['context_id'] = context_id
        if area_id is not None:
            update_data['area_id'] = area_id
        if status is not None:
            update_data['status'] = status
        if is_next_action is not None:
            update_data['is_next_action'] = is_next_action
        if waiting_for is not None:
            update_data['waiting_for'] = waiting_for
        if delegated_to is not None:
            update_data['delegated_to'] = delegated_to
        if someday is not None:
            update_data['someday'] = someday

        self.task_repo.update(id, **update_data)

        if tag_ids is not None:
            self.tag_service.assign_tags(id, tag_ids)

        return self.get_task(id)

    def patch_task(self, id: int, task_data: dict) -> TaskResponse:
        if not self.task_repo.exists(id):
            raise NotFoundException(f"Task with id {id} not found")

        update_data = {}
        if 'title' in task_data:
            update_data['title'] = task_data['title']
        if 'description' in task_data:
            update_data['description'] = task_data['description']
        if 'completed' in task_data:
            update_data['completed'] = task_data['completed']
        if 'priority' in task_data:
            update_data['priority'] = task_data['priority']
        if 'due_date' in task_data:
            update_data['due_date'] = task_data['due_date']
        if 'reminder_time' in task_data:
            update_data['reminder_time'] = task_data['reminder_time']
        if 'project_id' in task_data:
            project_id = task_data['project_id']
            if project_id and not self.project_service.project_repo.exists(project_id):
                raise NotFoundException(f"Project with id {project_id} not found")
            update_data['project_id'] = project_id
        if 'context_id' in task_data:
            update_data['context_id'] = task_data['context_id']
        if 'area_id' in task_data:
            update_data['area_id'] = task_data['area_id']
        if 'status' in task_data:
            update_data['status'] = task_data['status']
        if 'is_next_action' in task_data:
            update_data['is_next_action'] = task_data['is_next_action']
        if 'waiting_for' in task_data:
            update_data['waiting_for'] = task_data['waiting_for']
        if 'delegated_to' in task_data:
            update_data['delegated_to'] = task_data['delegated_to']
        if 'someday' in task_data:
            update_data['someday'] = task_data['someday']

        self.task_repo.update(id, **update_data)

        if 'tag_ids' in task_data:
            self.tag_service.assign_tags(id, task_data['tag_ids'])

        return self.get_task(id)

    def delete_task(self, id: int) -> None:
        if not self.task_repo.exists(id):
            raise NotFoundException(f"Task with id {id} not found")
        self.task_repo.delete(id)

    def toggle_complete(self, id: int) -> TaskResponse:
        task = self.task_repo.get(id)
        if not task:
            raise NotFoundException(f"Task with id {id} not found")

        updated = self.task_repo.update(id, completed=not task.completed)
        return TaskResponse.model_validate(updated)

    def set_next_action(self, id: int, flag: bool) -> TaskResponse:
        if not self.task_repo.exists(id):
            raise NotFoundException(f"Task with id {id} not found")

        updated = self.task_repo.update(id, is_next_action=flag)
        return TaskResponse.model_validate(updated)

    def schedule_reminder(self, id: int, time: datetime) -> TaskResponse:
        task = self.task_repo.get(id)
        if not task:
            raise NotFoundException(f"Task with id {id} not found")

        self.task_repo.update(id, reminder_time=time)

        self.notification_service.create_notification(
            id,
            f"Reminder: {task.title}",
            time
        )

        return self.get_task(id)

    def set_waiting(self, id: int, waiting_for: str) -> TaskResponse:
        if not self.task_repo.exists(id):
            raise NotFoundException(f"Task with id {id} not found")

        updated = self.task_repo.update(
            id,
            status="waiting",
            waiting_for=waiting_for
        )
        return TaskResponse.model_validate(updated)
