# L0-08 — Создать main.py с настройкой FastAPI

## Цель
Инициализировать приложение FastAPI с базовой конфигурацией.

## Вход
Config (L0-02), error_handler (L0-06), dependencies (L0-07).

## Выход
app/main.py с экземпляром FastAPI app.

## Готово когда
FastAPI app создан с title "Todo API", обработчики ошибок зарегистрированы, placeholder для CORS, dependency get_db готов.

## Подсказка для LLM
Создайте app/main.py с FastAPI app. Установите title="Todo API", version="1.0.0". Импортируйте и зарегистрируйте обработчики исключений из app.middleware.error_handler. Импортируйте get_db из app.dependencies. Добавьте placeholder для CORS middleware. Добавьте health endpoint GET /api/v1/health возвращающий {"status": "ok"}.

## Оценка усилия
S

## Файлы для создания
- app/main.py

## Структура main.py
```python
from fastapi import FastAPI
from app.middleware.error_handler import register_exception_handlers
from app.dependencies import get_db

app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="REST API для управления задачами с поддержкой GTD методологии"
)

# Регистрация обработчиков ошибок
register_exception_handlers(app)

# Placeholder для CORS middleware
# TODO: Добавить CORSMiddleware в L4-52

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}
```

## Health endpoint
GET /api/v1/health
- Ответ: {"status": "ok"}
- Проверка подключения к БД будет добавлена в задаче L3-42
