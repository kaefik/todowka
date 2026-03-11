# L0-06 — Создать error_handler middleware

## Цель
Создать унифицированный middleware обработки ошибок.

## Вход
Исключения из L0-05.

## Выход
app/middleware/error_handler.py.

## Готово когда
Обработчики исключений зарегистрированы в main.py возвращают JSON формат: {"error": "type", "message": "...", "details": {...}}.

## Подсказка для LLM
Создайте app/middleware/error_handler.py с обработчиками исключений для NotFoundException, ValidationErrorException, ConflictException, ReminderException и generic Exception. Возвращайте JSON с error type, message и details.

## Оценка усилия
S

## Файлы для создания
- app/middleware/error_handler.py

## Формат ответа
```json
{
  "error": "NotFoundException",
  "message": "Task with id 123 not found",
  "details": {
    "id": 123
  }
}
```

## Примечание
В этой задаче создайте только функцию error_handler. Регистрация в main.py будет выполнена в задаче L0-08.
