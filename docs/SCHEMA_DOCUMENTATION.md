# Schema Documentation

Полное описание схем данных Todo API.

## Table of Contents
- [Tag](#tag)
- [Context](#context)
- [Area](#area)
- [Project](#project)
- [Task](#task)
- [Subtask](#subtask)
- [Notification](#notification)
- [Enums](#enums)

---

## Tag

### Description
Категории и метки для организации задач.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | No (auto) | Уникальный идентификатор |
| name | string | Yes | Название тега (max 100 символов) |
| color | string | No | HEX-код цвета (например: #FF0000) |
| created_at | datetime | No (auto) | Время создания |
| updated_at | datetime | No (auto) | Время последнего обновления |

### Create Schema
```json
{
  "name": "Work",
  "color": "#FF0000"
}
```

### Response Schema
```json
{
  "id": 1,
  "name": "Work",
  "color": "#FF0000",
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T10:00:00Z"
}
```

### Validation Rules
- `name`: 1-100 символов, не может быть пустым
- `color`: Формат HEX (#FFFFFF), если указан

---

## Context

### Description
Ситуации для выполнения задач (дома, офис, в пути и т.д.).

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | No (auto) | Уникальный идентификатор |
| name | string | Yes | Название контекста (max 100 символов) |
| description | string | No | Описание контекста |
| created_at | datetime | No (auto) | Время создания |
| updated_at | datetime | No (auto) | Время последнего обновления |

### Create Schema
```json
{
  "name": "Office",
  "description": "Work at office"
}
```

### Response Schema
```json
{
  "id": 1,
  "name": "Office",
  "description": "Work at office",
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T10:00:00Z"
}
```

### Validation Rules
- `name`: 1-100 символов, не может быть пустым
- `description`: Макс. 500 символов, если указан

---

## Area

### Description
Области ответственности (высокоуровневые категории).

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | No (auto) | Уникальный идентификатор |
| name | string | Yes | Название области (max 100 символов) |
| description | string | No | Описание области |
| created_at | datetime | No (auto) | Время создания |
| updated_at | datetime | No (auto) | Время последнего обновления |

### Create Schema
```json
{
  "name": "Career",
  "description": "Professional development"
}
```

### Response Schema
```json
{
  "id": 1,
  "name": "Career",
  "description": "Professional development",
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T10:00:00Z"
}
```

### Validation Rules
- `name`: 1-100 символов, не может быть пустым
- `description`: Макс. 500 символов, если указан

---

## Project

### Description
Проекты для группировки задач с отслеживанием прогресса.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | No (auto) | Уникальный идентификатор |
| name | string | Yes | Название проекта (max 100 символов) |
| description | string | No | Описание проекта |
| area_id | integer | No | ID области ответственности |
| status | enum | No (auto) | Статус проекта (active, completed) |
| progress | integer | No (auto) | Прогресс (0-100) |
| total_tasks | integer | No (auto) | Всего задач в проекте |
| completed_tasks | integer | No (auto) | Завершенных задач |
| completed_at | datetime | No (auto) | Время завершения |
| created_at | datetime | No (auto) | Время создания |
| updated_at | datetime | No (auto) | Время последнего обновления |

### Create Schema
```json
{
  "name": "Learning Python",
  "description": "Learn FastAPI and SQLAlchemy",
  "area_id": 1
}
```

### Response Schema (Detailed)
```json
{
  "id": 1,
  "name": "Learning Python",
  "description": "Learn FastAPI and SQLAlchemy",
  "area_id": 1,
  "status": "active",
  "progress": 45,
  "total_tasks": 20,
  "completed_tasks": 9,
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T11:00:00Z"
}
```

### Validation Rules
- `name`: 1-100 символов, не может быть пустым
- `description`: Макс. 500 символов, если указан
- `area_id`: Должен существовать в таблице areas
- `progress`: Автоматически вычисляется (completed_tasks / total_tasks * 100)

---

## Task

### Description
Задачи с GTD статусами.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | No (auto) | Уникальный идентификатор |
| title | string | Yes | Название задачи (max 200 символов) |
| description | string | No | Описание задачи |
| status | enum | No (auto) | Статус задачи |
| priority | enum | No (auto) | Приоритет задачи (low, medium, high) |
| project_id | integer | No | ID проекта |
| context_id | integer | No | ID контекста |
| tag_ids | integer[] | No | Массив ID тегов |
| is_next_action | boolean | No (auto) | Является ли следующим действием |
| completed_at | datetime | No (auto) | Время завершения |
| reminder_at | datetime | No | Время напоминания |
| created_at | datetime | No (auto) | Время создания |
| updated_at | datetime | No (auto) | Время последнего обновления |

### Create Schema
```json
{
  "title": "Complete API tutorial",
  "description": "Finish the tutorial",
  "project_id": 1,
  "context_id": 1,
  "tag_ids": [1, 2],
  "priority": "high",
  "status": "active"
}
```

### Response Schema
```json
{
  "id": 1,
  "title": "Complete API tutorial",
  "description": "Finish the tutorial",
  "status": "active",
  "priority": "high",
  "project_id": 1,
  "context_id": 1,
  "tag_ids": [1, 2],
  "is_next_action": false,
  "completed_at": null,
  "reminder_at": null,
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T10:00:00Z"
}
```

### Validation Rules
- `title`: 1-200 символов, не может быть пустым
- `description`: Макс. 1000 символов, если указан
- `project_id`: Должен существовать в таблице projects
- `context_id`: Должен существовать в таблице contexts
- `tag_ids`: Все ID должны существовать в таблице tags
- `priority`: low, medium, high (default: medium)
- `status`: inbox, active, completed, waiting, someday (default: inbox)

---

## Subtask

### Description
Подзадачи внутри проектов.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | No (auto) | Уникальный идентификатор |
| title | string | Yes | Название подзадачи (max 200 символов) |
| project_id | integer | No | ID проекта (если не указана task) |
| task_id | integer | No | ID задачи (опционально) |
| is_completed | boolean | No (auto) | Завершена ли подзадача |
| completed_at | datetime | No (auto) | Время завершения |
| created_at | datetime | No (auto) | Время создания |
| updated_at | datetime | No (auto) | Время последнего обновления |

### Create Schema (for Project)
```json
{
  "title": "Read documentation",
  "project_id": 1,
  "task_id": 2
}
```

### Response Schema
```json
{
  "id": 1,
  "title": "Read documentation",
  "project_id": 1,
  "task_id": 2,
  "is_completed": false,
  "completed_at": null,
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T10:00:00Z"
}
```

### Validation Rules
- `title`: 1-200 символов, не может быть пустым
- `project_id` или `task_id`: Должен быть указан хотя бы один
- `project_id`: Должен существовать в таблице projects
- `task_id`: Должен существовать в таблице tasks

---

## Notification

### Description
Уведомления о задачах.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | No (auto) | Уникальный идентификатор |
| message | string | No | Текст уведомления |
| task_id | integer | No | ID связанной задачи |
| status | enum | No (auto) | Статус уведомления |
| scheduled_at | datetime | No | Запланированное время |
| sent_at | datetime | No (auto) | Время отправки |
| error | string | No | Текст ошибки при отправке |
| created_at | datetime | No (auto) | Время создания |
| updated_at | datetime | No (auto) | Время последнего обновления |

### Response Schema
```json
{
  "id": 1,
  "message": "Task reminder",
  "task_id": 1,
  "status": "pending",
  "scheduled_at": "2026-03-12T14:00:00Z",
  "sent_at": null,
  "error": null,
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T10:00:00Z"
}
```

### Validation Rules
- `message`: Макс. 500 символов, если указан
- `task_id`: Должен существовать в таблице tasks
- `status`: pending, sent, failed (default: pending)

---

## Enums

### TaskStatus

| Value | Description |
|-------|-------------|
| `inbox` | Входящие (необработанные задачи) |
| `active` | Активные задачи |
| `completed` | Завершенные задачи |
| `waiting` | Ожидающие (на чьем-то ответе) |
| `someday` | Когда-нибудь позже (без срока) |

### TaskPriority

| Value | Description |
|-------|-------------|
| `low` | Низкий приоритет |
| `medium` | Средний приоритет (default) |
| `high` | Высокий приоритет |

### ProjectStatus

| Value | Description |
|-------|-------------|
| `active` | Активный проект (default) |
| `completed` | Завершенный проект |

### NotificationStatus

| Value | Description |
|-------|-------------|
| `pending` | Ожидает отправки (default) |
| `sent` | Отправлено |
| `failed` | Ошибка отправки |

---

## Date/Time Format

Все datetime поля используют ISO 8601 формат:
```
2026-03-12T10:00:00Z
2026-03-12T10:00:00+03:00
```

---

## Pagination Schema

Используется для списков с пагинацией.

### Response Schema
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "limit": 20,
  "pages": 5
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| items | array | Массив элементов |
| total | integer | Общее количество элементов |
| page | integer | Текущая страница |
| limit | integer | Элементов на странице |
| pages | integer | Общее количество страниц |

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Номер страницы |
| limit | integer | 10 | Элементов на странице |

---

## Relationship Diagram

```
Area (1) ----< (N) Project
                      |
                      | (1)
                      |----< (N) Task ----< (N) Tag
                      |       | (1)
                      |       |
Context (1) ----< (N)       |
                              |
                        Subtask (1)
```

**Legend:**
- `1` - один
- `<` - ссылка на
- `N` - много

**Relationships:**
- Area → Project: Один ко многим
- Project → Task: Один ко многим
- Project → Subtask: Один ко многим
- Task → Tag: Много ко многим
- Context → Task: Один ко многим
- Task → Subtask: Один ко многим (опционально)

---

## Common Fields

### ID
- Тип: `integer`
- Описание: Уникальный идентификатор
- Автоматически генерируется при создании
- Не может быть изменен

### Timestamp Fields
- Тип: `datetime`
- Описание: Время события
- Формат: ISO 8601
- Поля:
  - `created_at`: Время создания (автоматически)
  - `updated_at`: Время последнего обновления (автоматически)
  - `completed_at`: Время завершения (при соответствующем действии)

---

## Error Schemas

### Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "error message",
      "type": "error_type"
    }
  ]
}
```

### Not Found Error
```json
{
  "detail": "Entity not found"
}
```

### Bad Request Error
```json
{
  "detail": "Error message"
}
```