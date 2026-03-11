# L1-28 — Создать репозиторий Context

## Цель
Определить ContextRepository расширяющий BaseRepository.

## Вход
Базовый репозиторий (L1-26), Context модель (L1-11).

## Выход
app/repositories/context.py.

## Готово когда
ContextRepository extends BaseRepository.

## Подсказка для LLM
Создайте app/repositories/context.py с классом ContextRepository наследующим BaseRepository. Дополнительные методы не нужны помимо базовых.

## Оценка усилия
S

## Файлы для создания
- app/repositories/context.py

## Класс ContextRepository
```python
from sqlalchemy.orm import Session
from app.models.context import Context
from app.repositories.base import BaseRepository

class ContextRepository(BaseRepository[Context]):
    def __init__(self, db: Session):
        super().__init__(db, Context)
```
