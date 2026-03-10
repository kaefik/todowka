# Todo API Design Document

**Date:** 2025-03-10  
**Status:** Approved  
**Architecture:** Layered Architecture with Repository Pattern

---

## Overview

REST API для управления задачами, категориями и подзадачами. Ядро предоставляет API для любых клиентов (web, mobile, CLI, и т.д.).

**Tech Stack:**
- Language: Python
- Framework: FastAPI
- Database: SQLite
- ORM: SQLAlchemy
- Validation: Pydantic
- Architecture: Layered with Repository Pattern

---

## Project Structure

```
todo-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point, корневой endpoint
│   ├── config.py               # pydantic-settings для конфигурации из .env
│   ├── dependencies.py         # FastAPI dependency injection (get_db, get_services)
│   ├── exceptions.py           # Кастомные исключения API
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── error_handler.py    # Единая обработка ошибок
│   ├── auth/                   # Аутентификация
│   │   ├── __init__.py
│   │   ├── security.py         # JWT или API key логика
│   │   └── dependencies.py     # get_current_user
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── task.py
│   │   ├── category.py
│   │   └── subtask.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py
│   │   ├── category.py
│   │   ├── subtask.py
│   │   └── pagination.py       # PaginatedResponse schema
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── task.py
│   │   ├── category.py
│   │   └── subtask.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task.py
│   │   ├── category.py
│   │   └── subtask.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── tasks.py            # /api/v1/tasks
│   │   ├── categories.py       # /api/v1/categories
│   │   └── subtasks.py         # /api/v1/subtasks
├── tests/
│   ├── unit/
│   │   ├── test_services.py
│   │   └── test_repositories.py
│   └── integration/
│       └── test_api.py
├── database.db
├── requirements.txt
└── .env
```

---

## Database Models

### Task
- `id` (PK, Integer)
- `title` (String, required)
- `description` (String, nullable)
- `completed` (Boolean, default=False)
- `priority` (Enum: low/medium/high, default=medium)
- `due_date` (DateTime, nullable)
- `created_at` (DateTime)
- `updated_at` (DateTime)
- `category_id` (FK, nullable)
- `user_id` (FK для авторизации, nullable на старте)

### Category
- `id` (PK, Integer)
- `name` (String, required)
- `description` (String, nullable)
- `color` (String hex, nullable)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Subtask
- `id` (PK, Integer)
- `task_id` (FK, required)
- `title` (String, required)
- `completed` (Boolean, default=False)
- `order` (Integer, для сортировки)
- `created_at` (DateTime)
- `updated_at` (DateTime)

---

## Pydantic Schemas

### Task
- `TaskCreate`: title, description?, priority?, due_date?, category_id?
- `TaskUpdate`: title?, description?, completed?, priority?, due_date?, category_id?
- `TaskResponse`: id, title, description, completed, priority, due_date, created_at, updated_at, category_id

### Category
- `CategoryCreate`: name, description?, color?
- `CategoryResponse`: id, name, description, color, created_at, updated_at

### Subtask
- `SubtaskCreate`: title, order?
- `SubtaskUpdate`: title?, completed?, order?
- `SubtaskResponse`: id, task_id, title, completed, order, created_at, updated_at

### Pagination
- `PaginationResponse[T]`: items: List[T], total: int, page: int, size: int

---

## API Endpoints

### Tasks (/api/v1/tasks)
```
GET    /api/v1/tasks           - список задач с пагинацией (page, size, completed?, category_id?, priority?)
GET    /api/v1/tasks/{id}      - получить задачу по ID
POST   /api/v1/tasks           - создать задачу
PUT    /api/v1/tasks/{id}      - обновить задачу (все поля)
PATCH  /api/v1/tasks/{id}      - частичное обновление задачи
DELETE /api/v1/tasks/{id}      - удалить задачу
```

### Categories (/api/v1/categories)
```
GET    /api/v1/categories      - список всех категорий
GET    /api/v1/categories/{id}  - получить категорию
POST   /api/v1/categories      - создать категорию
PUT    /api/v1/categories/{id} - обновить категорию
DELETE /api/v1/categories/{id} - удалить категорию
```

### Subtasks (/api/v1/tasks/{task_id}/subtasks)
```
GET    /api/v1/tasks/{task_id}/subtasks      - список подзадач для задачи
POST   /api/v1/tasks/{task_id}/subtasks      - создать подзадачу
PUT    /api/v1/tasks/{task_id}/subtasks/{id} - обновить подзадачу
DELETE /api/v1/tasks/{task_id}/subtasks/{id} - удалить подзадачу
```

### Health & Info
```
GET    /api/v1/health          - статус сервиса
GET    /                       - информация о API (ссылка на Swagger UI)
```

---

## Repository Layer

### BaseRepository
- `__init__(db_session)` - конструктор с сессией БД
- `get(id)` - получить запись по ID
- `get_all(limit, offset)` - получить все с пагинацией
- `create(**kwargs)` - создать запись
- `update(id, **kwargs)` - обновить запись
- `delete(id)` - удалить запись
- `exists(id)` - проверка существования

### TaskRepository
- Все методы BaseRepository
- `get_filtered(filters)` - фильтрация по completed, category_id, priority, due_date
- `count(filters)` - подсчёт с фильтрами

### CategoryRepository
- Все методы BaseRepository

### SubtaskRepository
- Все методы BaseRepository
- `get_by_task(task_id)` - все подзадачи для задачи

---

## Service Layer

### TaskService
- `get_tasks(page, size, filters)` - пагинированный список с фильтрами
- `get_task(id)` - получить задачу (или NotFoundException)
- `create_task(data)` - создать с валидацией
- `update_task(id, data)` - обновить с проверкой существования
- `delete_task(id)` - удалить
- `toggle_complete(id)` - переключить статус completed

### CategoryService
- CRUD операции
- Проверка при удалении, что категория не используется задачами

### SubtaskService
- CRUD операции
- Проверка при создании, что task_id существует
- `get_subtasks(task_id)` - все подзадачи для задачи

---

## Configuration & Dependencies

### Config (app/config.py)
- `pydantic-settings.BaseSettings`
- `DATABASE_URL` (sqlite:///database.db)
- `SECRET_KEY` (для JWT)
- `API_HOST`, `API_PORT`
- `LOG_LEVEL`

### Dependencies (app/dependencies.py)
- `get_db()` - SQLAlchemy сессия
- `get_task_service(db)`
- `get_category_service(db)`
- `get_subtask_service(db)`
- `get_current_user(token)` - JWT/API key проверка (опционально)

---

## Error Handling

### Custom Exceptions (app/exceptions.py)
- `NotFoundException` - ресурс не найден (404)
- `ValidationErrorException` - ошибки валидации (422)
- `ConflictException` - конфликт данных (409)

### Middleware (app/middleware/error_handler.py)
- `@app.exception_handler` для единообразного JSON ответа
- Формат: `{"error": "type", "message": "...", "details": {...}}`

---

## Authentication

**Базовый вариант:**
- API key в Header (`X-API-Key`) или JWT (`Authorization: Bearer <token>`)
- `get_current_user` dependency для защиты endpoints
- Опционально: можно добавить позже, пока без защиты

---

## Deployment

### Requirements (requirements.txt)
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
sqlalchemy>=2.0.0
pydantic-settings>=2.1.0
alembic>=1.13.0 (опционально)
```

### Run Command
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker (опционально)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Notes

- SQLite без Alembic - создаём таблицы через `Base.metadata.create_all()` при старте
- Пагинация обязательна для списков (`page`, `size` параметры)
- Swagger UI доступен по `/docs`
- CORS middleware для клиентских приложений
- Логирование запросов (заголовки, статус, время ответа)
