# L0-02 — Создать config.py с pydantic-settings

## Цель
Определить конфигурацию приложения используя pydantic-settings.

## Вход
Структура проекта из L0-01.

## Выход
app/config.py с классом Settings.

## Готово когда
Класс Settings имеет поля: DATABASE_URL, REDIS_URL, CELERY_BROKER_URL, CELERY_RESULT_BACKEND, SECRET_KEY, API_HOST, API_PORT, LOG_LEVEL, REMINDER_CHECK_INTERVAL.

## Подсказка для LLM
Создайте app/config.py с классом Settings наследующим pydantic-settings.BaseSettings. Включите поля: DATABASE_URL (default="sqlite:///database.db"), REDIS_URL, CELERY_BROKER_URL, CELERY_RESULT_BACKEND, SECRET_KEY, API_HOST, API_PORT, LOG_LEVEL, REMINDER_CHECK_INTERVAL.

## Оценка усилия
S

## Файлы для создания
- app/config.py

## Поля конфигурации
```python
DATABASE_URL: str = "sqlite:///database.db"
REDIS_URL: str
CELERY_BROKER_URL: str
CELERY_RESULT_BACKEND: str
SECRET_KEY: str
API_HOST: str = "0.0.0.0"
API_PORT: int = 8000
LOG_LEVEL: str = "INFO"
REMINDER_CHECK_INTERVAL: int = 60
```
