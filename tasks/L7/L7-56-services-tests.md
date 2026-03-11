# L7-56 — Создать unit-тесты для сервисов

## Цель
Написать unit-тесты для всех классов сервисов.

## Вход
Все сервисы (L2-34 через L2-41).

## Выход
tests/unit/test_services.py с тестами сервисов.

## Готово когда
Каждый сервис имеет тесты для всех методов покрывающие бизнес-логику и error случаи.

## Подсказка для LLM
Создайте tests/unit/test_services.py используя pytest. Напишите тесты для каждого сервиса: TagService (test_create, test_get_by_id_raises_not_found, test_assign_tags), ContextService, AreaService, ProjectService (test_complete_project, test_update_progress), SubtaskService (test_create_with_invalid_task_id), NotificationService (test_create_notification), TaskService (test_create_task_with_tags, test_toggle_complete, test_set_next_action, test_schedule_reminder, test_set_waiting, test_get_tasks_with_filters). Мокайте репозитории в сервисных тестах.

## Оценка усилия
L

## Файлы для создания
- tests/unit/test_services.py

## Структура тестов
```python
import pytest
from datetime import datetime
from unittest.mock import Mock, MagicMock
from app.services.tag import TagService
from app.services.context import ContextService
from app.services.area import AreaService
from app.services.project import ProjectService
from app.services.subtask import SubtaskService
from app.services.notification import NotificationService
from app.services.task import TaskService
from app.exceptions import NotFoundException
from app.schemas.tag import TagCreate
from app.schemas.context import ContextCreate
from app.schemas.area import AreaCreate
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.schemas.subtask import SubtaskCreate, SubtaskUpdate
from app.schemas.notification import NotificationCreate
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.tag import Tag
from app.models.context import Context
from app.models.area import Area
from app.models.project import Project
from app.models.task import Task

# ===== TagService Tests =====
def test_tag_service_create():
    """Тест создания тега"""
    mock_tag_repo = Mock()
    mock_task_repo = Mock()
    mock_db = Mock()

    tag = Tag(id=1, name="Work", color="#FF0000")
    mock_tag_repo.create.return_value = tag

    service = TagService(mock_tag_repo, mock_task_repo, mock_db)
    result = service.create("Work", "#FF0000")

    assert result.id == 1
    assert result.name == "Work"
    mock_tag_repo.create.assert_called_once_with(name="Work", color="#FF0000")

def test_tag_service_get_by_id_not_found():
    """Тест получения несуществующего тега"""
    mock_tag_repo = Mock()
    mock_task_repo = Mock()
    mock_db = Mock()

    mock_tag_repo.get.return_value = None

    service = TagService(mock_tag_repo, mock_task_repo, mock_db)

    with pytest.raises(NotFoundException) as exc_info:
        service.get_by_id(999)

    assert "not found" in str(exc_info.value)

def test_tag_service_assign_tags():
    """Тест назначения тегов задаче"""
    mock_tag_repo = Mock()
    mock_task_repo = Mock()
    mock_db = Mock()

    task = Mock(id=1, tags=[])
    tag = Tag(id=1, name="Work")
    mock_task_repo.get.return_value = task
    mock_tag_repo.get.return_value = tag

    service = TagService(mock_tag_repo, mock_task_repo, mock_db)
    service.assign_tags(1, [1])

    assert tag in task.tags
    mock_db.commit.assert_called_once()

# ===== ContextService Tests =====
def test_context_service_create():
    """Тест создания контекста"""
    mock_context_repo = Mock()
    context = Context(id=1, name="@Office", icon="🏢", color="#0000FF")
    mock_context_repo.create.return_value = context

    service = ContextService(mock_context_repo)
    result = service.create("@Office", "🏢", "#0000FF")

    assert result.id == 1
    assert result.name == "@Office"

# ===== AreaService Tests =====
def test_area_service_create():
    """Тест создания области"""
    mock_area_repo = Mock()
    area = Area(id=1, name="Work", description="Professional life", color="#FF0000")
    mock_area_repo.create.return_value = area

    service = AreaService(mock_area_repo)
    result = service.create("Work", "Professional life", "#FF0000")

    assert result.id == 1
    assert result.name == "Work"

# ===== ProjectService Tests =====
def test_project_service_create():
    """Тест создания проекта"""
    mock_project_repo = Mock()
    mock_task_repo = Mock()
    project = Project(id=1, name="New Project")
    mock_project_repo.create.return_value = project

    service = ProjectService(mock_project_repo, mock_task_repo)
    result = service.create(ProjectCreate(name="New Project"))

    assert result.id == 1
    assert result.name == "New Project"

def test_project_service_complete_project():
    """Тест завершения проекта"""
    mock_project_repo = Mock()
    mock_task_repo = Mock()
    project = Project(id=1, name="Test Project")
    task1 = Task(id=1, title="Task 1", completed=False)
    task2 = Task(id=2, title="Task 2", completed=False)

    mock_project_repo.get.return_value = project
    mock_project_repo.update.return_value = project
    mock_task_repo.get_filtered.return_value = ([task1, task2], 2)

    service = ProjectService(mock_project_repo, mock_task_repo)
    result = service.complete_project(1)

    # Проверяем что задачи помечены как завершённые
    assert mock_task_repo.update.call_count == 2

# ===== SubtaskService Tests =====
def test_subtask_service_create_with_invalid_task_id():
    """Тест создания подзадачи с несуществующей задачей"""
    mock_subtask_repo = Mock()
    mock_task_repo = Mock()
    mock_task_repo.exists.return_value = False

    service = SubtaskService(mock_subtask_repo, mock_task_repo)

    with pytest.raises(NotFoundException) as exc_info:
        service.create(999, SubtaskCreate(title="Test Subtask"))

    assert "not found" in str(exc_info.value)

# ===== NotificationService Tests =====
def test_notification_service_create():
    """Тест создания уведомления"""
    mock_notification_repo = Mock()
    notification = Mock(id=1, task_id=1, message="Test", scheduled_at=datetime.now())
    mock_notification_repo.create.return_value = notification

    service = NotificationService(mock_notification_repo)
    result = service.create_notification(
        NotificationCreate(task_id=1, message="Test", scheduled_at=datetime.now())
    )

    assert result.id == 1

# ===== TaskService Tests =====
def test_task_service_create_with_tags():
    """Тест создания задачи с тегами"""
    mock_task_repo = Mock()
    mock_tag_service = Mock()
    mock_project_service = Mock()
    mock_subtask_service = Mock()
    mock_notification_service = Mock()

    task = Task(id=1, title="Test Task")
    mock_task_repo.create.return_value = task
    mock_project_service.project_repo.exists.return_value = False

    service = TaskService(
        mock_task_repo, mock_tag_service,
        mock_project_service, mock_subtask_service,
        mock_notification_service
    )

    data = TaskCreate(title="Test Task", tag_ids=[1, 2])
    result = service.create_task(data)

    mock_tag_service.assign_tags.assert_called_once_with(1, [1, 2])

def test_task_service_toggle_complete():
    """Тест переключения завершения задачи"""
    mock_task_repo = Mock()
    mock_tag_service = Mock()
    mock_project_service = Mock()
    mock_subtask_service = Mock()
    mock_notification_service = Mock()

    task = Task(id=1, title="Test Task", completed=False)
    mock_task_repo.get.return_value = task
    mock_task_repo.update.return_value = Task(id=1, title="Test Task", completed=True)

    service = TaskService(
        mock_task_repo, mock_tag_service,
        mock_project_service, mock_subtask_service,
        mock_notification_service
    )

    result = service.toggle_complete(1)

    mock_task_repo.update.assert_called_once_with(1, completed=True)

def test_task_service_set_next_action():
    """Тест установки флага следующего действия"""
    mock_task_repo = Mock()
    mock_tag_service = Mock()
    mock_project_service = Mock()
    mock_subtask_service = Mock()
    mock_notification_service = Mock()

    task = Task(id=1, title="Test Task")
    mock_task_repo.get.return_value = task
    mock_task_repo.update.return_value = Task(id=1, title="Test Task", is_next_action=True)

    service = TaskService(
        mock_task_repo, mock_tag_service,
        mock_project_service, mock_subtask_service,
        mock_notification_service
    )

    result = service.set_next_action(1, True)

    mock_task_repo.update.assert_called_once_with(1, is_next_action=True)

def test_task_service_schedule_reminder():
    """Тест планирования напоминания"""
    mock_task_repo = Mock()
    mock_tag_service = Mock()
    mock_project_service = Mock()
    mock_subtask_service = Mock()
    mock_notification_service = Mock()

    task = Task(id=1, title="Test Task", reminder_time=None)
    mock_task_repo.get.return_value = task
    mock_task_repo.update.return_value = Task(id=1, title="Test Task", reminder_time=datetime.now())
    mock_notification_service.create_notification.return_value = Mock(id=1)

    service = TaskService(
        mock_task_repo, mock_tag_service,
        mock_project_service, mock_subtask_service,
        mock_notification_service
    )

    reminder_time = datetime.now()
    result = service.schedule_reminder(1, reminder_time)

    # Проверяем что reminder_time обновлён и уведомление создано
    mock_task_repo.update.assert_called_once_with(1, reminder_time=reminder_time)
    mock_notification_service.create_notification.assert_called_once()

def test_task_service_get_tasks_with_filters():
    """Тест получения задач с фильтрами"""
    mock_task_repo = Mock()
    mock_tag_service = Mock()
    mock_project_service = Mock()
    mock_subtask_service = Mock()
    mock_notification_service = Mock()

    task1 = Task(id=1, title="Task 1")
    task2 = Task(id=2, title="Task 2")
    mock_task_repo.get_filtered.return_value = ([task1, task2], 2)

    service = TaskService(
        mock_task_repo, mock_tag_service,
        mock_project_service, mock_subtask_service,
        mock_notification_service
    )

    result = service.get_tasks(page=1, size=10, status="active")

    assert result.total == 2
    assert len(result.items) == 2
    mock_task_repo.get_filtered.assert_called_once()
```

## Запуск тестов

```bash
# Запуск unit-тестов для сервисов
pytest tests/unit/test_services.py -v

# С покрытием кода
pytest tests/unit/test_services.py --cov=app.services --cov-report=html

# Все unit-тесты
pytest tests/unit/ -v
```
