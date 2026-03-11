# L7-55 — Создать unit-тесты для репозиториев

## Цель
Написать unit-тесты для всех классов репозиториев.

## Вход
Все репозитории (L1-26 через L1-33).

## Выход
tests/unit/test_repositories.py с тестами репозиториев.

## Готово когда
Каждый репозиторий имеет тесты для всех методов покрывающие success и error случаи.

## Подсказка для LLM
Создайте tests/unit/test_repositories.py используя pytest. Создайте in-memory SQLite базу данных для тестирования. Напишите тесты для методов BaseRepository. Напишите тесты для каждого специфичного репозитория: TagRepository (test_get_by_name, test_get_or_create), TaskRepository (test_get_filtered, test_get_next_actions и т.д.), ProjectRepository (test_get_by_status, test_update_progress), SubtaskRepository (test_get_by_task), TagRepository, ContextRepository, AreaRepository, NotificationRepository (test_get_pending, test_mark_sent, test_mark_failed). Используйте fixtures для database session.

## Оценка усилия
L

## Файлы для создания
- tests/unit/test_repositories.py
- tests/unit/conftest.py (для fixtures)

## Структура тестов
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.models.base import Base
from app.models.task import Task
from app.models.project import Project
from app.models.tag import Tag
from app.models.context import Context
from app.models.area import Area
from app.models.subtask import Subtask
from app.models.notification import Notification
from app.repositories.tag import TagRepository
from app.repositories.context import ContextRepository
from app.repositories.area import AreaRepository
from app.repositories.project import ProjectRepository
from app.repositories.subtask import SubtaskRepository
from app.repositories.notification import NotificationRepository
from app.repositories.task import TaskRepository

# In-memory SQLite для тестов
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """Создаёт новую сессию БД для каждого теста"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# ===== BaseRepository Tests =====
def test_base_repository_create(db: Session):
    """Тест создания записи через BaseRepository"""
    from app.repositories.base import BaseRepository
    repo = BaseRepository(db, Tag)
    tag = repo.create(name="Test Tag")
    assert tag.id is not None
    assert tag.name == "Test Tag"

# ===== TagRepository Tests =====
def test_tag_repository_get_by_name(db: Session):
    """Тест поиска тега по имени"""
    repo = TagRepository(db)
    tag = repo.create(name="Work")
    found = repo.get_by_name("Work")
    assert found is not None
    assert found.name == "Work"

def test_tag_repository_get_or_create(db: Session):
    """Тест получения или создания тега"""
    repo = TagRepository(db)
    # Создаём
    tag1 = repo.get_or_create("Work", "#FF0000")
    # Получаем существующий
    tag2 = repo.get_or_create("Work", "#00FF00")
    assert tag1.id == tag2.id
    assert tag1.color == "#FF0000"  # Цвет не обновляется

# ===== TaskRepository Tests =====
def test_task_repository_get_filtered(db: Session):
    """Тест фильтрации задач"""
    from app.models.project import Project
    from app.models.task import TaskStatus

    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)

    # Создаём проект и задачи
    project = project_repo.create(name="Test Project")
    task_repo.create(title="Task 1", status=TaskStatus.ACTIVE, project_id=project.id)
    task_repo.create(title="Task 2", status=TaskStatus.INBOX)

    # Фильтруем по project_id
    tasks, total = task_repo.get_filtered({'project_id': project.id, 'limit': 10, 'offset': 0})
    assert len(tasks) == 1
    assert tasks[0].title == "Task 1"

def test_task_repository_get_next_actions(db: Session):
    """Тест получения next actions"""
    task_repo = TaskRepository(db)

    task_repo.create(title="Normal Task", is_next_action=False)
    task_repo.create(title="Next Action", is_next_action=True)

    next_actions = task_repo.get_next_actions()
    assert len(next_actions) == 1
    assert next_actions[0].title == "Next Action"

# ===== ProjectRepository Tests =====
def test_project_repository_get_by_status(db: Session):
    """Тест получения проектов по статусу"""
    project_repo = ProjectRepository(db)

    project_repo.create(name="Active Project", status="active")
    project_repo.create(name="Completed Project", status="completed")

    active_projects = project_repo.get_by_status("active")
    assert len(active_projects) == 1
    assert active_projects[0].name == "Active Project"

# ===== SubtaskRepository Tests =====
def test_subtask_repository_get_by_task(db: Session):
    """Тест получения подзадач задачи"""
    from app.models.task import Task
    task_repo = TaskRepository(db)
    subtask_repo = SubtaskRepository(db)

    task = task_repo.create(title="Main Task")
    subtask_repo.create(task_id=task.id, title="Subtask 1")
    subtask_repo.create(task_id=task.id, title="Subtask 2")

    subtasks = subtask_repo.get_by_task(task.id)
    assert len(subtasks) == 2

# ===== NotificationRepository Tests =====
def test_notification_repository_get_pending(db: Session):
    """Тест получения ожидающих уведомлений"""
    from app.models.notification import NotificationStatus
    notification_repo = NotificationRepository(db)

    notification_repo.create(task_id=1, message="Pending", scheduled_at=datetime.now(), status=NotificationStatus.PENDING)
    notification_repo.create(task_id=2, message="Sent", scheduled_at=datetime.now(), status=NotificationStatus.SENT)

    pending = notification_repo.get_pending()
    assert len(pending) == 1
    assert pending[0].message == "Pending"

# ===== ContextRepository Tests =====
def test_context_repository_crud(db: Session):
    """Тест CRUD для ContextRepository"""
    repo = ContextRepository(db)
    context = repo.create(name="@Office", color="#0000FF")
    assert context.id is not None

    found = repo.get(context.id)
    assert found.name == "@Office"

    updated = repo.update(context.id, name="@Home")
    assert updated.name == "@Home"

    repo.delete(context.id)
    assert not repo.exists(context.id)

# ===== AreaRepository Tests =====
def test_area_repository_crud(db: Session):
    """Тест CRUD для AreaRepository"""
    repo = AreaRepository(db)
    area = repo.create(name="Work", description="Professional life")
    assert area.id is not None

    found = repo.get(area.id)
    assert found.name == "Work"
    assert found.description == "Professional life"
```

## Запуск тестов

```bash
# Запуск unit-тестов для репозиториев
pytest tests/unit/test_repositories.py -v

# С покрытием кода
pytest tests/unit/test_repositories.py --cov=app.repositories --cov-report=html
```
