# L1-17 — Создать инициализацию БД в main.py

## Цель
Добавить создание таблиц БД при запуске.

## Вход
Все модели созданы (L1-09 через L1-16).

## Выход
Обновлённый app/main.py с инициализацией БД.

## Готово когда
Base.metadata.create_all(bind=engine) вызывается при событии app startup.

## Подсказка для LLM
В app/main.py создайте engine SQLAlchemy из DATABASE_URL. Создайте sessionmaker. Добавьте обработчик @app.on_event("startup") который вызывает Base.metadata.create_all(bind=engine) для создания всех таблиц.

## Оценка усилия
S

## Файлы для изменения
- app/main.py

## Структура обновлений
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import Settings
from app.models.base import Base

# Настройка БД
settings = Settings()
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency для получения сессии БД
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Инициализация БД при старте приложения
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
```

## Примечание
Также обновите app/dependencies.py, заменив placeholder get_db() на импорт из main.py.
