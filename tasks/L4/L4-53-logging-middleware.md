# L4-53 — Добавить middleware логирования запросов

## Цель
Добавить логирование запросов/ответов.

## Вход
main.py из L4-52.

## Выход
Request logging middleware добавлен.

## Готово когда
Каждый запрос логируется с method, path, status code, response time.

## Подсказка для LLM
Создайте app/middleware/logging.py с middleware функцией которая логирует method, path, headers запроса и status code и время ответа. В app/main.py добавьте этот middleware к app.

## Оценка усилия
S

## Файлы для создания
- app/middleware/logging.py

## Файлы для изменения
- app/main.py

## Создание logging middleware
```python
# app/middleware/logging.py
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """Логирует каждый запрос и ответ"""
        start_time = time.time()

        # Логируем входящий запрос
        logger.info(f"Request: {request.method} {request.url.path}")

        # Выполняем запрос
        response = await call_next(request)

        # Логируем ответ
        process_time = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} - "
            f"Time: {process_time:.3f}s - "
            f"{request.method} {request.url.path}"
        )

        return response
```

## Добавление middleware в main.py
```python
from app.middleware.logging import LoggingMiddleware

# Добавьте после CORS middleware
app.add_middleware(LoggingMiddleware)
```

## Пример вывода логов
```
2025-03-10 12:34:56 - app.middleware.logging - INFO - Request: GET /api/v1/tasks
2025-03-10 12:34:56 - app.middleware.logging - INFO - Response: 200 - Time: 0.123s - GET /api/v1/tasks
```

## Примечание
- Логи выводятся в stdout/stderr
- Для production можно настроить логирование в файл
- Включает время обработки каждого запроса
