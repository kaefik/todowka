# Руководство по выполнению для LLM

## System Prompt (установить один раз в начале работы)

```
Вы реализуете Todo REST API с поддержкой GTD методологии используя FastAPI, SQLAlchemy и Pydantic. Архитектура следует многоуровневому паттерну: Models → Schemas → Repositories → Services → Routes. Весь код должен следовать best practices Python и использовать type hints. База данных SQLite без миграций (используйте Base.metadata.create_all). MVP режим однопользовательский без аутентификации.
```

## Порядок выполнения

Выполняйте задачи в числовом порядке от L0-01 до L8-60. После каждой задачи:

1. **Проверьте что артефакт существует и соответствует условию "Готово когда"**
2. **Передайте расположение артефакта следующей задаче как "Вход"**
3. **Переименуйте файл задачи** добавив префикс `DONE-`

## Передача контекста между шагами

| Откуда | Куда | Что передаётся |
|--------|------|---------------|
| L0 | L1 | config.py, структура main.py |
| L1 (модели + схемы) | L2 | пути к файлам моделей и схем |
| L2 (сервисы) | L3 | пути к сервисам |
| L3 (routes) | L7 | зарегистрированные endpoints |
| Все слои | L8 | полная картина проекта |

## Советы для выполнения

### Для моделей (app/models/)
- Всегда импортируйте Base из `app.models.base`
- Используйте type hints для всех полей
- Для Enum создавайте классы в том же файле

### Для репозиториев (app/repositories/)
- Используйте Session из `sqlalchemy.orm`
- Возвращайте модели SQLAlchemy или None
- При ошибке бросайте соответствующие исключения

### Для сервисов (app/services/)
- Всегда бросайте `NotFoundException` из `app.exceptions` для отсутствующих ресурсов
- Используйте dependency injection через конструктор
- Возвращайте Pydantic схемы (Response)

### Для routes (app/routes/)
- Используйте dependency injection FastAPI для сервисов
- Всегда используйте `PaginationResponse[T]` для list endpoints
- Добавляйте docstrings для clarity
- Используйте соответствующие HTTP методы (GET, POST, PUT, PATCH, DELETE)

### Для GTD специфичных полей
- **is_next_action**: Boolean — помечает задачу как следующее действие
- **waiting_for**: String — описание от кого/чего ожидаем
- **delegated_to**: String — кому делегировали
- **someday**: Boolean — задача отложена "на когда-нибудь"
- **status**: Enum (inbox/active/someday/waiting/delegated)
- **priority**: Enum (low/medium/high)

## Команды для тестирования

После завершения задач 55-57:

```bash
# Unit-тесты
pytest tests/unit/ -v

# Integration-тесты
pytest tests/integration/ -v

# Все тесты
pytest tests/ -v

# С покрытием
pytest tests/ --cov=app --cov-report=html
```

## Запуск приложения

После завершения задач 51 и 54:

```bash
# Терминал 1 - API
uvicorn app.main:app --reload

# Терминал 2 - Redis
redis-server

# Терминал 3 - Celery worker
celery -A app.services.reminders worker --loglevel=info

# Терминал 4 - Celery beat (для периодических задач)
celery -A app.services.reminders beat --loglevel=info
```

## Документация API

После задачи 51:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Проверка качества кода

После завершения разработки:

```bash
# Линтер (если настроен)
ruff check app/

# Форматирование
black app/

# Type checking
mypy app/
```

## Обработка ошибок

### NotFoundException (404)
Используйте когда ресурс не найден:
```python
from app.exceptions import NotFoundException

task = task_repo.get(task_id)
if task is None:
    raise NotFoundException(f"Task with id {task_id} not found")
```

### ValidationErrorException (422)
Используйте для ошибок валидации данных:
```python
from app.exceptions import ValidationErrorException

if not data.title:
    raise ValidationErrorException("Title is required")
```

### ConflictException (409)
Используйте для конфликтов данных:
```python
from app.exceptions import ConflictException

existing_tag = tag_repo.get_by_name(name)
if existing_tag:
    raise ConflictException(f"Tag with name '{name}' already exists")
```

### ReminderException (500)
Используйте для ошибок отправки напоминаний:
```python
from app.exceptions import ReminderException

try:
    send_email(task)
except Exception as e:
    raise ReminderException(f"Failed to send reminder: {str(e)}")
```

## Форматирование ответа LLM

При выполнении задачи всегда предоставляйте:

1. **Краткое описание** — что было сделано
2. **Созданные/изменённые файлы** — список путей
3. **Проверка** — как проверить что задача выполнена ("Готово когда")

Пример:
```
Создана структура проекта с директориями и __init__.py файлами.

Файлы:
- app/__init__.py
- app/models/__init__.py
- app/schemas/__init__.py
- app/repositories/__init__.py
- app/services/__init__.py
- app/routes/__init__.py
- app/middleware/__init__.py
- app/auth/__init__.py
- tests/__init__.py
- tests/unit/__init__.py
- tests/integration/__init__.py

Проверка: Все директории и __init__.py файлы созданы.
```

## Важные замечания

1. **Не пропускайте задачи** — каждая задача зависит от предыдущих
2. **Следуйте "Подсказке для LLM"** — в ней содержатся конкретные инструкции
3. **Проверяйте "Готово когда"** — убедитесь что условие выполнено
4. **Используйте type hints** — улучшает читаемость и помогает IDE
5. **Тестируйте по ходу** — не ждите конца для проверки

## Частые проблемы

### SQLAlchemy Session
Всегда используйте dependency injection:
```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db

def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    # ...
```

### Pydantic Schemas
Разделяйте Create, Update и Response схемы:
- **Create**: только обязательные и опциональные поля для создания
- **Update**: все поля опциональные (for partial updates)
- **Response**: все поля включая computed fields

### Pagination
Используйте generic тип:
```python
from typing import TypeVar, List, Generic
from pydantic import BaseModel

T = TypeVar('T')

class PaginationResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
```

### DateTime
Используйте timezone-aware datetime:
```python
from datetime import datetime, timezone

created_at = datetime.now(timezone.utc)
```

## Успех! 🚀

Следуйте этому руководству, и вы успешно реализуете Todo API с поддержкой GTD методологии.
