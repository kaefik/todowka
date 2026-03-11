from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.middleware.error_handler import register_exception_handlers
from app.dependencies import get_db
from app.config import settings
from app.models.base import Base
from app.models.tag import Tag
from app.models.context import Context
from app.models.area import Area
from app.models.project import Project
from app.models.task import Task, task_tags
from app.models.subtask import Subtask
from app.models.notification import Notification
from app.dependencies import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="REST API для управления задачами с поддержкой GTD методологии",
    lifespan=lifespan
)

register_exception_handlers(app)

@app.get("/api/v1/health")
def health_check():
    """Проверка здоровья API и подключения к БД"""
    try:
        from app.dependencies import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "error": str(e)}
