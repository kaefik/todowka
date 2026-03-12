# Todo API Examples

Примеры запросов и ответов для всех endpoints Todo API.

## Table of Contents
- [Tags](#tags)
- [Contexts](#contexts)
- [Areas](#areas)
- [Projects](#projects)
- [Tasks](#tasks)
- [Inbox](#inbox)
- [Notifications](#notifications)

---

## Tags

### Create Tag

**Request:**
```bash
POST /api/v1/tags
Content-Type: application/json

{
  "name": "Work",
  "color": "#FF0000"
}
```

**Response: 201 Created**
```json
{
  "id": 1,
  "name": "Work",
  "color": "#FF0000",
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T10:00:00Z"
}
```

### Get All Tags

**Request:**
```bash
GET /api/v1/tags
```

**Response: 200 OK**
```json
[
  {
    "id": 1,
    "name": "Work",
    "color": "#FF0000",
    "created_at": "2026-03-12T10:00:00Z",
    "updated_at": "2026-03-12T10:00:00Z"
  },
  {
    "id": 2,
    "name": "Personal",
    "color": "#00FF00",
    "created_at": "2026-03-12T10:05:00Z",
    "updated_at": "2026-03-12T10:05:00Z"
  }
]
```

### Get Tag by ID

**Request:**
```bash
GET /api/v1/tags/1
```

**Response: 200 OK**
```json
{
  "id": 1,
  "name": "Work",
  "color": "#FF0000",
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T10:00:00Z"
}
```

### Update Tag

**Request:**
```bash
PUT /api/v1/tags/1
Content-Type: application/json

{
  "name": "Work - Updated",
  "color": "#00FF00"
}
```

**Response: 200 OK**
```json
{
  "id": 1,
  "name": "Work - Updated",
  "color": "#00FF00",
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T11:00:00Z"
}
```

### Delete Tag

**Request:**
```bash
DELETE /api/v1/tags/1
```

**Response: 204 No Content**

---

## Contexts

### Create Context

**Request:**
```bash
POST /api/v1/contexts
Content-Type: application/json

{
  "name": "Office",
  "description": "Work at office"
}
```

**Response: 201 Created**
```json
{
  "id": 1,
  "name": "Office",
  "description": "Work at office",
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T10:00:00Z"
}
```

### Get All Contexts

**Request:**
```bash
GET /api/v1/contexts
```

**Response: 200 OK**
```json
[
  {
    "id": 1,
    "name": "Office",
    "description": "Work at office",
    "created_at": "2026-03-12T10:00:00Z",
    "updated_at": "2026-03-12T10:00:00Z"
  },
  {
    "id": 2,
    "name": "Home",
    "description": "Work from home",
    "created_at": "2026-03-12T10:05:00Z",
    "updated_at": "2026-03-12T10:05:00Z"
  }
]
```

---

## Areas

### Create Area

**Request:**
```bash
POST /api/v1/areas
Content-Type: application/json

{
  "name": "Career",
  "description": "Professional development"
}
```

**Response: 201 Created**
```json
{
  "id": 1,
  "name": "Career",
  "description": "Professional development",
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T10:00:00Z"
}
```

### Get All Areas

**Request:**
```bash
GET /api/v1/areas
```

**Response: 200 OK**
```json
[
  {
    "id": 1,
    "name": "Career",
    "description": "Professional development",
    "created_at": "2026-03-12T10:00:00Z",
    "updated_at": "2026-03-12T10:00:00Z"
  },
  {
    "id": 2,
    "name": "Health",
    "description": "Physical and mental health",
    "created_at": "2026-03-12T10:05:00Z",
    "updated_at": "2026-03-12T10:05:00Z"
  }
]
```

---

## Projects

### Create Project

**Request:**
```bash
POST /api/v1/projects
Content-Type: application/json

{
  "name": "Learning Python",
  "description": "Learn FastAPI and SQLAlchemy",
  "area_id": 1
}
```

**Response: 201 Created**
```json
{
  "id": 1,
  "name": "Learning Python",
  "description": "Learn FastAPI and SQLAlchemy",
  "area_id": 1,
  "status": "active",
  "progress": 0,
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T10:00:00Z"
}
```

### Get All Projects (Paginated)

**Request:**
```bash
GET /api/v1/projects?page=1&limit=10
```

**Response: 200 OK**
```json
{
  "items": [
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
  ],
  "total": 1,
  "page": 1,
  "limit": 10,
  "pages": 1
}
```

### Complete Project

**Request:**
```bash
POST /api/v1/projects/1/complete
```

**Response: 200 OK**
```json
{
  "id": 1,
  "name": "Learning Python",
  "status": "completed",
  "progress": 100,
  "completed_at": "2026-03-12T12:00:00Z"
}
```

---

## Tasks

### Create Task with Tags

**Request:**
```bash
POST /api/v1/tasks
Content-Type: application/json

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

**Response: 201 Created**
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
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T10:00:00Z"
}
```

### Get All Tasks (Filtered)

**Request:**
```bash
GET /api/v1/tasks?status=active&priority=high&context_id=1
```

**Response: 200 OK**
```json
[
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
    "created_at": "2026-03-12T10:00:00Z",
    "updated_at": "2026-03-12T10:00:00Z"
  }
]
```

### Set Task as Next Action

**Request:**
```bash
POST /api/v1/tasks/1/next-action
```

**Response: 200 OK**
```json
{
  "id": 1,
  "title": "Complete API tutorial",
  "is_next_action": true,
  ...
}
```

### Get Next Actions

**Request:**
```bash
GET /api/v1/tasks/next-actions
```

**Response: 200 OK**
```json
[
  {
    "id": 1,
    "title": "Complete API tutorial",
    "description": "Finish the tutorial",
    "status": "active",
    "priority": "high",
    "is_next_action": true,
    ...
  }
]
```

### Complete Task

**Request:**
```bash
POST /api/v1/tasks/1/complete
```

**Response: 200 OK**
```json
{
  "id": 1,
  "title": "Complete API tutorial",
  "status": "completed",
  "priority": "high",
  "completed_at": "2026-03-12T12:00:00Z"
}
```

### Toggle Complete Task

**Request:**
```bash
POST /api/v1/tasks/1/toggle-complete
```

**Response: 200 OK**
```json
{
  "id": 1,
  "title": "Complete API tutorial",
  "status": "completed",
  "completed_at": "2026-03-12T12:00:00Z"
}
```

---

## Inbox

### Create Inbox Task

**Request:**
```bash
POST /api/v1/inbox
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs"
}
```

**Response: 201 Created**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "status": "inbox",
  "priority": "medium",
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T10:00:00Z"
}
```

### Get Inbox Tasks

**Request:**
```bash
GET /api/v1/inbox
```

**Response: 200 OK**
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "status": "inbox",
    "priority": "medium",
    "created_at": "2026-03-12T10:00:00Z",
    "updated_at": "2026-03-12T10:00:00Z"
  },
  {
    "id": 2,
    "title": "Call mom",
    "description": "Weekly check-in",
    "status": "inbox",
    "priority": "medium",
    "created_at": "2026-03-12T10:05:00Z",
    "updated_at": "2026-03-12T10:05:00Z"
  }
]
```

---

## Notifications

### Get All Notifications

**Request:**
```bash
GET /api/v1/notifications
```

**Response: 200 OK**
```json
[
  {
    "id": 1,
    "message": "Task reminder",
    "task_id": 1,
    "status": "pending",
    "scheduled_at": "2026-03-12T14:00:00Z",
    "created_at": "2026-03-12T10:00:00Z",
    "updated_at": "2026-03-12T10:00:00Z"
  }
]
```

### Get Notification by ID

**Request:**
```bash
GET /api/v1/notifications/1
```

**Response: 200 OK**
```json
{
  "id": 1,
  "message": "Task reminder",
  "task_id": 1,
  "status": "pending",
  "scheduled_at": "2026-03-12T14:00:00Z",
  "created_at": "2026-03-12T10:00:00Z",
  "updated_at": "2026-03-12T10:00:00Z"
}
```

---

## Error Examples

### 404 Not Found

**Request:**
```bash
GET /api/v1/tags/999
```

**Response: 404 Not Found**
```json
{
  "detail": "Tag not found"
}
```

### 422 Validation Error

**Request:**
```bash
POST /api/v1/tags
Content-Type: application/json

{
  "color": "#FF0000"
}
```

**Response: 422 Unprocessable Entity**
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 400 Bad Request

**Request:**
```bash
POST /api/v1/tasks/999/complete
```

**Response: 400 Bad Request**
```json
{
  "detail": "Task not found"
}
```

---

## Using curl

### Create Tag
```bash
curl -X POST http://localhost:8000/api/v1/tags \
  -H "Content-Type: application/json" \
  -d '{"name": "Work", "color": "#FF0000"}'
```

### Get Tasks
```bash
curl http://localhost:8000/api/v1/tasks
```

### Create Task
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test task",
    "description": "Description",
    "priority": "high",
    "tag_ids": [1]
  }'
```

### Complete Task
```bash
curl -X POST http://localhost:8000/api/v1/tasks/1/complete
```

---

## Using JavaScript (fetch)

### Create Task
```javascript
const createTask = async () => {
  const response = await fetch('http://localhost:8000/api/v1/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title: 'Test task',
      description: 'Description',
      priority: 'high',
      tag_ids: [1]
    })
  });

  if (!response.ok) {
    throw new Error('Failed to create task');
  }

  return await response.json();
};
```

### Get Tasks
```javascript
const getTasks = async () => {
  const response = await fetch('http://localhost:8000/api/v1/tasks');

  if (!response.ok) {
    throw new Error('Failed to get tasks');
  }

  return await response.json();
};
```

---

## Full Workflow Example

```javascript
// 1. Create supporting entities
const workTag = await fetch('/api/v1/tags', {
  method: 'POST',
  body: JSON.stringify({name: 'Work', color: '#FF0000'})
}).then(r => r.json());

const officeContext = await fetch('/api/v1/contexts', {
  method: 'POST',
  body: JSON.stringify({name: 'Office', description: 'Work at office'})
}).then(r => r.json());

const careerArea = await fetch('/api/v1/areas', {
  method: 'POST',
  body: JSON.stringify({name: 'Career', description: 'Professional development'})
}).then(r => r.json());

const project = await fetch('/api/v1/projects', {
  method: 'POST',
  body: JSON.stringify({
    name: 'Learning API',
    area_id: careerArea.id
  })
}).then(r => r.json());

// 2. Create task with all relationships
const task = await fetch('/api/v1/tasks', {
  method: 'POST',
  body: JSON.stringify({
    title: 'Complete API tutorial',
    description: 'Finish the tutorial',
    project_id: project.id,
    context_id: officeContext.id,
    tag_ids: [workTag.id],
    priority: 'high'
  })
}).then(r => r.json());

// 3. Set as next action
await fetch(`/api/v1/tasks/${task.id}/next-action`, {
  method: 'POST'
});

// 4. Complete task
await fetch(`/api/v1/tasks/${task.id}/complete`, {
  method: 'POST'
});
```