# Todo API Design Document

**Date:** 2025-03-10
**Status:** Approved
**Architecture:** Layered Architecture with Repository Pattern

---

## Overview

REST API для управления задачами, проектами, подзадачами с поддержкой GTD методологии. Ядро предоставляет API для любых клиентов (web, mobile, CLI, и т.д.).

**Target Audience:** Люди, которые хотят привести в порядок свои задачи, внедрить GTD или другие методологии управления задачами и проектами.

**Tech Stack:**
- Language: Python
- Framework: FastAPI
- Database: SQLite
- ORM: SQLAlchemy
- Validation: Pydantic
- Architecture: Layered with Repository Pattern
- Background Tasks: Celery + Redis (для напоминаний)

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
│   ├── auth/                   # Аутентификация (для будущего расширения)
│   │   ├── __init__.py
│   │   ├── security.py         # JWT или API key логика
│   │   └── dependencies.py     # get_current_user
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── task.py
│   │   ├── project.py
│   │   ├── subtask.py
│   │   ├── tag.py
│   │   ├── context.py
│   │   ├── area.py
│   │   └── notification.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py
│   │   ├── project.py
│   │   ├── subtask.py
│   │   ├── tag.py
│   │   ├── context.py
│   │   ├── area.py
│   │   ├── notification.py
│   │   └── pagination.py       # PaginatedResponse schema
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── task.py
│   │   ├── project.py
│   │   ├── subtask.py
│   │   ├── tag.py
│   │   ├── context.py
│   │   ├── area.py
│   │   └── notification.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task.py
│   │   ├── project.py
│   │   ├── subtask.py
│   │   ├── tag.py
│   │   ├── context.py
│   │   ├── area.py
│   │   ├── notification.py
│   │   └── reminders.py         # Background tasks для напоминаний
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── tasks.py            # /api/v1/tasks
│   │   ├── projects.py         # /api/v1/projects
│   │   ├── subtasks.py         # /api/v1/subtasks
│   │   ├── tags.py            # /api/v1/tags
│   │   ├── contexts.py        # /api/v1/contexts
│   │   ├── areas.py           # /api/v1/areas
│   │   ├── notifications.py   # /api/v1/notifications
│   │   └── inbox.py           # /api/v1/inbox (GTD)
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
- `status` (Enum: inbox/active/someday/waiting/delegated, default=active)
- `priority` (Enum: low/medium/high, default=medium)
- `due_date` (DateTime, nullable)
- `reminder_time` (DateTime, nullable)
- `is_next_action` (Boolean, default=False)
- `waiting_for` (String, nullable)
- `delegated_to` (String, nullable)
- `someday` (Boolean, default=False)
- `created_at` (DateTime)
- `updated_at` (DateTime)
- `project_id` (FK, nullable)
- `context_id` (FK, nullable)
- `area_id` (FK, nullable)
- `tags` (Many-to-Many relationship with Tag)

### Project
- `id` (PK, Integer)
- `name` (String, required)
- `description` (String, nullable)
- `status` (Enum: active/completed/paused, default=active)
- `start_date` (DateTime, nullable)
- `end_date` (DateTime, nullable)
- `progress` (Integer, 0-100, default=0)
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

### Tag
- `id` (PK, Integer)
- `name` (String, required, unique)
- `color` (String hex, nullable)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Context (GTD)
- `id` (PK, Integer)
- `name` (String, required, unique)
- `icon` (String, nullable)
- `color` (String hex, nullable)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Area (GTD - Область ответственности)
- `id` (PK, Integer)
- `name` (String, required, unique)
- `description` (String, nullable)
- `color` (String hex, nullable)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Notification
- `id` (PK, Integer)
- `task_id` (FK, required)
- `message` (String, required)
- `scheduled_at` (DateTime, required)
- `sent_at` (DateTime, nullable)
- `status` (Enum: pending/sent/failed, default=pending)
- `created_at` (DateTime)

---

## Pydantic Schemas

### Task
- `TaskCreate`: title, description?, priority?, due_date?, reminder_time?, project_id?, context_id?, area_id?, tag_ids?, status?, is_next_action?, waiting_for?, delegated_to?, someday?
- `TaskUpdate`: title?, description?, completed?, priority?, due_date?, reminder_time?, project_id?, context_id?, area_id?, status?, is_next_action?, waiting_for?, delegated_to?, someday?
- `TaskResponse`: id, title, description, completed, status, priority, due_date, reminder_time, is_next_action, waiting_for, delegated_to, someday, created_at, updated_at, project_id, context_id, area_id, tags

### Project
- `ProjectCreate`: name, description?, status?, start_date?, end_date?, color?
- `ProjectUpdate`: name?, description?, status?, start_date?, end_date?, progress?, color?
- `ProjectResponse`: id, name, description, status, start_date, end_date, progress, color, created_at, updated_at

### Subtask
- `SubtaskCreate`: title, order?
- `SubtaskUpdate`: title?, completed?, order?
- `SubtaskResponse`: id, task_id, title, completed, order, created_at, updated_at

### Tag
- `TagCreate`: name, color?
- `TagResponse`: id, name, color, created_at, updated_at

### Context
- `ContextCreate`: name, icon?, color?
- `ContextResponse`: id, name, icon, color, created_at, updated_at

### Area
- `AreaCreate`: name, description?, color?
- `AreaResponse`: id, name, description, color, created_at, updated_at

### Notification
- `NotificationCreate`: task_id, message, scheduled_at
- `NotificationResponse`: id, task_id, message, scheduled_at, sent_at, status, created_at

### Pagination
- `PaginationResponse[T]`: items: List[T], total: int, page: int, size: int

---

## API Endpoints

### Tasks (/api/v1/tasks)
```
GET    /api/v1/tasks           - список задач с пагинацией (page, size, status?, project_id?, context_id?, area_id?, priority?, tag_ids?)
GET    /api/v1/tasks/{id}      - получить задачу по ID
POST   /api/v1/tasks           - создать задачу
PUT    /api/v1/tasks/{id}      - обновить задачу (все поля)
PATCH  /api/v1/tasks/{id}      - частичное обновление задачи
DELETE /api/v1/tasks/{id}      - удалить задачу
POST   /api/v1/tasks/{id}/next-action - отметить как следующее действие
POST   /api/v1/tasks/{id}/complete - завершить задачу
POST   /api/v1/tasks/{id}/schedule-reminder - запланировать напоминание
```

### GTD Endpoints
```
GET    /api/v1/inbox           - задачи со статусом inbox (входящие)
POST   /api/v1/inbox           - создать задачу в inbox (автоматически status=inbox)
GET    /api/v1/next-actions    - задачи где is_next_action=true
GET    /api/v1/waiting         - задачи со статусом waiting
GET    /api/v1/someday         - задачи где someday=true
```

### Projects (/api/v1/projects)
```
GET    /api/v1/projects        - список проектов с пагинацией (page, size, status?)
GET    /api/v1/projects/{id}   - получить проект
POST   /api/v1/projects        - создать проект
PUT    /api/v1/projects/{id}   - обновить проект
DELETE /api/v1/projects/{id}   - удалить проект
POST   /api/v1/projects/{id}/complete - завершить проект
GET    /api/v1/projects/{id}/tasks - задачи проекта
```

### Subtasks (/api/v1/tasks/{task_id}/subtasks)
```
GET    /api/v1/tasks/{task_id}/subtasks      - список подзадач для задачи
POST   /api/v1/tasks/{task_id}/subtasks      - создать подзадачу
PUT    /api/v1/tasks/{task_id}/subtasks/{id} - обновить подзадачу
DELETE /api/v1/tasks/{task_id}/subtasks/{id} - удалить подзадачу
```

### Tags (/api/v1/tags)
```
GET    /api/v1/tags            - список всех тегов
GET    /api/v1/tags/{id}       - получить тег
POST   /api/v1/tags            - создать тег
PUT    /api/v1/tags/{id}       - обновить тег
DELETE /api/v1/tags/{id}       - удалить тег
GET    /api/v1/tags/{id}/tasks - задачи с этим тегом
```

### Contexts (/api/v1/contexts)
```
GET    /api/v1/contexts        - список всех контекстов
GET    /api/v1/contexts/{id}   - получить контекст
POST   /api/v1/contexts        - создать контекст
PUT    /api/v1/contexts/{id}   - обновить контекст
DELETE /api/v1/contexts/{id}   - удалить контекст
GET    /api/v1/contexts/{id}/tasks - задачи с этим контекстом
```

### Areas (/api/v1/areas)
```
GET    /api/v1/areas           - список всех областей
GET    /api/v1/areas/{id}      - получить область
POST   /api/v1/areas           - создать область
PUT    /api/v1/areas/{id}      - обновить область
DELETE /api/v1/areas/{id}      - удалить область
GET    /api/v1/areas/{id}/tasks - задачи в этой области
```

### Notifications (/api/v1/notifications)
```
GET    /api/v1/notifications   - список уведомлений (page, size, status?)
GET    /api/v1/notifications/{id} - получить уведомление
POST   /api/v1/notifications   - создать уведомление (автоматически при планировании напоминания)
```

### Health & Info
```
GET    /api/v1/health          - статус сервиса
GET    /                        - информация о API (ссылка на Swagger UI)
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
- `get_filtered(filters)` - фильтрация по status, project_id, context_id, area_id, priority, tag_ids, due_date
- `count(filters)` - подсчёт с фильтрами
- `get_by_tags(tag_ids)` - задачи с заданными тегами
- `get_next_actions()` - задачи где is_next_action=true
- `get_inbox()` - задачи со статусом inbox
- `get_waiting()` - задачи со статусом waiting
- `get_someday()` - задачи где someday=true

### ProjectRepository
- Все методы BaseRepository
- `get_by_status(status)` - фильтрация по статусу
- `update_progress(project_id)` - пересчитать прогресс на основе задач

### SubtaskRepository
- Все методы BaseRepository
- `get_by_task(task_id)` - все подзадачи для задачи

### TagRepository
- Все методы BaseRepository
- `get_by_name(name)` - найти тег по имени
- `get_or_create(name, color)` - получить или создать тег

### ContextRepository
- Все методы BaseRepository

### AreaRepository
- Все методы BaseRepository

### NotificationRepository
- Все методы BaseRepository
- `get_pending()` - все ожидающие уведомления
- `mark_sent(id)` - отметить как отправленное
- `mark_failed(id, error)` - отметить как неудачное

---

## Service Layer

### TaskService
- `get_tasks(page, size, filters)` - пагинированный список с фильтрами
- `get_task(id)` - получить задачу (или NotFoundException)
- `create_task(data)` - создать с валидацией
- `update_task(id, data)` - обновить с проверкой существования
- `delete_task(id)` - удалить
- `toggle_complete(id)` - переключить статус completed
- `set_next_action(id, flag)` - отметить как следующее действие
- `schedule_reminder(id, time)` - запланировать напоминание
- `set_waiting(id, waiting_for)` - установить статус "ожидание"

### ProjectService
- CRUD операции
- `complete_project(id)` - завершить проект (закрыть все задачи)
- `update_progress(id)` - пересчитать прогресс
- Проверка при удалении, что проект не используется

### SubtaskService
- CRUD операции
- Проверка при создании, что task_id существует
- `get_subtasks(task_id)` - все подзадачи для задачи

### TagService
- CRUD операции
- `assign_tags(task_id, tag_ids)` - назначить теги задаче
- `get_task_tags(task_id)` - получить теги задачи

### ContextService
- CRUD операции

### AreaService
- CRUD операции

### NotificationService
- `create_notification(task_id, message, scheduled_at)` - создать уведомление
- `get_pending_notifications()` - получить все ожидающие
- `send_notification(notification)` - отправить (делегируется в RemindersService)

### RemindersService (Background Tasks)
- `check_and_send_reminders()` - периодически проверять reminder_time в задачах
- `send_email(task)` - отправить email (опционально)
- `send_webhook(task)` - отправить webhook (опционально)

---

## Configuration & Dependencies

### Config (app/config.py)
- `pydantic-settings.BaseSettings`
- `DATABASE_URL` (sqlite:///database.db)
- `REDIS_URL` (redis://localhost:6379/0)
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `SECRET_KEY` (для JWT - для будущего)
- `API_HOST`, `API_PORT`
- `LOG_LEVEL`
- `REMINDER_CHECK_INTERVAL` (по умолчанию 60 сек)

### Dependencies (app/dependencies.py)
- `get_db()` - SQLAlchemy сессия
- `get_task_service(db)`
- `get_project_service(db)`
- `get_subtask_service(db)`
- `get_tag_service(db)`
- `get_context_service(db)`
- `get_area_service(db)`
- `get_notification_service(db)`
- `get_current_user(token)` - JWT/API key проверка (для будущего расширения)

---

## Error Handling

### Custom Exceptions (app/exceptions.py)
- `NotFoundException` - ресурс не найден (404)
- `ValidationErrorException` - ошибки валидации (422)
- `ConflictException` - конфликт данных (409)
- `ReminderException` - ошибка отправки напоминания

### Middleware (app/middleware/error_handler.py)
- `@app.exception_handler` для единообразного JSON ответа
- Формат: `{"error": "type", "message": "...", "details": {...}}`

---

## Authentication

**Для MVP:** Однопользовательский режим, без аутентификации.

**Будущее расширение:**
- API key в Header (`X-API-Key`) или JWT (`Authorization: Bearer <token>`)
- `get_current_user` dependency для защиты endpoints
- Многопользовательский режим с разделением данных по `user_id`

---

## Notifications & Reminders

### Celery Background Tasks
- Периодическая задача: проверка задач с `reminder_time` в ближайшее время
- Создание записей в `Notification`
- Отправка уведомлений через email/webhook (опционально)

### Запуск Celery
```bash
celery -A app.services.reminders worker --loglevel=info
celery -A app.services.reminders beat --loglevel=info
```

---

## Deployment

### Requirements (requirements.txt)
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
sqlalchemy>=2.0.0
pydantic-settings>=2.1.0
celery>=5.3.0
redis>=5.0.0
```

### Run Command
```bash
# API
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Redis
redis-server

# Celery worker
celery -A app.services.reminders worker --loglevel=info

# Celery beat (для периодических задач)
celery -A app.services.reminders beat --loglevel=info
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

## GTD Methodology Support

### GTD Concepts in API
1. **Inbox** - `/api/v1/inbox` endpoint для быстрого захвата задач
2. **Next Actions** - поле `is_next_action`, фильтр `/api/v1/next-actions`
3. **Contexts** - отдельная сущность `Context` (@офис, @телефон, @интернет)
4. **Areas** - отдельная сущность `Area` (Работа, Здоровье, Семья)
5. **Waiting For** - поле `waiting_for` + статус `waiting`
6. **Delegated** - поле `delegated_to` + статус `delegated`
7. **Someday/Maybe** - поле `someday` + статус `someday`
8. **Projects** - сущность `Project` с прогрессом и сроками

### GTD Workflow
1. Сбор: `POST /api/v1/inbox` - быстрая запись
2. Обработка: изменение `status` на `active`, добавление `project_id`, `context_id`, `area_id`
3. Организация: добавление тегов, установка `is_next_action`
4. Планирование: установка `due_date`, `reminder_time`
5. Выполнение: `POST /api/v1/tasks/{id}/complete`
6. Проверка: просмотр `/api/v1/next-actions`, `/api/v1/waiting`, `/api/v1/someday`

---

## Future Extensions

### Web Application
- Отдельный клиент на React/Vue/Svelte
- Реализация всех возможностей API
- Drag-and-drop интерфейс для задач и проектов
- Календарный вид
- GTD Dashboard

### Multi-User Support
- Аутентификация (JWT/API Key)
- Разделение данных по `user_id`
- Совместная работа над проектами
- Права доступа

### Advanced Features
- Встроенный календарь для встреч
- Reference items (заметки, справочники)
- Автоматизация Daily/Weekly Review
- Интеграции с Google Calendar, Outlook, etc.
- Email-to-Inbox (создание задач по email)
- Мобильные приложения (iOS, Android)
- Экспорт/импорт данных
- Аналитика и статистика

---

## Notes

- SQLite без Alembic - создаём таблицы через `Base.metadata.create_all()` при старте
- Пагинация обязательна для списков (`page`, `size` параметры)
- Swagger UI доступен по `/docs`
- CORS middleware для клиентских приложений
- Логирование запросов (заголовки, статус, время ответа)
- Режим MVP: однопользовательский, без аутентификации
- Celery + Redis для фоновых задач (напоминания)
