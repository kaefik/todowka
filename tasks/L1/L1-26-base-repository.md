# L1-26 — Создать базовый репозиторий

## Цель
Определить generic базовый класс репозитория.

## Вход
Базовая модель (L1-09).

## Выход
app/repositories/base.py.

## Готово когда
BaseRepository с методами get, get_all, create, update, delete, exists.

## Подсказка для LLM
Создайте app/repositories/base.py с классом BaseRepository. Методы: __init__(self, db: Session), get(self, id: int), get_all(self, limit: int = 100, offset: int = 0), create(self, **kwargs), update(self, id: int, **kwargs), delete(self, id: int), exists(self, id: int) -> bool.

## Оценка усилия
S

## Файлы для создания
- app/repositories/base.py

## Класс BaseRepository
```python
from typing import Type, TypeVar, Generic, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model

    def get(self, id: int) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, limit: int = 100, offset: int = 0) -> list[ModelType]:
        return self.db.query(self.model).offset(offset).limit(limit).all()

    def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, id: int, **kwargs) -> Optional[ModelType]:
        instance = self.get(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.db.commit()
            self.db.refresh(instance)
        return instance

    def delete(self, id: int) -> bool:
        instance = self.get(id)
        if instance:
            self.db.delete(instance)
            self.db.commit()
            return True
        return False

    def exists(self, id: int) -> bool:
        return self.get(id) is not None

    def count(self) -> int:
        return self.db.query(self.model).count()
```
