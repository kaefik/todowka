# Todo API Integration Guide

Руководство по интеграции Todo API в фронтенд приложения.

## Table of Contents
1. [Setup](#setup)
2. [Authentication](#authentication)
3. [API Client](#api-client)
4. [Common Operations](#common-operations)
5. [Error Handling](#error-handling)
6. [Real-time Updates](#real-time-updates)
7. [Best Practices](#best-practices)
8. [Framework Examples](#framework-examples)

---

## Setup

### API Configuration

```javascript
const API_CONFIG = {
  baseURL: 'http://localhost:8000',
  apiVersion: '/api/v1',
  timeout: 10000, // 10 seconds
  headers: {
    'Content-Type': 'application/json'
  }
};

const getURL = (endpoint) => `${API_CONFIG.baseURL}${API_CONFIG.apiVersion}${endpoint}`;
```

### Environment Variables

```javascript
// .env file
NEXT_PUBLIC_API_URL=http://localhost:8000
VITE_API_URL=http://localhost:8000
REACT_APP_API_URL=http://localhost:8000
```

---

## Authentication

В текущей версии аутентификация не требуется (public API).

```javascript
// For future authentication:
const headers = {
  'Content-Type': 'application/json',
  // 'Authorization': `Bearer ${token}`
};
```

---

## API Client

### Fetch API (Built-in)

```javascript
class TodoAPIClient {
  constructor(baseURL = 'http://localhost:8000/api/v1') {
    this.baseURL = baseURL;
    this.headers = {
      'Content-Type': 'application/json'
    };
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      ...options,
      headers: {
        ...this.headers,
        ...options.headers
      }
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const error = await response.json();
        throw new APIError(error.detail, response.status);
      }

      // 204 No Content
      if (response.status === 204) {
        return null;
      }

      return await response.json();
    } catch (error) {
      if (error instanceof APIError) {
        throw error;
      }
      throw new APIError('Network error', 0);
    }
  }

  get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

class APIError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

// Usage
const api = new TodoAPIClient();
```

---

## Common Operations

### Tags

```javascript
// Get all tags
const tags = await api.get('/tags');

// Create tag
const tag = await api.post('/tags', {
  name: 'Work',
  color: '#FF0000'
});

// Update tag
const updated = await api.put(`/tags/${tag.id}`, {
  name: 'Updated Work',
  color: '#00FF00'
});

// Delete tag
await api.delete(`/tags/${tag.id}`);
```

### Contexts

```javascript
// Get all contexts
const contexts = await api.get('/contexts');

// Create context
const context = await api.post('/contexts', {
  name: 'Office',
  description: 'Work at office'
});

// Update context
const updated = await api.put(`/contexts/${context.id}`, {
  name: 'Updated Office',
  description: 'Updated description'
});

// Delete context
await api.delete(`/contexts/${context.id}`);
```

### Areas

```javascript
// Get all areas
const areas = await api.get('/areas');

// Create area
const area = await api.post('/areas', {
  name: 'Career',
  description: 'Professional development'
});

// Update area
const updated = await api.put(`/areas/${area.id}`, {
  name: 'Updated Career',
  description: 'Updated description'
});

// Delete area
await api.delete(`/areas/${area.id}`);
```

### Projects

```javascript
// Get all projects (paginated)
const projects = await api.get('/projects?page=1&limit=10');

// Create project
const project = await api.post('/projects', {
  name: 'Learning Python',
  description: 'Learn FastAPI and SQLAlchemy',
  area_id: 1
});

// Get project with details
const projectDetails = await api.get(`/projects/${project.id}`);

// Complete project
await api.post(`/projects/${project.id}/complete`);

// Delete project
await api.delete(`/projects/${project.id}`);
```

### Tasks

```javascript
// Get all tasks (filtered)
const tasks = await api.get('/tasks?status=active&priority=high');

// Get next actions
const nextActions = await api.get('/tasks/next-actions');

// Create task
const task = await api.post('/tasks', {
  title: 'Complete API tutorial',
  description: 'Finish tutorial',
  project_id: 1,
  context_id: 1,
  tag_ids: [1, 2],
  priority: 'high',
  status: 'active'
});

// Update task
const updated = await api.put(`/tasks/${task.id}`, {
  title: 'Updated title',
  priority: 'medium'
});

// Set as next action
await api.post(`/tasks/${task.id}/next-action`);

// Complete task
await api.post(`/tasks/${task.id}/complete`);

// Toggle complete
await api.post(`/tasks/${task.id}/toggle-complete`);

// Delete task
await api.delete(`/tasks/${task.id}`);
```

### Inbox

```javascript
// Get inbox tasks
const inboxTasks = await api.get('/inbox');

// Create inbox task
const inboxTask = await api.post('/inbox', {
  title: 'Buy groceries',
  description: 'Milk, bread, eggs'
});
```

### Notifications

```javascript
// Get all notifications
const notifications = await api.get('/notifications');

// Get notification by ID
const notification = await api.get(`/notifications/${notificationId}`);

// Update notification
const updated = await api.put(`/notifications/${notificationId}`, {
  status: 'sent'
});
```

---

## Error Handling

### Try-Catch Pattern

```javascript
try {
  const task = await api.post('/tasks', {
    title: 'New task'
  });
  console.log('Task created:', task);
} catch (error) {
  if (error.status === 422) {
    console.error('Validation error:', error.message);
  } else if (error.status === 404) {
    console.error('Not found:', error.message);
  } else {
    console.error('Unexpected error:', error.message);
  }
}
```

### Error Handler Hook

```javascript
const handleAPIError = (error, showNotification) => {
  switch (error.status) {
    case 400:
      showNotification('Bad request', 'error');
      break;
    case 404:
      showNotification('Resource not found', 'error');
      break;
    case 422:
      showNotification('Invalid data', 'error');
      break;
    case 500:
      showNotification('Server error', 'error');
      break;
    default:
      showNotification('Network error', 'error');
  }
};

// Usage
try {
  const result = await api.get('/tasks');
} catch (error) {
  handleAPIError(error, (title, type) => {
    alert(`${title}: ${error.message}`);
  });
}
```

### Validation Error Handling

```javascript
try {
  const result = await api.post('/tasks', data);
} catch (error) {
  if (error.status === 422 && error.message instanceof Array) {
    // Validation error with field details
    error.message.forEach(fieldError => {
      console.error(`Field: ${fieldError.loc[1]}, Error: ${fieldError.msg}`);
    });
  } else {
    handleAPIError(error);
  }
}
```

---

## Real-time Updates

### Polling Strategy

```javascript
class TaskPoller {
  constructor(apiClient, interval = 30000) {
    this.api = apiClient;
    this.interval = interval;
    this.timeoutId = null;
  }

  start(onUpdate) {
    const poll = async () => {
      try {
        const tasks = await this.api.get('/tasks');
        onUpdate(tasks);
      } catch (error) {
        console.error('Polling error:', error);
      }
      this.timeoutId = setTimeout(poll, this.interval);
    };

    poll();
  }

  stop() {
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
      this.timeoutId = null;
    }
  }
}

// Usage
const poller = new TaskPoller(api, 30000); // 30 seconds
poller.start((tasks) => {
  console.log('Tasks updated:', tasks);
});

// Stop when component unmounts
poller.stop();
```

### WebSocket (Future)

```javascript
// When WebSocket support is added:
const ws = new WebSocket('ws://localhost:8000/ws/tasks');

ws.onmessage = (event) => {
  const task = JSON.parse(event.data);
  console.log('Task update:', task);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('WebSocket closed');
};
```

---

## Best Practices

### 1. Data Caching

```javascript
class CachedAPIClient extends TodoAPIClient {
  constructor(baseURL, cacheTime = 60000) {
    super(baseURL);
    this.cache = new Map();
    this.cacheTime = cacheTime;
  }

  async get(endpoint, options = {}) {
    const cacheKey = endpoint;
    const cached = this.cache.get(cacheKey);

    if (cached && Date.now() - cached.timestamp < this.cacheTime) {
      return cached.data;
    }

    const data = await super.get(endpoint);
    this.cache.set(cacheKey, {
      data,
      timestamp: Date.now()
    });

    return data;
  }

  invalidate(endpoint) {
    this.cache.delete(endpoint);
  }
}
```

### 2. Request Debouncing

```javascript
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Usage for search
const debouncedSearch = debounce(async (query) => {
  const tasks = await api.get(`/tasks?search=${query}`);
}, 300);

// Debounced API calls
input.addEventListener('input', (e) => {
  debouncedSearch(e.target.value);
});
```

### 3. Optimistic Updates

```javascript
async function createTaskOptimistically(title) {
  // Create temporary ID
  const tempId = `temp-${Date.now()}`;
  const tempTask = {
    id: tempId,
    title,
    status: 'inbox',
    isNextAction: false
  };

  // Update UI immediately
  setTasks([...tasks, tempTask]);

  try {
    // Make API call
    const realTask = await api.post('/tasks', { title });

    // Replace temp task with real task
    setTasks(tasks.map(t => t.id === tempId ? realTask : t));
  } catch (error) {
    // Rollback on error
    setTasks(tasks.filter(t => t.id !== tempId));
    alert('Failed to create task');
  }
}
```

### 4. Loading States

```javascript
function useAPICall() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const call = async (endpoint) => {
    setLoading(true);
    setError(null);

    try {
      const result = await api.get(endpoint);
      setData(result);
    } catch (error) {
      setError(error);
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, call };
}

// Usage
const { data: tasks, loading, error, call: fetchTasks } = useAPICall();
```

### 5. Pagination Helper

```javascript
async function fetchAllPaginated(endpoint, limit = 100) {
  let allItems = [];
  let page = 1;
  let hasMore = true;

  while (hasMore) {
    const response = await api.get(`${endpoint}?page=${page}&limit=${limit}`);
    allItems = [...allItems, ...response.items];
    hasMore = page < response.pages;
    page++;
  }

  return allItems;
}

// Usage
const allTasks = await fetchAllPaginated('/tasks');
```

---

## Framework Examples

### React

```javascript
import { useState, useEffect } from 'react';

function TasksComponent() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const api = new TodoAPIClient();

  useEffect(() => {
    const fetchTasks = async () => {
      setLoading(true);
      try {
        const data = await api.get('/tasks');
        setTasks(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, []);

  const handleCreateTask = async (title) => {
    try {
      const newTask = await api.post('/tasks', { title });
      setTasks([...tasks, newTask]);
    } catch (err) {
      alert(err.message);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h1>Tasks</h1>
      <button onClick={() => handleCreateTask('New task')}>
        Add Task
      </button>
      <ul>
        {tasks.map(task => (
          <li key={task.id}>{task.title}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Vue.js

```javascript
<template>
  <div>
    <h1>Tasks</h1>
    <button @click="createTask">Add Task</button>
    <ul v-if="!loading">
      <li v-for="task in tasks" :key="task.id">
        {{ task.title }}
      </li>
    </ul>
    <div v-if="loading">Loading...</div>
    <div v-if="error">{{ error }}</div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const tasks = ref([]);
    const loading = ref(false);
    const error = ref(null);
    const api = new TodoAPIClient();

    onMounted(async () => {
      loading.value = true;
      try {
        tasks.value = await api.get('/tasks');
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    });

    const createTask = async () => {
      try {
        const newTask = await api.post('/tasks', { title: 'New task' });
        tasks.value.push(newTask);
      } catch (err) {
        alert(err.message);
      }
    };

    return { tasks, loading, error, createTask };
  }
};
</script>
```

### Angular

```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class TodoService {
  private baseURL = 'http://localhost:8000/api/v1';

  constructor(private http: HttpClient) {}

  getTasks(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseURL}/tasks`)
      .pipe(catchError(this.handleError));
  }

  createTask(task: any): Observable<any> {
    return this.http.post(`${this.baseURL}/tasks`, task)
      .pipe(catchError(this.handleError));
  }

  private handleError(error: any) {
    return throwError(() => error.error?.detail || 'Server error');
  }
}
```

---

## TypeScript Types

```typescript
// types/todo.ts

export interface Task {
  id: number;
  title: string;
  description?: string;
  status: 'inbox' | 'active' | 'completed' | 'waiting' | 'someday';
  priority: 'low' | 'medium' | 'high';
  project_id?: number;
  context_id?: number;
  tag_ids: number[];
  is_next_action: boolean;
  completed_at?: string;
  reminder_at?: string;
  created_at: string;
  updated_at: string;
}

export interface Tag {
  id: number;
  name: string;
  color?: string;
  created_at: string;
  updated_at: string;
}

export interface Context {
  id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface Area {
  id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface Project {
  id: number;
  name: string;
  description?: string;
  area_id?: number;
  status: 'active' | 'completed';
  progress: number;
  total_tasks: number;
  completed_tasks: number;
  created_at: string;
  updated_at: string;
}

export interface PaginationResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export interface TaskCreate {
  title: string;
  description?: string;
  status?: 'inbox' | 'active' | 'completed' | 'waiting' | 'someday';
  priority?: 'low' | 'medium' | 'high';
  project_id?: number;
  context_id?: number;
  tag_ids?: number[];
}

export interface TagCreate {
  name: string;
  color?: string;
}
```

---

## Testing

### Unit Tests

```javascript
import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('TodoAPIClient', () => {
  let api;
  let mockFetch;

  beforeEach(() => {
    mockFetch = vi.fn();
    global.fetch = mockFetch;
    api = new TodoAPIClient();
  });

  it('should create task', async () => {
    const mockTask = { id: 1, title: 'Test' };
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTask
    });

    const result = await api.post('/tasks', { title: 'Test' });

    expect(mockFetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ title: 'Test' })
      })
    );
    expect(result).toEqual(mockTask);
  });

  it('should handle errors', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: 'Not found' }),
      status: 404
    });

    await expect(api.get('/tasks/999')).rejects.toThrow('Not found');
  });
});
```

### Integration Tests

```javascript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';

describe('Todo API Integration', () => {
  const api = new TodoAPIClient('http://localhost:8000/api/v1');
  let createdTaskId;

  it('should create task', async () => {
    const task = await api.post('/tasks', {
      title: 'Integration test task'
    });

    expect(task).toHaveProperty('id');
    createdTaskId = task.id;
  });

  it('should get tasks', async () => {
    const tasks = await api.get('/tasks');

    expect(Array.isArray(tasks)).toBe(true);
    expect(tasks.length).toBeGreaterThan(0);
  });

  it('should complete task', async () => {
    const result = await api.post(`/tasks/${createdTaskId}/complete`);

    expect(result.status).toBe('completed');
  });
});
```

---

## Additional Resources

- [Developer Guide](DEVELOPER_GUIDE.md)
- [API Examples](API_EXAMPLES.md)
- [Schema Documentation](SCHEMA_DOCUMENTATION.md)
- [Troubleshooting](TROUBLESHOOTING.md)