# L1-27 — Создать репозиторий Tag

## Цель
Определить TagRepository расширяющий BaseRepository.

## Вход
Базовый репозиторий (L1-26), Tag модель (L1-10).

## Выход
app/repositories/tag.py.

## Готово когда
TagRepository extends BaseRepository с методами get_by_name и get_or_create.

## Подсказка для LLM
Создайте app/repositories/tag.py с классом TagRepository наследующим BaseRepository. Добавьте методы: get_by_name(self, name: str) возвращающий Tag или None, get_or_create(self, name: str, color: Optional[str] = None) возвращающий Tag.

## Оценка усилия
S

## Файлы для создания
- app/repositories/tag.py

## Класс TagRepository
```python
from typing import Optional
from sqlalchemy.orm import Session
from app.models.tag import Tag
from app.repositories.base import BaseRepository

class TagRepository(BaseRepository[Tag]):
    def __init__(self, db: Session):
        super().__init__(db, Tag)

    def get_by_name(self, name: str) -> Optional[Tag]:
        return self.db.query(Tag).filter(Tag.name == name).first()

    def get_or_create(self, name: str, color: Optional[str] = None) -> Tag:
        tag = self.get_by_name(name)
        if not tag:
            tag = self.create(name=name, color=color)
        return tag
```
