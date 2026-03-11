from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.error_handler import register_exception_handlers
from app.middleware.logging import LoggingMiddleware
from app.dependencies import engine
from app.routes.tags import router as tags_router
from app.routes.contexts import router as contexts_router
from app.routes.areas import router as areas_router
from app.routes.projects import router as projects_router
from app.routes.subtasks import router as subtasks_router
from app.routes.notifications import router as notifications_router
from app.routes.inbox import router as inbox_router
from app.routes.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.models.base import Base
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="REST API для управления задачами с поддержкой GTD методологии",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

register_exception_handlers(app)

app.include_router(tags_router, prefix="/api/v1")
app.include_router(contexts_router, prefix="/api/v1")
app.include_router(areas_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
app.include_router(subtasks_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")
app.include_router(inbox_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Todo API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


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
