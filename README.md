# Todo API

REST API для управления задачами с поддержкой GTD методологии.

## Описание

Todo API — это мощный REST API для управления задачами, проектами и подзадачами с полной поддержкой GTD (Getting Things Done) методологии. API предоставляет гибкую систему для организации задач, проектов, контекстов и областей ответственности.

## Возможности

- **Управление задачами**: CRUD операции с поддержкой приоритетов, сроков выполнения и напоминаний
- **Проекты**: Организация задач в проекты с отслеживанием прогресса
- **GTD поддержка**:
  - Inbox для быстрого захвата задач
  - Next Actions для текущих задач
  - Contexts для ситуационных задач (@офис, @телефон)
  - Areas для областей ответственности (Работа, Здоровье)
  - Waiting For для делегированных задач
  - Someday/Maybe для отложенных задач
- **Подзадачи**: Иерархическая структура задач
- **Теги**: Гибкая система тегирования для дополнительной организации
- **Напоминания**: Периодические напоминания через Celery
- **Пагинация**: Эффективная работа с большими объёмами данных

## Tech Stack

- **Язык**: Python 3.11+
- **Фреймворк**: FastAPI 0.104+
- **База данных**: SQLite
- **ORM**: SQLAlchemy 2.0+
- **Валидация**: Pydantic 2.5+
- **Фоновые задачи**: Celery 5.3+ + Redis 5.0+

## Установка

### Клонирование репозитория

```bash
git clone https://github.com/yourusername/todowka.git
cd todowka
```

### Создание виртуального окружения

```bash
# С Python venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Или с pipenv
pipenv --python 3.11
pipenv shell

# Или с poetry
poetry install
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

## Настройка

### Переменные окружения

Скопируйте пример файла окружения:

```bash
cp .env.example .env
```

Отредактируйте `.env` при необходимости:

```env
DATABASE_URL=sqlite:///database.db
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
REMINDER_CHECK_INTERVAL=60
```

## Запуск

### Требования

- Python 3.11+
- Redis сервер

### Установка и запуск Redis

```bash
sudo dnf install redis
sudo systemctl enable redis
sudo systemctl start redis
```

### Запуск API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Запуск Celery Worker

```bash
celery -A app.services.reminders worker --loglevel=info
```

### Запуск Celery Beat (планировщик)

```bash
celery -A app.services.reminders beat --loglevel=info
```

### Все вместе (с tmux/screen)

Создайте файл `start.sh`:

```bash
#!/bin/bash

# Запуск в разных терминалах
redis-server &
sleep 2
celery -A app.services.reminders worker --loglevel=info &
celery -A app.services.reminders beat --loglevel=info &
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Сделайте исполняемым:

```bash
chmod +x start.sh
./start.sh
```

## API Документация

После запуска API доступна интерактивная документация:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Структура проекта

```
todowka/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI приложение
│   ├── config.py               # Конфигурация
│   ├── dependencies.py         # Dependency injection
│   ├── exceptions.py           # Кастомные исключения
│   ├── middleware/             # Middleware
│   ├── models/                 # SQLAlchemy модели
│   ├── schemas/               # Pydantic схемы
│   ├── repositories/           # Репозитории (DAL)
│   ├── services/               # Бизнес-логика
│   └── routes/                 # API routes
├── tests/
│   ├── unit/                   # Unit-тесты
│   └── integration/            # Integration-тесты
├── tasks/                      # Задачи для реализации
├── requirements.txt             # Зависимости
├── .env.example                # Пример окружения
└── README.md                   # Этот файл
```

## Использование API

### Создание задачи

```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Изучить FastAPI",
    "description": "Пройти базовый курс",
    "priority": "high",
    "status": "active"
  }'
```

### Создание задачи в Inbox

```bash
curl -X POST http://localhost:8000/api/v1/inbox \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Быстрая мысль"
  }'
```

### Получение задач

```bash
# Все задачи
curl http://localhost:8000/api/v1/tasks

# С фильтрами
curl "http://localhost:8000/api/v1/tasks?status=active&priority=high"

# Пагинация
curl "http://localhost:8000/api/v1/tasks?page=1&size=10"
```

### GTD Endpoints

```bash
# Inbox задачи
curl http://localhost:8000/api/v1/inbox

# Next Actions
curl http://localhost:8000/api/v1/next-actions

# Waiting задачи
curl http://localhost:8000/api/v1/waiting

# Someday задачи
curl http://localhost:8000/api/v1/someday
```

## Тестирование

### Запуск всех тестов

```bash
pytest tests/ -v
```

### Запуск unit-тестов

```bash
pytest tests/unit/ -v
```

### Запуск integration-тестов

```bash
pytest tests/integration/ -v
```

### С покрытием кода

```bash
pytest tests/ --cov=app --cov-report=html
```

## Линтер и форматирование

```bash
# Форматирование кода
black app/ tests/

# Линтер
ruff check app/ tests/

# Type checking
mypy app/
```

## Docker (опционально)

### Сборка образа

```bash
docker build -t todo-api .
```

### Запуск контейнера

```bash
docker run -p 8000:8000 todo-api
```

### Docker Compose

Создайте `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///database.db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery-worker:
    build: .
    command: celery -A app.services.reminders worker --loglevel=info
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - redis

  celery-beat:
    build: .
    command: celery -A app.services.reminders beat --loglevel=info
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - redis
```

Запуск:

```bash
docker-compose up -d
```

## Планируемые расширения

- [ ] Аутентификация (JWT/API Key)
- [ ] Многопользовательский режим
- [ ] Email-уведомления
- [ ] Webhook уведомления
- [ ] Встроенный календарь
- [ ] Mobile API
- [ ] WebSocket для real-time обновлений

## Лицензия

MIT License

## Связь

Для вопросов и предложений создавайте issue в репозитории.
