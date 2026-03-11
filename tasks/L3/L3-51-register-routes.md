# L3-51 — Зарегистрировать все routes в main.py с APIRouter

## Цель
Примонтировать все API routes в FastAPI app.

## Вход
Все файлы routes (L3-42 через L3-50).

## Выход
Обновлённый app/main.py со всеми зарегистрированными routers.

## Готово когда
Все routers примонтированы под префиксом /api/v1.

## Подсказка для LLM
В app/main.py импортируйте все routers из app.routes.tasks, app.routes.projects, app.routes.subtasks, app.routes.tags, app.routes.contexts, app.routes.areas, app.routes.notifications, app.routes.inbox. Зарегистрируйте каждый router с app.include_router(router, prefix="/api/v1", tags=["Tasks"], и т.д.). Добавьте GET / root endpoint возвращающий {"message": "Todo API", "docs": "/docs"}.

## Оценка усилия
S

## Файлы для изменения
- app/main.py

## Обновление main.py
```python
from fastapi import FastAPI
from app.middleware.error_handler import register_exception_handlers
from app.routes.tasks import router as tasks_router
from app.routes.projects import router as projects_router
from app.routes.subtasks import router as subtasks_router
from app.routes.tags import router as tags_router
from app.routes.contexts import router as contexts_router
from app.routes.areas import router as areas_router
from app.routes.notifications import router as notifications_router
from app.routes.inbox import router as inbox_router

app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="REST API для управления задачами с поддержкой GTD методологии"
)

# Регистрация обработчиков ошибок
register_exception_handlers(app)

# Регистрация routers
app.include_router(tags_router, prefix="/api/v1")
app.include_router(contexts_router, prefix="/api/v1")
app.include_router(areas_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
app.include_router(subtasks_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")
app.include_router(inbox_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")

# Root endpoint
@app.get("/")
def root():
    """Корневой endpoint с информацией о API"""
    return {
        "message": "Todo API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }
```

## Примечание
После этой задачи все API endpoints будут доступны по префиксу /api/v1.
Swagger UI будет доступен по /docs.
