# L0-04 — Создать файл .env.example

## Цель
Предоставить шаблон для переменных окружения.

## Вход
Config из L0-02.

## Выход
Файл .env.example.

## Готово когда
Файл содержит все поля конфигурации с примерами значений.

## Подсказка для LLM
Создайте .env.example с плейсхолдерами для: DATABASE_URL, REDIS_URL, CELERY_BROKER_URL, CELERY_RESULT_BACKEND, SECRET_KEY, API_HOST, API_PORT, LOG_LEVEL, REMINDER_CHECK_INTERVAL.

## Оценка усилия
S

## Файлы для создания
- .env.example

## Пример содержимого
```
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
