from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings
from app.repositories.tag import TagRepository
from app.repositories.context import ContextRepository
from app.repositories.area import AreaRepository
from app.repositories.project import ProjectRepository
from app.repositories.task import TaskRepository
from app.repositories.subtask import SubtaskRepository
from app.repositories.notification import NotificationRepository
from app.services.tag import TagService
from app.services.context import ContextService
from app.services.area import AreaService
from app.services.project import ProjectService
from app.services.task import TaskService
from app.services.subtask import SubtaskService
from app.services.notification import NotificationService


engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    task_repo = TaskRepository(db)
    tag_repo = TagRepository(db)
    project_repo = ProjectRepository(db)
    subtask_repo = SubtaskRepository(db)
    notification_repo = NotificationRepository(db)

    tag_service = TagService(tag_repo, task_repo, db)
    project_service = ProjectService(project_repo, task_repo)
    subtask_service = SubtaskService(subtask_repo, task_repo)
    notification_service = NotificationService(notification_repo)

    return TaskService(task_repo, tag_service, project_service, subtask_service, notification_service)


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    return ProjectService(project_repo, task_repo)


def get_subtask_service(db: Session = Depends(get_db)) -> SubtaskService:
    subtask_repo = SubtaskRepository(db)
    task_repo = TaskRepository(db)
    return SubtaskService(subtask_repo, task_repo)


def get_tag_service(db: Session = Depends(get_db)) -> TagService:
    tag_repo = TagRepository(db)
    task_repo = TaskRepository(db)
    return TagService(tag_repo, task_repo, db)


def get_context_service(db: Session = Depends(get_db)) -> ContextService:
    context_repo = ContextRepository(db)
    return ContextService(context_repo)


def get_area_service(db: Session = Depends(get_db)) -> AreaService:
    area_repo = AreaRepository(db)
    return AreaService(area_repo)


def get_notification_service(db: Session = Depends(get_db)) -> NotificationService:
    notification_repo = NotificationRepository(db)
    return NotificationService(notification_repo)
