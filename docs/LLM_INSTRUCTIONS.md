# Instructions for LLM (Claude, GPT-4, etc.)

Специальные инструкции для LLM при работе с Todo API.

## Context

You are working with a Todo API that implements GTD (Getting Things Done) methodology for task management. The API is built with FastAPI and uses RESTful architecture.

## API Configuration

- **Base URL**: `http://localhost:8000`
- **API Version**: `/api/v1`
- **Interactive Documentation**: `http://localhost:8000/docs`
- **OpenAPI Specification**: `http://localhost:8000/openapi.json`
- **Authentication**: None (public API in current version)

## Important Notes

### 1. Request Format
- All POST/PUT requests require `Content-Type: application/json` header
- JSON body for all POST/PUT requests
- IDs are integers, not strings
- Datetimes are ISO 8601 strings

### 2. Response Format
- Success: Returns JSON with entity data
- Created: Returns 201 status with created entity
- No Content: 204 status for DELETE operations
- Error: Returns JSON with `{"detail": "error message"}`

### 3. Validation Errors (422)
- Returned as array of validation errors
- Format: `{"detail": [{"loc": ["body", "field"], "msg": "error", "type": "type"}]}`
- Check required fields and data types

### 4. Not Found Errors (404)
- Simple format: `{"detail": "Entity not found"}`
- Check if ID exists before update/delete

### 5. Common Patterns

**Create Entity:**
```
POST /api/v1/{entity}
{
  "required_field": "value",
  "optional_field": "value"
}
```

**Get All:**
```
GET /api/v1/{entity}?page=1&limit=10
```

**Get Single:**
```
GET /api/v1/{entity}/{id}
```

**Update:**
```
PUT /api/v1/{entity}/{id}
{
  "field": "new_value"
}
```

**Delete:**
```
DELETE /api/v1/{entity}/{id}
```

## Entity Details

### Tag
- **Required**: `name` (string, max 100 chars)
- **Optional**: `color` (string, HEX format like #FF0000)
- **Auto**: `id`, `created_at`, `updated_at`
- **Endpoints**: `/api/v1/tags`

### Context
- **Required**: `name` (string, max 100 chars)
- **Optional**: `description` (string, max 500 chars)
- **Auto**: `id`, `created_at`, `updated_at`
- **Endpoints**: `/api/v1/contexts`

### Area
- **Required**: `name` (string, max 100 chars)
- **Optional**: `description` (string, max 500 chars)
- **Auto**: `id`, `created_at`, `updated_at`
- **Endpoints**: `/api/v1/areas`

### Project
- **Required**: `name` (string, max 100 chars)
- **Optional**: `description`, `area_id`
- **Auto**: `id`, `status`, `progress`, `total_tasks`, `completed_tasks`, `created_at`, `updated_at`
- **Status**: `active`, `completed`
- **Endpoints**: `/api/v1/projects`
- **Special**: `POST /api/v1/projects/{id}/complete`, `POST /api/v1/projects/{id}/subtasks`

### Task
- **Required**: `title` (string, max 200 chars)
- **Optional**: `description`, `status`, `priority`, `project_id`, `context_id`, `tag_ids`
- **Auto**: `id`, `is_next_action`, `completed_at`, `reminder_at`, `created_at`, `updated_at`
- **Status**: `inbox`, `active`, `completed`, `waiting`, `someday`
- **Priority**: `low`, `medium`, `high`
- **Endpoints**: `/api/v1/tasks`
- **Special**: `POST /api/v1/tasks/{id}/complete`, `POST /api/v1/tasks/{id}/next-action`, `POST /api/v1/tasks/{id}/toggle-complete`
- **Filters**: `status`, `priority`, `project_id`, `context_id`, `area_id`

### Inbox
- **Special endpoint for quick capture**: `/api/v1/inbox`
- **Required**: `title` (string, max 200 chars)
- **Optional**: `description`
- **Auto**: Sets `status` to `inbox`

## GTD Workflow Implementation

### 1. Capture (Захват)
Use inbox endpoint for quick capture without details:
```
POST /api/v1/inbox
{
  "title": "Quick task"
}
```

### 2. Clarify (Уточнение)
Move from inbox to organized structure:
```
POST /api/v1/tasks
{
  "title": "Organized task",
  "project_id": 1,
  "context_id": 1,
  "tag_ids": [1, 2],
  "priority": "high"
}
```

### 3. Organize (Организация)
Set task as next action:
```
POST /api/v1/tasks/{id}/next-action
```

Get all next actions:
```
GET /api/v1/tasks/next-actions
```

### 4. Engage (Выполнение)
Complete task:
```
POST /api/v1/tasks/{id}/complete
```

### 5. Review (Обзор)
Get tasks by status:
```
GET /api/v1/tasks?status=waiting
GET /api/v1/tasks?status=someday
GET /api/v1/tasks?status=completed
```

## Tag Assignment

**Create task with tags:**
```json
{
  "title": "Task",
  "tag_ids": [1, 2, 3]
}
```

**Update task tags:**
```json
{
  "tag_ids": [1, 3]
}
```

**Note**: `tag_ids` replaces all existing tags, doesn't append.

## Pagination

**Query Parameters:**
- `page` (default: 1)
- `limit` (default: 10)

**Response Format:**
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "limit": 20,
  "pages": 5
}
```

**Use for:**
- `/api/v1/tasks?page=1&limit=20`
- `/api/v1/projects?page=1&limit=10`

## Filtering Tasks

Combine multiple filters:
```
GET /api/v1/tasks?status=active&priority=high&context_id=1
```

**Available filters:**
- `status`: inbox, active, completed, waiting, someday
- `priority`: low, medium, high
- `project_id`: integer
- `context_id`: integer
- `area_id`: integer

## Error Handling Patterns

### 400 Bad Request
Invalid action or state conflict.
Example: Cannot set next action for completed task.

### 404 Not Found
Resource with given ID doesn't exist.
Always check existence before update/delete.

### 422 Validation Error
Missing required fields or invalid data types.
Check the `detail` array for specific field errors.

### 500 Internal Server Error
Server error. Check server logs.

## Common Mistakes to Avoid

### 1. Missing Content-Type
❌ Wrong:
```javascript
fetch('/api/v1/tags', {
  method: 'POST',
  body: JSON.stringify({name: 'Work'})
})
```

✅ Correct:
```javascript
fetch('/api/v1/tags', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({name: 'Work'})
})
```

### 2. Using String IDs
❌ Wrong:
```javascript
fetch('/api/v1/tags/' + id) // id might be string
```

✅ Correct:
```javascript
fetch('/api/v1/tags/' + parseInt(id))
```

### 3. Wrong Status Values
❌ Wrong:
```json
{"status": "new", "priority": "urgent"}
```

✅ Correct:
```json
{"status": "inbox", "priority": "high"}
```

### 4. Missing Required Fields
❌ Wrong:
```json
{"color": "#FF0000"} // missing "name" field
```

✅ Correct:
```json
{"name": "Work", "color": "#FF0000"}
```

### 5. Non-existent References
❌ Wrong:
```json
{"project_id": 999} // project doesn't exist
```

✅ Correct:
```json
{"project_id": 1} // valid project ID
```

## Best Practices for LLM

1. **Always use full URLs**: Start with `http://localhost:8000/api/v1/`
2. **Include headers**: Always add `Content-Type: application/json`
3. **Validate IDs**: Ensure referenced IDs exist before creating tasks
4. **Use correct enums**: Only use allowed values for status, priority, etc.
5. **Handle errors gracefully**: Always include error handling in code
6. **Use inbox for quick capture**: Don't require all details for initial task creation
7. **Use next actions**: When user wants to select tasks for execution
8. **Filter appropriately**: Use query parameters to reduce data transfer
9. **Use pagination**: For large datasets, always use page/limit parameters
10. **Check response status**: Always verify `response.ok` before processing data

## Code Generation Templates

### Basic Fetch
```javascript
const response = await fetch('http://localhost:8000/api/v1/endpoint', {
  method: 'GET',
  headers: {'Content-Type': 'application/json'}
});

if (!response.ok) {
  const error = await response.json();
  throw new Error(error.detail);
}

return await response.json();
```

### Create with Tags
```javascript
const task = await fetch('http://localhost:8000/api/v1/tasks', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    title: 'Task title',
    description: 'Task description',
    project_id: 1,
    context_id: 1,
    tag_ids: [1, 2, 3],
    priority: 'high',
    status: 'active'
  })
}).then(r => r.json());
```

### GTD Complete Workflow
```javascript
// 1. Capture to inbox
const inboxTask = await fetch('http://localhost:8000/api/v1/inbox', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({title: 'Buy groceries'})
}).then(r => r.json());

// 2. Organize with details
const organizedTask = await fetch(`http://localhost:8000/api/v1/tasks/${inboxTask.id}`, {
  method: 'PUT',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    project_id: 1,
    context_id: 1,
    tag_ids: [1]
  })
}).then(r => r.json());

// 3. Set as next action
await fetch(`http://localhost:8000/api/v1/tasks/${organizedTask.id}/next-action`, {
  method: 'POST'
});

// 4. Complete task
await fetch(`http://localhost:8000/api/v1/tasks/${organizedTask.id}/complete`, {
  method: 'POST'
});
```

## Example Prompts

### Create a new task
```
Create a task with title "Complete API tutorial", description "Finish the tutorial", project ID 1, context ID 2, tags [1, 3], high priority, and active status.
```

### Get all next actions
```
Get all tasks with is_next_action=true. Also include their project and context details.
```

### Complete a GTD workflow
```
Help me implement the GTD workflow:
1. Create an inbox task: "Call client"
2. Organize it with project ID 5 and context ID 3
3. Set it as a next action
4. Show me how to complete it later
```

### Filter tasks
```
Get all active tasks with high priority in context ID 1. Use pagination with limit 20.
```

## Additional Resources

- [Developer Guide](DEVELOPER_GUIDE.md)
- [API Examples](API_EXAMPLES.md)
- [Schema Documentation](SCHEMA_DOCUMENTATION.md)
- [Integration Guide](INTEGRATION_GUIDE.md)
- [OpenAPI Specification](openapi.json)

## Testing Commands

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Get all tasks
curl http://localhost:8000/api/v1/tasks

# Create tag
curl -X POST http://localhost:8000/api/v1/tags \
  -H "Content-Type: application/json" \
  -d '{"name": "Work", "color": "#FF0000"}'

# Create task
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "priority": "high", "tag_ids": [1]}'

# Complete task
curl -X POST http://localhost:8000/api/v1/tasks/1/complete
```

## Remember

- Always validate IDs before using them
- Use correct enum values (status, priority, etc.)
- Include Content-Type header for POST/PUT
- Handle errors properly (400, 404, 422, 500)
- Use pagination for large datasets
- Leverage filters to reduce data transfer
- Follow GTD workflow: Capture → Clarify → Organize → Engage → Review