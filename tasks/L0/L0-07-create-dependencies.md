# L0-07 — Создать dependencies.py (get_db, get_services)

## Цель
Определить функции dependency injection для FastAPI.

## Вход
Config из L0-02.

## Выход
app/dependencies.py с get_db и функциями получения сервисов.

## Готово когда
get_db() возвращает сессию SQLAlchemy, get_task_service(), get_project_service(), get_subtask_service(), get_tag_service(), get_context_service(), get_area_service(), get_notification_service() определены.

## Подсказка для LLM
Создайте app/dependencies.py с функцией get_db() возвращающей сессию SQLAlchemy используя DATABASE_URL из config. Добавьте placeholder функции для get_task_service, get_project_service, get_subtask_service, get_tag_service, get_context_service, get_area_service, get_notification_service (они будут обновлены после создания сервисов).

## Оценка усилия
S

## Файлы для создания
- app/dependencies.py

## Зависимости
```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.config import Settings

def get_db() -> Session:
    # Возвращает сессию SQLAlchemy
    pass

def get_task_service(db: Session = Depends(get_db)):
    # Placeholder - будет обновлён в L2-41
    pass

def get_project_service(db: Session = Depends(get_db)):
    # Placeholder - будет обновлён в L2-37
    pass

# ... остальные placeholder функции
```

## Примечание
В этой задаче создайте только placeholder функции для сервисов. Полная реализация будет выполнена в задачах L2-34 через L2-41.
