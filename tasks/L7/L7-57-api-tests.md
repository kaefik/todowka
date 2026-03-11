# L7-57 — Создать integration-тесты для API endpoints

## Цель
Написать integration-тесты для всех API endpoints.

## Вход
Все routes зарегистрированы (L3-51).

## Выход
tests/integration/test_api.py с тестами API endpoints.

## Готово когда
Каждый endpoint протестирован с различными вводами и граничными случаями.

## Подсказка для LLM
Создайте tests/integration/test_api.py используя pytest с FastAPI TestClient. Используйте in-memory SQLite базу данных. Напишите тесты для каждой группы endpoints: tags (GET, POST, PUT, DELETE), contexts, areas, projects (включая complete и get_tasks), subtasks, notifications, inbox (GET, POST), tasks (GET с фильтрами, POST, PUT, PATCH, DELETE, next-action, complete, schedule-reminder). Тестируйте пагинацию, фильтрацию, error случаи (404, 422), и GTD-специфичную функциональность.

## Оценка усилия
L

## Файлы для создания
- tests/integration/test_api.py
- tests/integration/conftest.py (для fixtures)

## Структура тестов
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.main import app
from app.models.base import Base

# In-memory SQLite для тестов
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def client():
    """Создаёт TestClient для каждого теста"""
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    from app.dependencies import get_db
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)

# ===== Tags Endpoints Tests =====
def test_create_tag(client: TestClient):
    """Тест создания тега"""
    response = client.post(
        "/api/v1/tags",
        json={"name": "Work", "color": "#FF0000"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Work"
    assert data["color"] == "#FF0000"
    assert "id" in data

def test_get_all_tags(client: TestClient):
    """Тест получения всех тегов"""
    # Создаём теги
    client.post("/api/v1/tags", json={"name": "Work"})
    client.post("/api/v1/tags", json={"name": "Personal"})

    response = client.get("/api/v1/tags")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_tag_by_id(client: TestClient):
    """Тест получения тега по ID"""
    # Создаём тег
    create_response = client.post("/api/v1/tags", json={"name": "Work"})
    tag_id = create_response.json()["id"]

    # Получаем тег
    response = client.get(f"/api/v1/tags/{tag_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Work"

def test_get_tag_not_found(client: TestClient):
    """Тест получения несуществующего тега"""
    response = client.get("/api/v1/tags/999")
    assert response.status_code == 404

def test_update_tag(client: TestClient):
    """Тест обновления тега"""
    # Создаём тег
    create_response = client.post("/api/v1/tags", json={"name": "Work"})
    tag_id = create_response.json()["id"]

    # Обновляем тег
    response = client.put(
        f"/api/v1/tags/{tag_id}",
        json={"name": "Work Updated", "color": "#00FF00"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Work Updated"

def test_delete_tag(client: TestClient):
    """Тест удаления тега"""
    # Создаём тег
    create_response = client.post("/api/v1/tags", json={"name": "Work"})
    tag_id = create_response.json()["id"]

    # Удаляем тег
    response = client.delete(f"/api/v1/tags/{tag_id}")
    assert response.status_code == 204

# ===== Contexts Endpoints Tests =====
def test_create_context(client: TestClient):
    """Тест создания контекста"""
    response = client.post(
        "/api/v1/contexts",
        json={"name": "@Office", "icon": "🏢", "color": "#0000FF"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "@Office"

# ===== Areas Endpoints Tests =====
def test_create_area(client: TestClient):
    """Тест создания области"""
    response = client.post(
        "/api/v1/areas",
        json={"name": "Work", "description": "Professional life"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Work"

# ===== Projects Endpoints Tests =====
def test_create_project(client: TestClient):
    """Тест создания проекта"""
    response = client.post(
        "/api/v1/projects",
        json={"name": "New Project", "description": "Test project"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Project"
    assert data["progress"] == 0

def test_get_projects_with_pagination(client: TestClient):
    """Тест получения проектов с пагинацией"""
    # Создаём несколько проектов
    for i in range(15):
        client.post("/api/v1/projects", json={"name": f"Project {i}"})

    response = client.get("/api/v1/projects?page=1&size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 15
    assert len(data["items"]) == 10
    assert data["page"] == 1

def test_complete_project(client: TestClient):
    """Тест завершения проекта"""
    # Создаём проект и задачу
    project_response = client.post("/api/v1/projects", json={"name": "Test Project"})
    project_id = project_response.json()["id"]

    # Создаём задачу в проекте
    client.post(
        "/api/v1/tasks",
        json={
            "title": "Task 1",
            "project_id": project_id
        }
    )

    # Завершаем проект
    response = client.post(f"/api/v1/projects/{project_id}/complete")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

# ===== Tasks Endpoints Tests =====
def test_create_task(client: TestClient):
    """Тест создания задачи"""
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Test Task", "description": "Task description"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["completed"] is False

def test_create_task_with_tags(client: TestClient):
    """Тест создания задачи с тегами"""
    # Создаём теги
    tag1 = client.post("/api/v1/tags", json={"name": "Work"}).json()
    tag2 = client.post("/api/v1/tags", json={"name": "Urgent"}).json()

    # Создаём задачу с тегами
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Task with tags",
            "tag_ids": [tag1["id"], tag2["id"]]
        }
    )
    assert response.status_code == 201
    assert len(response.json()["tags"]) == 2

def test_get_tasks_with_filters(client: TestClient):
    """Тест получения задач с фильтрами"""
    # Создаём задачи с разными статусами
    client.post("/api/v1/tasks", json={"title": "Active Task", "status": "active"})
    client.post("/api/v1/tasks", json={"title": "Inbox Task", "status": "inbox"})

    # Фильтруем по статусу
    response = client.get("/api/v1/tasks?status=active")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Active Task"

def test_toggle_complete_task(client: TestClient):
    """Тест переключения завершения задачи"""
    # Создаём задачу
    create_response = client.post("/api/v1/tasks", json={"title": "Task"})
    task_id = create_response.json()["id"]

    # Переключаем завершение
    response = client.post(f"/api/v1/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True

def test_set_next_action(client: TestClient):
    """Тест установки флага следующего действия"""
    # Создаём задачу
    create_response = client.post("/api/v1/tasks", json={"title": "Task"})
    task_id = create_response.json()["id"]

    # Устанавливаем как next action
    response = client.post(
        f"/api/v1/tasks/{task_id}/next-action",
        json={"flag": True}
    )
    assert response.status_code == 200
    assert response.json()["is_next_action"] is True

def test_schedule_reminder(client: TestClient):
    """Тест планирования напоминания"""
    from datetime import datetime, timedelta

    # Создаём задачу
    create_response = client.post("/api/v1/tasks", json={"title": "Task"})
    task_id = create_response.json()["id"]

    # Планируем напоминание
    reminder_time = (datetime.now() + timedelta(days=1)).isoformat()
    response = client.post(
        f"/api/v1/tasks/{task_id}/schedule-reminder",
        json={"time": reminder_time}
    )
    assert response.status_code == 200
    assert "reminder_time" in response.json()

# ===== GTD Endpoints Tests =====
def test_create_inbox_task(client: TestClient):
    """Тест создания задачи в inbox"""
    response = client.post(
        "/api/v1/inbox",
        json={"title": "Quick thought"}
    )
    assert response.status_code == 201
    assert response.json()["status"] == "inbox"

def test_get_inbox_tasks(client: TestClient):
    """Тест получения inbox задач"""
    # Создаём задачи
    client.post("/api/v1/inbox", json={"title": "Inbox 1"})
    client.post("/api/v1/tasks", json={"title": "Active", "status": "active"})

    # Получаем только inbox задачи
    response = client.get("/api/v1/inbox")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["status"] == "inbox"

def test_get_next_actions(client: TestClient):
    """Тест получения next actions"""
    # Создаём задачи
    client.post("/api/v1/tasks", json={"title": "Normal", "is_next_action": False})
    client.post("/api/v1/tasks", json={"title": "Next Action", "is_next_action": True})

    # Получаем next actions
    response = client.get("/api/v1/next-actions")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["is_next_action"] is True

# ===== Health Endpoint Test =====
def test_health_check(client: TestClient):
    """Тест health check"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"
```

## Запуск тестов

```bash
# Запуск integration-тестов
pytest tests/integration/test_api.py -v

# С покрытием кода
pytest tests/integration/test_api.py --cov=app.routes --cov-report=html

# Все тесты
pytest tests/ -v

# С покрытием всего проекта
pytest tests/ --cov=app --cov-report=html
```

## Покрытие кода

```bash
# Генерация HTML отчёта о покрытии
pytest tests/ --cov=app --cov-report=html

# Открытие отчёта
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```
