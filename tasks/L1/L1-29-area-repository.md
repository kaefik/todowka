# L1-29 — Создать репозиторий Area

## Цель
Определить AreaRepository расширяющий BaseRepository.

## Вход
Базовый репозиторий (L1-26), Area модель (L1-12).

## Выход
app/repositories/area.py.

## Готово когда
AreaRepository extends BaseRepository.

## Подсказка для LLM
Создайте app/repositories/area.py с классом AreaRepository наследующим BaseRepository. Дополнительные методы не нужны помимо базовых.

## Оценка усилия
S

## Файлы для создания
- app/repositories/area.py

## Класс AreaRepository
```python
from sqlalchemy.orm import Session
from app.models.area import Area
from app.repositories.base import BaseRepository

class AreaRepository(BaseRepository[Area]):
    def __init__(self, db: Session):
        super().__init__(db, Area)
```
