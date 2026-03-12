# Todo API Developer Guide

Полное руководство разработчика для работы с Todo API.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Authentication & Headers](#authentication--headers)
3. [Common Patterns](#common-patterns)
4. [GTD Methodology Implementation](#gtd-methodology-implementation)
5. [Error Handling](#error-handling)
6. [Best Practices](#best-practices)

---

## Getting Started

### Prerequisites
- API сервер должен быть запущен на `http://localhost:8000`
- Утилита `curl` или HTTP клиент (Postman, Insomnia)
- Для тестов: `http://localhost:8000/docs`

### Quick Test
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Expected response
{"status":"ok","database":"connected"}
```

---

## Authentication & Headers

### Required Headers
```bash
Content-Type: application/json
```

### Example Request
```bash
curl -X POST http://localhost:8000/api/v1/tags \
  -H "Content-Type: application/json" \
  -d '{"name": "Work", "color": "#FF0000"}'
```

### Optional Headers
```bash
Accept: application/json
User-Agent: YourApp/1.0
```

---

## Common Patterns

### 1. Create Entity

**Pattern:** `POST /api/v1/{entity}`

```javascript
// Create Tag
POST /api/v1/tags
{
  "name": "Work",
  "color": "#FF0000"
}

// Create Task
POST /api/v1/tasks
{
  "title": "Task title",
  "description": "Task description",
  "status": "active",
  "priority": "high"
}
```

### 2. Get All Entities

**Pattern:** `GET /api/v1/{entity}`

```javascript
// Get all tags
GET /api/v1/tags

// Get tasks with pagination
GET /api/v1/tasks?page=1&limit=20
```

**Response (with pagination):**
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "limit": 20,
  "pages": 5
}
```

### 3. Get Single Entity

**Pattern:** `GET /api/v1/{entity}/{id}`

```javascript
// Get tag by ID
GET /api/v1/tags/1

// Response
{
  "id": 1,
  "name": "Work",
  "color": "#FF0000",
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T10:00:00Z"
}
```

### 4. Update Entity

**Pattern:** `PUT /api/v1/{entity}/{id}`

```javascript
// Update tag
PUT /api/v1/tags/1
{
  "name": "Updated Work",
  "color": "#00FF00"
}
```

**Note:** PUT заменяет все поля, необязательные поля можно опустить.

### 5. Delete Entity

**Pattern:** `DELETE /api/v1/{entity}/{id}`

```javascript
// Delete tag
DELETE /api/v1/tags/1

// Response (204 No Content)
```

---

## GTD Methodology Implementation

### 1. Capture (Захват)

Быстрое добавление задач без детализации:

```javascript
POST /api/v1/inbox
{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs"
}
```

**Use case:** Быстрая запись идеи или задачи на лету.

### 2. Clarify (Уточнение)

Перенос задачи из inbox в организованную структуру:

```javascript
POST /api/v1/tasks
{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "project_id": 1,
  "context_id": 2,
  "tag_ids": [1, 3],
  "priority": "medium",
  "status": "active"
}
```

**Fields:**
- `project_id` - к какому проекту относится
- `context_id` - в каком контексте выполнять (дома, офис)
- `tag_ids` - категории для фильтрации
- `priority` - low, medium, high
- `status` - inbox, active, completed, waiting, someday

### 3. Organize (Организация)

Установка задачи как Next Action (следующее действие):

```javascript
POST /api/v1/tasks/{id}/next-action
```

**Use case:** Выбрать задачу для выполнения сейчас.

**Response:**
```json
{
  "id": 1,
  "title": "Task title",
  "is_next_action": true,
  ...
}
```

Получить все next actions:
```javascript
GET /api/v1/tasks/next-actions
```

### 4. Engage (Выполнение)

Завершение задачи:

```javascript
POST /api/v1/tasks/{id}/complete
```

**Response:**
```json
{
  "id": 1,
  "status": "completed",
  "completed_at": "2026-03-12T10:00:00Z"
}
```

### 5. Review (Обзор)

Получение задач по статусам:

```javascript
// Waiting for (ожидающие)
GET /api/v1/tasks?status=waiting

// Someday (когда-нибудь)
GET /api/v1/tasks?status=someday

// Completed (завершенные)
GET /api/v1/tasks?status=completed
```

---

## Task Filtering

### Filter by Status
```javascript
GET /api/v1/tasks?status=active
GET /api/v1/tasks?status=completed
GET /api/v1/tasks?status=waiting
GET /api/v1/tasks?status=someday
```

### Filter by Priority
```javascript
GET /api/v1/tasks?priority=high
GET /api/v1/tasks?priority=medium
GET /api/v1/tasks?priority=low
```

### Filter by Context
```javascript
GET /api/v1/tasks?context_id=1
```

### Filter by Project
```javascript
GET /api/v1/tasks?project_id=1
```

### Filter by Area
```javascript
GET /api/v1/tasks?area_id=1
```

### Combine Filters
```javascript
GET /api/v1/tasks?status=active&priority=high&context_id=1
```

---

## Project Management

### Create Project with Area
```javascript
POST /api/v1/projects
{
  "name": "Learning Python",
  "description": "Learn FastAPI and SQLAlchemy",
  "area_id": 1
}
```

### Add Subtask to Project
```javascript
POST /api/v1/projects/{project_id}/subtasks
{
  "title": "Read documentation",
  "task_id": 1  // optional: link to main task
}
```

### Complete Project
```javascript
POST /api/v1/projects/{project_id}/complete
```

**Response:**
```json
{
  "id": 1,
  "name": "Learning Python",
  "status": "completed",
  "progress": 100
}
```

### Get Project with Progress
```javascript
GET /api/v1/projects/{id}

// Response includes
{
  "id": 1,
  "name": "Project name",
  "status": "active",
  "progress": 45,
  "total_tasks": 20,
  "completed_tasks": 9
}
```

---

## Tag Assignment

### Create Task with Tags
```javascript
POST /api/v1/tasks
{
  "title": "Task title",
  "tag_ids": [1, 2, 3]
}
```

### Update Task Tags
```javascript
PUT /api/v1/tasks/{id}
{
  "tag_ids": [1, 3]  // replace all tags
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (delete) |
| 400 | Bad Request |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

### Error Response Format
```json
{
  "detail": "Error message here"
}
```

### Common Errors

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Solution:** Проверьте, что все обязательные поля заполнены.

#### 404 Not Found
```json
{
  "detail": "Tag not found"
}
```

**Solution:** Проверьте, что ID существует.

#### 400 Bad Request
```json
{
  "detail": "Cannot set next action for completed task"
}
```

**Solution:** Проверьте статус задачи.

---

## Best Practices

### 1. Use Inbox for Quick Capture
```javascript
// Fast capture
POST /api/v1/inbox
{"title": "Buy milk"}

// Later, organize into structure
PUT /api/v1/tasks/{id}
{
  "project_id": 1,
  "context_id": 2,
  "tag_ids": [1]
}
```

### 2. Limit Next Actions
```javascript
// Get only next actions for current context
GET /api/v1/tasks/next-actions?context_id=1
```

### 3. Use Tags for Cross-Project Filtering
```javascript
// Tag "Urgent" for urgent tasks
GET /api/v1/tags/1/tasks  // get all urgent tasks
```

### 4. Regular Review
```javascript
// Weekly review: get all active and waiting tasks
GET /api/v1/tasks?status=active
GET /api/v1/tasks?status=waiting
```

### 5. Pagination for Large Lists
```javascript
GET /api/v1/tasks?page=1&limit=20
```

### 6. Handle Errors Gracefully
```javascript
try {
  const response = await fetch(url, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return await response.json();
} catch (error) {
  console.error('API Error:', error.message);
}
```

---

## Testing

### Using curl
```bash
# Create tag
curl -X POST http://localhost:8000/api/v1/tags \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "color": "#FF0000"}'

# Get tasks
curl http://localhost:8000/api/v1/tasks
```

### Using Swagger UI
1. Откройте http://localhost:8000/docs
2. Выберите endpoint
3. Нажмите "Try it out"
4. Заполните параметры
5. Нажмите "Execute"

### Using Test Script
```bash
./test_api.sh
```

---

## Additional Resources

- [API Examples](API_EXAMPLES.md)
- [Schema Documentation](SCHEMA_DOCUMENTATION.md)
- [Integration Guide](INTEGRATION_GUIDE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [OpenAPI Specification](openapi.json)