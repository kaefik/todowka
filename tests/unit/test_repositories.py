import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.models.base import Base
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.project import Project, ProjectStatus
from app.models.tag import Tag
from app.models.context import Context
from app.models.area import Area
from app.models.subtask import Subtask
from app.models.notification import Notification, NotificationStatus
from app.repositories.tag import TagRepository
from app.repositories.context import ContextRepository
from app.repositories.area import AreaRepository
from app.repositories.project import ProjectRepository
from app.repositories.subtask import SubtaskRepository
from app.repositories.notification import NotificationRepository
from app.repositories.task import TaskRepository
from datetime import datetime


engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_base_repository_create(db: Session):
    from app.repositories.base import BaseRepository
    repo = BaseRepository(db, Tag)
    tag = repo.create(name="Test Tag")
    assert tag.id is not None
    assert tag.name == "Test Tag"


def test_tag_repository_get_by_name(db: Session):
    repo = TagRepository(db)
    tag = repo.create(name="Work")
    found = repo.get_by_name("Work")
    assert found is not None
    assert found.name == "Work"


def test_tag_repository_get_or_create(db: Session):
    repo = TagRepository(db)
    tag1 = repo.get_or_create("Work", "#FF0000")
    tag2 = repo.get_or_create("Work", "#00FF00")
    assert tag1.id == tag2.id
    assert tag1.color == "#FF0000"


def test_task_repository_get_filtered(db: Session):
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)

    project = project_repo.create(name="Test Project")
    task_repo.create(title="Task 1", status=TaskStatus.ACTIVE, project_id=project.id)
    task_repo.create(title="Task 2", status=TaskStatus.INBOX)

    tasks, total = task_repo.get_filtered({'project_id': project.id, 'limit': 10, 'offset': 0})
    assert len(tasks) == 1
    assert tasks[0].title == "Task 1"


def test_task_repository_get_next_actions(db: Session):
    task_repo = TaskRepository(db)

    task_repo.create(title="Normal Task", is_next_action=False)
    task_repo.create(title="Next Action", is_next_action=True)

    next_actions = task_repo.get_next_actions()
    assert len(next_actions) == 1
    assert next_actions[0].title == "Next Action"


def test_task_repository_get_inbox(db: Session):
    task_repo = TaskRepository(db)

    task_repo.create(title="Inbox Task", status=TaskStatus.INBOX)
    task_repo.create(title="Active Task", status=TaskStatus.ACTIVE)

    inbox_tasks = task_repo.get_inbox()
    assert len(inbox_tasks) == 1
    assert inbox_tasks[0].title == "Inbox Task"


def test_task_repository_get_waiting(db: Session):
    task_repo = TaskRepository(db)

    task_repo.create(title="Waiting Task", status=TaskStatus.WAITING)
    task_repo.create(title="Active Task", status=TaskStatus.ACTIVE)

    waiting_tasks = task_repo.get_waiting()
    assert len(waiting_tasks) == 1
    assert waiting_tasks[0].title == "Waiting Task"


def test_task_repository_get_someday(db: Session):
    task_repo = TaskRepository(db)

    task_repo.create(title="Someday Task", someday=True)
    task_repo.create(title="Normal Task", someday=False)

    someday_tasks = task_repo.get_someday()
    assert len(someday_tasks) == 1
    assert someday_tasks[0].title == "Someday Task"


def test_project_repository_get_by_status(db: Session):
    project_repo = ProjectRepository(db)

    project_repo.create(name="Active Project", status=ProjectStatus.ACTIVE)
    project_repo.create(name="Completed Project", status=ProjectStatus.COMPLETED)

    active_projects = project_repo.get_by_status(ProjectStatus.ACTIVE)
    assert len(active_projects) == 1
    assert active_projects[0].name == "Active Project"


def test_project_repository_update_progress(db: Session):
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)

    project = project_repo.create(name="Test Project")
    task_repo.create(title="Task 1", project_id=project.id, completed=True)
    task_repo.create(title="Task 2", project_id=project.id, completed=False)

    updated = project_repo.update_progress(project.id)
    assert updated.progress == 50


def test_subtask_repository_get_by_task(db: Session):
    task_repo = TaskRepository(db)
    subtask_repo = SubtaskRepository(db)

    task = task_repo.create(title="Main Task")
    subtask_repo.create(task_id=task.id, title="Subtask 1")
    subtask_repo.create(task_id=task.id, title="Subtask 2")

    subtasks = subtask_repo.get_by_task(task.id)
    assert len(subtasks) == 2


def test_notification_repository_get_pending(db: Session):
    notification_repo = NotificationRepository(db)

    notification_repo.create(task_id=1, message="Pending", scheduled_at=datetime.now(), status=NotificationStatus.PENDING)
    notification_repo.create(task_id=2, message="Sent", scheduled_at=datetime.now(), status=NotificationStatus.SENT)

    pending = notification_repo.get_pending()
    assert len(pending) == 1
    assert pending[0].message == "Pending"


def test_notification_repository_mark_sent(db: Session):
    notification_repo = NotificationRepository(db)

    notification = notification_repo.create(task_id=1, message="Test", scheduled_at=datetime.now(), status=NotificationStatus.PENDING)

    updated = notification_repo.mark_sent(notification.id)
    assert updated.status == NotificationStatus.SENT


def test_notification_repository_mark_failed(db: Session):
    notification_repo = NotificationRepository(db)

    notification = notification_repo.create(task_id=1, message="Test", scheduled_at=datetime.now(), status=NotificationStatus.PENDING)

    updated = notification_repo.mark_failed(notification.id, "Error")
    assert updated.status == NotificationStatus.FAILED
    assert "[Error:" in updated.message


def test_context_repository_crud(db: Session):
    repo = ContextRepository(db)
    context = repo.create(name="@Office", color="#0000FF")
    assert context.id is not None

    found = repo.get(context.id)
    assert found.name == "@Office"

    updated = repo.update(context.id, name="@Home")
    assert updated.name == "@Home"

    repo.delete(context.id)
    assert not repo.exists(context.id)


def test_area_repository_crud(db: Session):
    repo = AreaRepository(db)
    area = repo.create(name="Work", description="Professional life")
    assert area.id is not None

    found = repo.get(area.id)
    assert found.name == "Work"
    assert found.description == "Professional life"
