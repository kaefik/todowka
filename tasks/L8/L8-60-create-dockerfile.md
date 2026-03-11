# L8-60 — Создать Dockerfile (опционально)

## Цель
Создать Dockerfile для контейнеризации.

## Вход
requirements.txt (L8-58).

## Выход
Dockerfile.

## Готово когда
Dockerfile может собирать и запускать FastAPI приложение.

## Подсказка для LLM
Создайте Dockerfile: FROM python:3.11-slim, WORKDIR /app, COPY requirements.txt ., RUN pip install -r requirements.txt, COPY . ., CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"].

## Оценка усилия
S

## Файлы для создания
- Dockerfile
- .dockerignore (опционально)

## Dockerfile

```dockerfile
# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Создаём директорию для базы данных
RUN mkdir -p /app/data

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=sqlite:////app/data/database.db

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## .dockerignore

```dockerignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Тесты и покрытие
.pytest_cache/
.coverage
htmlcov/
.tox/
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Git
.git/
.gitignore

# Задачи
tasks/

# Документация
docs/
*.md
!README.md

# Окружение
.env
.env.local

# OS
.DS_Store
Thumbs.db

# Docker
Dockerfile
.dockerignore
docker-compose.yml
```

## Сборка образа

```bash
# Сборка образа
docker build -t todo-api:latest .

# Или с указанием версии
docker build -t todo-api:1.0.0 .
```

## Запуск контейнера

```bash
# Простая команда
docker run -p 8000:8000 todo-api:latest

# С монтированием volume для базы данных
docker run -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  todo-api:latest

# С переменными окружения
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:////app/data/database.db \
  -e REDIS_URL=redis://host.docker.internal:6379/0 \
  todo-api:latest
```

## Docker Compose

### docker-compose.yml

```yaml
version: '3.8'

services:
  # API сервис
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: todo-api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:////app/data/database.db
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    volumes:
      - ./data:/app/data
    depends_on:
      - redis
    restart: unless-stopped

  # Redis сервис
  redis:
    image: redis:7-alpine
    container_name: todo-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    restart: unless-stopped

  # Celery Worker
  celery-worker:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: todo-celery-worker
    command: celery -A app.services.reminders worker --loglevel=info
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    volumes:
      - ./data:/app/data
    depends_on:
      - redis
    restart: unless-stopped

  # Celery Beat
  celery-beat:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: todo-celery-beat
    command: celery -A app.services.reminders beat --loglevel=info
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - redis
    restart: unless-stopped

volumes:
  redis-data:

networks:
  default:
    name: todo-network
```

### Запуск с Docker Compose

```bash
# Сборка и запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка всех сервисов
docker-compose down

# Полная очистка (включая volumes)
docker-compose down -v

# Перезапуск конкретного сервиса
docker-compose restart api
```

## Production Dockerfile

### dockerfile.prod

```dockerfile
# Многоступенчатая сборка для оптимизации размера образа
FROM python:3.11-slim as builder

WORKDIR /app

# Устанавливаем зависимости для сборки
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Финальный образ
FROM python:3.11-slim

WORKDIR /app

# Копируем установленные зависимости из builder
COPY --from=builder /root/.local /root/.local

# Убедимся что скрипты в PATH
ENV PATH=/root/.local/bin:$PATH

# Копируем код приложения
COPY . .

# Создаём директорию для базы данных
RUN mkdir -p /app/data

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=sqlite:////app/data/database.db
ENV LOG_LEVEL=WARNING

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Использование production Dockerfile

```bash
# Сборка production образа
docker build -f dockerfile.prod -t todo-api:prod .

# Запуск
docker run -p 8000:8000 \
  -e LOG_LEVEL=WARNING \
  todo-api:prod
```

## Проверка работоспособности

```bash
# Проверка health endpoint
curl http://localhost:8000/api/v1/health

# Ожидаемый ответ
# {"status": "ok", "database": "connected"}

# Проверка создания задачи
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task from Docker"}'
```

## Оптимизация размера образа

### Анализ размера

```bash
# Просмотр размера всех images
docker images

# Просмотр размеров слоёв
docker history todo-api:latest
```

### Оптимизации

1. Используйте `.dockerignore` для исключения ненужных файлов
2. Используйте многоступенчатую сборку (multi-stage build)
3. Объединяйте команды RUN с `&&`
4. Очищайте кэш после установки пакетов
5. Используйте официальные образы с суффиксом `-slim`

## Развертывание

### Push в Docker Hub

```bash
# Вход в Docker Hub
docker login

# Тегирование
docker tag todo-api:latest yourusername/todo-api:1.0.0

# Push
docker push yourusername/todo-api:1.0.0
```

### Pull и запуск на сервере

```bash
# Pull образа
docker pull yourusername/todo-api:1.0.0

# Запуск
docker run -d -p 8000:8000 \
  -e REDIS_URL=redis://redis-server:6379/0 \
  yourusername/todo-api:1.0.0
```
```

## Полезные команды Docker

```bash
# Просмотр запущенных контейнеров
docker ps

# Просмотр всех контейнеров (включая остановленные)
docker ps -a

# Просмотр логов контейнера
docker logs -f todo-api

# Вход в контейнер
docker exec -it todo-api /bin/bash

# Остановка контейнера
docker stop todo-api

# Удаление контейнера
docker rm todo-api

# Удаление образа
docker rmi todo-api:latest

# Очистка неиспользуемых ресурсов
docker system prune -a
```
