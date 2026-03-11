# L1-31 — Создать репозиторий Subtask

## Цель
Определить SubtaskRepository расширяющий BaseRepository.

## Вход
Базовый репозиторий (L1-26), Subtask модель (L1-14).

## Выход
app/repositories/subtask.py.

## Готово когда
SubtaskRepository extends BaseRepository с методом get_by_task.

## Подсказка для LLM
Создайте app/repositories/subtask.py с классом SubtaskRepository наследующим BaseRepository. Добавьте метод: get_by_task(self, task_id: int) возвращающий список Subtasks для данной задачи.

## Оценка усилия
S

## Файлы для создания
- app/repositories/subtask.py

## Класс SubtaskRepository
```python
from sqlalchemy.orm import Session
from app.models.subtask import Subtask
from app.repositories.base import BaseRepository

class SubtaskRepository(BaseRepository[Subtask]):
    def __init__(self, db: Session):
        super().__init__(db, Subtask)

    def get_by_task(self, task_id: int) -> list[Subtask]:
        return self.db.query(Subtask).filter(Subtask.task_id == task_id).all()
```
