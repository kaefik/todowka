# L3-42 — Создать health endpoint

## Цель
Добавить health check endpoint в main.py.

## Вход
main.py из L0-08.

## Выход
Обновлённый app/main.py с GET /api/v1/health.

## Готово когда
Health endpoint возвращает {"status": "ok", "database": "connected"}.

## Подсказка для LLM
В app/main.py обновите health endpoint для проверки подключения к БД: попробуйте выполнить "SELECT 1" и верните {"status": "ok", "database": "connected"} или ошибку при неудаче.

## Оценка усилия
S

## Файлы для изменения
- app/main.py

## Обновление health endpoint
```python
@app.get("/api/v1/health")
def health_check():
    """Проверка здоровья API и подключения к БД"""
    try:
        # Проверка подключения к БД
        from app.main import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "error": str(e)}
```

## Примечание
Этот endpoint используется для мониторинга健康状况 сервиса.
