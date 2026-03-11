# L1-09 — Создать базовую модель (app/models/base.py)

## Цель
Определить базовую SQLAlchemy модель с общими полями.

## Вход
Структура проекта из L0-01.

## Выход
app/models/base.py с классом Base и общими полями.

## Готово когда
Класс Base extends DeclarativeBase с полями id, created_at, updated_at.

## Подсказка для LLM
Создайте app/models/base.py с классом Base наследующим SQLAlchemy's DeclarativeBase. Добавьте Column поля: id (Integer, primary_key=True), created_at (DateTime, default=datetime.utcnow), updated_at (DateTime, default=datetime.utcnow, onupdate=datetime.utcnow).

## Оценка усилия
S

## Файлы для создания
- app/models/base.py

## Поля базовой модели
```python
from datetime import datetime
from sqlalchemy import Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    )
```

## Примечание
Все другие модели будут наследовать от Base и использовать TimestampMixin для общих полей.
