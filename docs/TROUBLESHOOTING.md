# Troubleshooting Guide

Решение распространенных проблем при работе с Todo API.

## Table of Contents
1. [Connection Issues](#connection-issues)
2. [API Errors](#api-errors)
3. [Data Issues](#data-issues)
4. [Performance Issues](#performance-issues)
5. [Development Issues](#development-issues)

---

## Connection Issues

### Problem: Connection Refused

**Symptoms:**
```
Error: connect ECONNREFUSED 127.0.0.1:8000
```

**Solutions:**

1. **Check if API is running:**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

2. **Start API server:**
   ```bash
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

3. **Check port is available:**
   ```bash
   lsof -i :8000
   ```

4. **Verify firewall settings:**
   ```bash
   sudo firewall-cmd --list-ports
   ```

---

### Problem: Timeout

**Symptoms:**
```
Error: Request timeout after 30000ms
```

**Solutions:**

1. **Increase timeout in client:**
   ```javascript
   const response = await fetch(url, {
     signal: AbortSignal.timeout(30000) // 30 seconds
   });
   ```

2. **Check server performance:**
   ```bash
   top
   htop
   ```

3. **Reduce query complexity:**
   ```javascript
   // Instead of getting all tasks
   GET /api/v1/tasks

   // Use pagination
   GET /api/v1/tasks?page=1&limit=20
   ```

---

### Problem: CORS Error

**Symptoms:**
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000'
has been blocked by CORS policy
```

**Solutions:**

1. **Check CORS settings in `app/main.py`:**
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Or specific origins
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Restart API server after CORS changes**

---

## API Errors

### Problem: 404 Not Found

**Symptoms:**
```json
{"detail": "Entity not found"}
```

**Common Causes:**
- Wrong endpoint URL
- Non-existent ID
- Missing API version prefix

**Solutions:**

1. **Check URL format:**
   ```javascript
   // Wrong
   GET http://localhost:8000/tags

   // Correct
   GET http://localhost:8000/api/v1/tags
   ```

2. **Verify ID exists:**
   ```javascript
   // First, get all to check ID
   const all = await api.get('/tags');
   const exists = all.find(t => t.id === id);

   if (!exists) {
     throw new Error('Tag not found');
   }
   ```

3. **Check documentation:**
   - Visit `http://localhost:8000/docs`
   - Verify endpoint exists

---

### Problem: 422 Validation Error

**Symptoms:**
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Common Causes:**
- Missing required fields
- Invalid data types
- Wrong enum values
- String length exceeded

**Solutions:**

1. **Check required fields:**
   ```javascript
   // Check schema documentation
   // Example: Tag requires "name"
   POST /api/v1/tags
   {
     "name": "Work",  // Required
     "color": "#FF0000"  // Optional
   }
   ```

2. **Validate enum values:**
   ```javascript
   // Wrong
   {"status": "new", "priority": "urgent"}

   // Correct
   {"status": "inbox", "priority": "high"}
   ```

3. **Check string lengths:**
   ```javascript
   // Tag name: max 100 chars
   // Task title: max 200 chars
   // Description: max 500-1000 chars
   ```

4. **Validate data types:**
   ```javascript
   // Wrong
   {"project_id": "1"}  // String

   // Correct
   {"project_id": 1}  // Integer
   ```

---

### Problem: 400 Bad Request

**Symptoms:**
```json
{"detail": "Cannot set next action for completed task"}
```

**Common Causes:**
- Invalid action for current state
- Logic conflict

**Solutions:**

1. **Check task status before action:**
   ```javascript
   const task = await api.get(`/tasks/${id}`);

   if (task.status === 'completed') {
     console.log('Cannot modify completed task');
     return;
   }
   ```

2. **Review error message:**
   - Error messages are descriptive
   - Follow suggested action

---

### Problem: 500 Internal Server Error

**Symptoms:**
```json
{"detail": "Internal server error"}
```

**Common Causes:**
- Database connection issue
- Server-side bug
- Invalid data format

**Solutions:**

1. **Check server logs:**
   ```bash
   # If running with uvicorn
   # Check terminal output

   # Or check log files
   tail -f app.log
   ```

2. **Check database connection:**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

3. **Restart API server:**
   ```bash
   # Stop server (Ctrl+C)
   # Start again
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

---

## Data Issues

### Problem: Task Not Showing

**Symptoms:**
- Task created but not in list
- Filter not working

**Solutions:**

1. **Check task status:**
   ```javascript
   // Inbox tasks only show in /inbox
   // Active tasks show in /tasks
   const inboxTasks = await api.get('/inbox');
   const activeTasks = await api.get('/tasks?status=active');
   ```

2. **Verify filters:**
   ```javascript
   // Remove filters temporarily
   GET /api/v1/tasks

   // Apply filters one by one
   GET /api/v1/tasks?status=active
   GET /api/v1/tasks?status=active&priority=high
   ```

3. **Check pagination:**
   ```javascript
   // Task might be on different page
   GET /api/v1/tasks?page=2&limit=10
   ```

---

### Problem: Tags Not Associating

**Symptoms:**
- Tags created but not linked to task
- `tag_ids` array not working

**Solutions:**

1. **Use correct field name:**
   ```javascript
   // Correct field name is "tag_ids" (plural)
   POST /api/v1/tasks
   {
     "title": "Task",
     "tag_ids": [1, 2, 3]  // Correct
   }
   ```

2. **Verify tag IDs exist:**
   ```javascript
   const tags = await api.get('/tags');
   const tagIds = tags.map(t => t.id);

   // Only use existing IDs
   const task = await api.post('/tasks', {
     title: 'Task',
     tag_ids: tagIds  // Use valid IDs
   });
   ```

3. **Check for duplicates:**
   ```javascript
   // tag_ids array should have unique values
   tag_ids: [1, 2, 3]  // Correct
   tag_ids: [1, 1, 2]  // Wrong (duplicate)
   ```

---

### Problem: Progress Not Updating

**Symptoms:**
- Project progress stuck at 0%
- Completed tasks not counted

**Solutions:**

1. **Complete tasks properly:**
   ```javascript
   // Wrong (just update status)
   PUT /api/v1/tasks/1
   {"status": "completed"}

   // Correct (use complete endpoint)
   POST /api/v1/tasks/1/complete
   ```

2. **Refresh project data:**
   ```javascript
   // Get fresh project data
   const project = await api.get(`/projects/${projectId}`);
   console.log('Progress:', project.progress);
   ```

3. **Check task belongs to project:**
   ```javascript
   const task = await api.get(`/tasks/${taskId}`);
   if (task.project_id !== projectId) {
     console.log('Task not in this project');
   }
   ```

---

## Performance Issues

### Problem: Slow Loading

**Symptoms:**
- API responses take > 5 seconds
- UI freezes on data fetch

**Solutions:**

1. **Use pagination:**
   ```javascript
   // Instead of
   GET /api/v1/tasks

   // Use
   GET /api/v1/tasks?page=1&limit=20
   ```

2. **Apply filters:**
   ```javascript
   // Reduce data by filtering
   GET /api/v1/tasks?status=active&context_id=1
   ```

3. **Implement caching:**
   ```javascript
   const cache = new Map();
   const CACHE_TTL = 60000; // 1 minute

   async function getCachedData(key, fetchFn) {
     const cached = cache.get(key);
     if (cached && Date.now() - cached.time < CACHE_TTL) {
       return cached.data;
     }

     const data = await fetchFn();
     cache.set(key, { data, time: Date.now() });
     return data;
   }
   ```

4. **Use loading states:**
   ```javascript
   const [loading, setLoading] = useState(false);

   const fetchTasks = async () => {
     setLoading(true);
     try {
       const tasks = await api.get('/tasks');
       setTasks(tasks);
     } finally {
       setLoading(false);
     }
   };
   ```

---

### Problem: Memory Leak

**Symptoms:**
- Browser tab consumes high memory
- Page becomes unresponsive over time

**Solutions:**

1. **Clean up intervals:**
   ```javascript
   useEffect(() => {
     const interval = setInterval(fetchTasks, 30000);

     return () => clearInterval(interval); // Cleanup
   }, []);
   ```

2. **Unsubscribe from events:**
   ```javascript
   useEffect(() => {
     const poller = new TaskPoller(api);
     poller.start(onUpdate);

     return () => poller.stop(); // Cleanup
   }, []);
   ```

3. **Limit cache size:**
   ```javascript
   const MAX_CACHE_SIZE = 100;

   function setCache(key, value) {
     if (cache.size >= MAX_CACHE_SIZE) {
       // Remove oldest entry
       const oldestKey = cache.keys().next().value;
       cache.delete(oldestKey);
     }
     cache.set(key, value);
   }
   ```

---

## Development Issues

### Problem: Import Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'app'
```

**Solutions:**

1. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Check Python path:**
   ```bash
   export PYTHONPATH="${PYTHONPATH}:."
   ```

---

### Problem: Database Locked

**Symptoms:**
```
sqlite3.OperationalError: database is locked
```

**Solutions:**

1. **Close all connections:**
   ```bash
   # Stop API server
   # Stop any running tests
   ```

2. **Remove database lock:**
   ```bash
   rm -f database.db-journal
   ```

3. **Use WAL mode:**
   ```python
   # In app/dependencies.py
   engine = create_engine(
       settings.DATABASE_URL,
       connect_args={
           "check_same_thread": False,
           "journal_mode": "wal"
       }
   )
   ```

---

### Problem: Port Already in Use

**Symptoms:**
```
OSError: [Errno 48] Address already in use
```

**Solutions:**

1. **Find and kill process:**
   ```bash
   # Find process using port 8000
   lsof -i :8000

   # Kill process
   kill -9 <PID>
   ```

2. **Use different port:**
   ```bash
   uvicorn app.main:app --port 8001
   ```

---

### Problem: Tests Failing

**Symptoms:**
```
pytest errors, integration tests not passing
```

**Solutions:**

1. **Check database tables:**
   ```bash
   # Ensure models are imported in test file
   from app.models.task import Task
   from app.models.project import Project
   from app.models.tag import Tag
   ```

2. **Run tests individually:**
   ```bash
   # Run specific test
   pytest tests/integration/test_api.py::test_create_tag -v

   # Run unit tests only
   pytest tests/unit/ -v
   ```

3. **Check for import order:**
   ```python
   # Import models before Base.metadata.create_all()
   from app.models.task import Task
   from app.models.project import Project
   from app.models.tag import Tag
   from app.models.base import Base
   ```

---

## Debugging Tips

### Enable Logging

```python
# In app/main.py
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.get("/")
def root():
    logger.debug("Root endpoint called")
    return {"message": "Hello"}
```

### Use Browser DevTools

```javascript
// Open Console (F12)
// Add debug logging
console.log('Fetching tasks...');
const tasks = await api.get('/tasks');
console.log('Tasks received:', tasks);
```

### Check Network Tab

1. Open DevTools (F12)
2. Go to Network tab
3. Make API request
4. Click request
5. Check:
   - Request headers
   - Response status
   - Response body
   - Timing

### Test with curl

```bash
# Simple test
curl -v http://localhost:8000/api/v1/health

# With data
curl -X POST http://localhost:8000/api/v1/tags \
  -H "Content-Type: application/json" \
  -d '{"name": "Test"}' \
  -v

# View headers
curl -I http://localhost:8000/api/v1/tags
```

---

## Getting Help

### Documentation
- [Developer Guide](DEVELOPER_GUIDE.md)
- [API Examples](API_EXAMPLES.md)
- [Schema Documentation](SCHEMA_DOCUMENTATION.md)
- [Integration Guide](INTEGRATION_GUIDE.md)
- [LLM Instructions](LLM_INSTRUCTIONS.md)

### Interactive Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### OpenAPI Specification
- Download: http://localhost:8000/openapi.json
- Use with API clients (Postman, Insomnia)

### Test Script
```bash
./test_api.sh
```

### Server Health Check
```bash
curl http://localhost:8000/api/v1/health
```

---

## Quick Fixes Checklist

- [ ] API server is running
- [ ] Correct URL (include `/api/v1/`)
- [ ] Content-Type header is set
- [ ] IDs are integers
- [ ] Required fields are present
- [ ] Enum values are correct
- [ ] Referenced entities exist
- [ ] Database is not locked
- [ ] No port conflicts
- [ ] CORS is configured
- [ ] Virtual environment is activated
- [ ] Dependencies are installed
- [ ] Response status is checked
- [ ] Error handling is in place
- [ ] Pagination is used for large datasets