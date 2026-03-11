# L0-05 — Создать exceptions.py с кастомными исключениями

## Цель
Определить кастомные API исключения.

## Вход
Структура проекта из L0-01.

## Выход
app/exceptions.py с NotFoundException, ValidationErrorException, ConflictException, ReminderException.

## Готово когда
Все классы исключений определены с соответствующими HTTP статус кодами (404, 422, 409, 500).

## Подсказка для LLM
Создайте app/exceptions.py с классами исключений наследующими HTTPException: NotFoundException (404), ValidationErrorException (422), ConflictException (409), ReminderException (500).

## Оценка усилия
S

## Файлы для создания
- app/exceptions.py

## Классы исключений
```python
from fastapi import HTTPException

class NotFoundException(HTTPException):
    status_code = 404

class ValidationErrorException(HTTPException):
    status_code = 422

class ConflictException(HTTPException):
    status_code = 409

class ReminderException(HTTPException):
    status_code = 500
```
