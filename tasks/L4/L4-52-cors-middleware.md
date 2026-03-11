# L4-52 — Добавить CORS middleware в main.py

## Цель
Включить CORS для клиентских приложений.

## Вход
main.py из L3-51.

## Выход
Обновлённый app/main.py с CORS middleware.

## Готово когда
CORSMiddleware добавлен разрешая все origins, methods, headers.

## Подсказка для LLM
В app/main.py добавьте CORSMiddleware из fastapi.middleware.cors. Добавьте middleware к app с allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"].

## Оценка усилия
S

## Файлы для изменения
- app/main.py

## Добавление CORS middleware
```python
from fastapi.middleware.cors import CORSMiddleware

# Добавьте после создания app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В production замените на список разрешённых origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Примечание
- Для production рекомендуется указать конкретные origins вместо ["*"]
- CORS необходим для фронтенд приложений (React, Vue, etc.)
- Разрешает все HTTP методы и заголовки
