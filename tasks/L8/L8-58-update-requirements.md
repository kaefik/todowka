# L8-58 — Обновить requirements.txt со всеми зависимостями

## Цель
Убедиться что requirements.txt включает все необходимые пакеты.

## Вход
requirements.txt (L0-3), конфигурация Celery (L5-54).

## Выход
Обновлённый requirements.txt с полным списком зависимостей.

## Готово когда
Файл включает FastAPI, SQLAlchemy, Pydantic, Pydantic-settings, Celery, Redis, Uvicorn, pytest, pytest-asyncio.

## Подсказка для LLM
Обновите requirements.txt с: fastapi>=0.104.0, uvicorn[standard]>=0.24.0, pydantic>=2.5.0, sqlalchemy>=2.0.0, pydantic-settings>=2.1.0, celery>=5.3.0, redis>=5.0.0, pytest>=7.4.0, pytest-asyncio>=0.21.0.

## Оценка усилия
S

## Файлы для изменения
- requirements.txt

## Полный список зависимостей
```
# FastAPI и веб-сервер
fastapi>=0.104.0
uvicorn[standard]>=0.24.0

# База данных и ORM
sqlalchemy>=2.0.0

# Валидация данных
pydantic>=2.5.0
pydantic-settings>=2.1.0

# Фоновые задачи
celery>=5.3.0
redis>=5.0.0

# Тестирование
pytest>=7.4.0
pytest-asyncio>=0.21.0

# Опционально: покрытие кода
pytest-cov>=4.1.0

# Опционально: форматирование и линтинг
black>=23.12.0
ruff>=0.1.0
mypy>=1.7.0
```

## Установка зависимостей

```bash
# Установка всех зависимостей
pip install -r requirements.txt

# Или с pipenv
pipenv install -r requirements.txt

# Или с poetry
poetry add $(cat requirements.txt)
```

## Разделение на production и development

Можно создать отдельные файлы:

requirements.txt:
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
celery>=5.3.0
redis>=5.0.0
```

requirements-dev.txt:
```
-r requirements.txt
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
black>=23.12.0
ruff>=0.1.0
mypy>=1.7.0
```

## Проверка установленных пакетов

```bash
# Список установленных пакетов
pip list

# Проверка устаревших пакетов
pip list --outdated

# Обновление пакетов
pip install --upgrade -r requirements.txt
```
