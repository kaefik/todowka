# Todo API Documentation

REST API для управления задачами с поддержкой GTD (Getting Things Done) методологии.

## Quick Start

- **Base URL**: `http://localhost:8000`
- **Interactive Docs**: [Swagger UI](http://localhost:8000/docs)
- **Alternative Docs**: [ReDoc](http://localhost:8000/redoc)
- **Health Check**: `GET /api/v1/health`

## Core Concepts

### Tasks (Задачи)
Основная сущность для управления задачами с GTD статусами:
- `inbox` - входящие (необработанные)
- `active` - активные задачи
- `completed` - завершенные
- `waiting` - ожидающие
- `someday` - когда-нибудь позже

### Projects (Проекты)
Группировка задач по проектам с отслеживанием прогресса.

### Tags (Теги)
Категории и метки для организации задач (например: "Работа", "Личное", "Срочное").

### Contexts (Контексты)
Ситуации для выполнения задач (например: "Дома", "Офис", "В пути").

### Areas (Области ответственности)
Высокоуровневые категории (например: "Карьера", "Здоровье", "Семья").

### Inbox (Входящие)
Быстрый сбор задач без детализации.

## Key Endpoints

### Tasks
```
POST   /api/v1/tasks              - создать задачу
GET    /api/v1/tasks              - все задачи (с фильтрацией)
GET    /api/v1/tasks/{id}         - задача по ID
PUT    /api/v1/tasks/{id}         - обновить задачу
DELETE /api/v1/tasks/{id}         - удалить задачу
POST   /api/v1/tasks/{id}/complete - завершить задачу
POST   /api/v1/tasks/{id}/next-action - в next actions
```

### Inbox
```
POST   /api/v1/inbox             - создать задачу в inbox
GET    /api/v1/inbox             - задачи из inbox
```

### Projects
```
POST   /api/v1/projects          - создать проект
GET    /api/v1/projects          - все проекты (с пагинацией)
GET    /api/v1/projects/{id}     - проект по ID
PUT    /api/v1/projects/{id}     - обновить проект
DELETE /api/v1/projects/{id}     - удалить проект
POST   /api/v1/projects/{id}/complete - завершить проект
POST   /api/v1/projects/{id}/subtasks - добавить подзадачу
```

### Tags
```
POST   /api/v1/tags              - создать тег
GET    /api/v1/tags              - все теги
GET    /api/v1/tags/{id}         - тег по ID
PUT    /api/v1/tags/{id}         - обновить тег
DELETE /api/v1/tags/{id}         - удалить тег
```

### Contexts
```
POST   /api/v1/contexts          - создать контекст
GET    /api/v1/contexts          - все контексты
GET    /api/v1/contexts/{id}     - контекст по ID
PUT    /api/v1/contexts/{id}     - обновить контекст
DELETE /api/v1/contexts/{id}     - удалить контекст
```

### Areas
```
POST   /api/v1/areas            - создать область
GET    /api/v1/areas            - все области
GET    /api/v1/areas/{id}       - область по ID
PUT    /api/v1/areas/{id}       - обновить область
DELETE /api/v1/areas/{id}       - удалить область
```

### Notifications
```
GET    /api/v1/notifications     - все уведомления
GET    /api/v1/notifications/{id} - уведомление по ID
PUT    /api/v1/notifications/{id} - обновить уведомление
```

## Common Query Parameters

### Pagination
- `page` - номер страницы (default: 1)
- `limit` - элементов на странице (default: 10)

### Task Filters
- `status` - статус задачи (inbox, active, completed, waiting, someday)
- `priority` - приоритет (low, medium, high)
- `project_id` - фильтр по проекту
- `context_id` - фильтр по контексту
- `area_id` - фильтр по области

## GTD Workflow

```
1. Capture → Inbox
   POST /api/v1/inbox

2. Clarify → Task with details
   POST /api/v1/tasks
   (с project, context, tags)

3. Organize → Next Actions
   POST /api/v1/tasks/{id}/next-action

4. Execute → Complete
   POST /api/v1/tasks/{id}/complete
```

## Response Format

### Success Response
```json
{
  "id": 1,
  "name": "Work",
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T10:00:00Z"
}
```

### Error Response
```json
{
  "detail": "Error message here"
}
```

### Pagination Response
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "limit": 10,
  "pages": 10
}
```

## Authentication

В текущей версии аутентификация не требуется (public API).

## Documentation

- Полное руководство: [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
- Примеры запросов: [API_EXAMPLES.md](API_EXAMPLES.md)
- Схемы данных: [SCHEMA_DOCUMENTATION.md](SCHEMA_DOCUMENTATION.md)
- Интеграция: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
- Для LLM: [LLM_INSTRUCTIONS.md](LLM_INSTRUCTIONS.md)
- Решение проблем: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- OpenAPI спецификация: [openapi.json](openapi.json)