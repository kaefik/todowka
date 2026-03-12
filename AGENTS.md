# AGENTS.md

Этот файл содержит инструкции для AI агентов по работе с проектом Todo API.

## Описание проекта

Todo API — это REST API для управления задачами с полной поддержкой GTD (Getting Things Done) методологии. API построен на FastAPI с использованием SQLAlchemy ORM и поддерживает управление задачами, проектами, подзадачами, тегами, контекстами и областями ответственности.

## Технологический стек

- **Язык**: Python 3.11+
- **Фреймворк**: FastAPI 0.104+
- **База данных**: SQLite
- **ORM**: SQLAlchemy 2.0+
- **Валидация**: Pydantic 2.5+
- **Фоновые задачи**: Celery 5.3+ + Redis 5.0+
- **Тестирование**: pytest 7.4+

## Структура проекта

```
todowka/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI приложение
│   ├── config.py               # Конфигурация
│   ├── dependencies.py         # Dependency injection
│   ├── exceptions.py           # Кастомные исключения
│   ├── middleware/             # Middleware (CORS, logging)
│   ├── models/                 # SQLAlchemy модели
│   ├── schemas/               # Pydantic схемы
│   ├── repositories/           # Репозитории (DAL)
│   ├── services/               # Бизнес-логика
│   └── routes/                 # API routes
├── tests/
│   ├── unit/                   # Unit-тесты
│   └── integration/            # Integration-тесты
├── tasks/                      # Задачи для реализации (L0-L8)
├── requirements.txt             # Зависимости
└── .env.example                # Пример окружения
```

## Установка и запуск

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Настройка окружения

```bash
cp .env.example .env
```

Редактируйте `.env` при необходимости:
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

### Запуск Redis

```bash
redis-server
```

### Запуск API

```bash
uvicorn app.main:app --reload
```

### Запуск Celery Worker

```bash
celery -A app.services.reminders worker --loglevel=info
```

### Запуск Celery Beat

```bash
celery -A app.services.reminders beat --loglevel=info
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

После внесения изменений в код **ОБЯЗАТЕЛЬНО** запустите следующие команды:

### Форматирование кода

```bash
black app/ tests/
```

### Линтер

```bash
ruff check app/ tests/
```

### Type checking

```bash
mypy app/
```

## Архитектурные слои

Проект следует принципу разделения ответственности:

1. **Routes** (`app/routes/`) - API endpoints, принимают HTTP запросы
2. **Services** (`app/services/`) - Бизнес-логика, валидация, координация репозиториев
3. **Repositories** (`app/repositories/`) - Доступ к данным, работа с БД через SQLAlchemy
4. **Schemas** (`app/schemas/`) - Pydantic модели для валидации и сериализации
5. **Models** (`app/models/`) - SQLAlchemy модели БД

## Конвенции кода

- Используйте type hints во всех функциях и методах
- Следуйте PEP 8 (black автоматически форматирует код)
- Не добавляйте комментарии если не требуется
- Используйте f-strings для форматирования строк
- Следуйте существующему паттерну именования файлов и классов

## Задачи для реализации

В папке `tasks/` находятся задачи, организованные по слоям (L0-L8):

- **L0** - Базовая инфраструктура проекта
- **L1** - Модели, схемы и репозитории
- **L2** - Сервисы бизнес-логики
- **L3** - API routes
- **L4** - Middleware (CORS, logging)
- **L5** - Фоновые задачи (Celery)
- **L6** - Документация и примеры
- **L7** - Тестирование
- **L8** - DevOps и инфраструктура

Каждая задача описана в отдельном `.md` файле.

## API Documentation

После запуска API доступна интерактивная документация:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Пример работы с проектом

При добавлении новой функции:

1. Создайте/обновите модель в `app/models/`
2. Создайте схему в `app/schemas/`
3. Создайте/обновите репозиторий в `app/repositories/`
4. Создайте/обновите сервис в `app/services/`
5. Создайте/обновите route в `app/routes/`
6. Зарегистрируйте route в `app/main.py`
7. Добавьте тесты в `tests/unit/` или `tests/integration/`
8. Запустите линтер и форматирование
9. Запустите тесты
