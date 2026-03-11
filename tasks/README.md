# План реализации Todo API

## Общая информация

- **Всего задач**: 60
- **Расчётное усилие**: ~50-60 часов
- **Статус задач**:
  - 📝 TODO — задача не начата
  - ✅ DONE — задача выполнена

## Сводная таблица

| # | Слой | Задача | Усилие | Статус |
|---|------|-------|--------|--------|
| 1 | Foundation | Создать структуру проекта и базовые файлы | S | 📝 TODO |
| 2 | Foundation | Создать config.py с pydantic-settings | S | 📝 TODO |
| 3 | Foundation | Создать requirements.txt с зависимостями | S | 📝 TODO |
| 4 | Foundation | Создать файл .env.example | S | 📝 TODO |
| 5 | Foundation | Создать exceptions.py с кастомными исключениями | S | 📝 TODO |
| 6 | Foundation | Создать middleware error_handler | S | 📝 TODO |
| 7 | Foundation | Создать dependencies.py (get_db, get_services) | S | 📝 TODO |
| 8 | Foundation | Создать main.py с настройкой FastAPI | S | 📝 TODO |
| 9 | Data Layer | Создать базовую модель (app/models/base.py) | S | 📝 TODO |
| 10 | Data Layer | Создать модель Tag | S | 📝 TODO |
| 11 | Data Layer | Создать модель Context | S | 📝 TODO |
| 12 | Data Layer | Создать модель Area | S | 📝 TODO |
| 13 | Data Layer | Создать модель Project | S | 📝 TODO |
| 14 | Data Layer | Создать модель Subtask | S | 📝 TODO |
| 15 | Data Layer | Создать модель Task с m2m к Tag | M | 📝 TODO |
| 16 | Data Layer | Создать модель Notification | S | 📝 TODO |
| 17 | Data Layer | Создать инициализацию БД в main.py | S | 📝 TODO |
| 18 | Data Layer | Создать схему пагинации (schemas/pagination.py) | S | 📝 TODO |
| 19 | Data Layer | Создать схемы Tag (Create, Response) | S | 📝 TODO |
| 20 | Data Layer | Создать схемы Context | S | 📝 TODO |
| 21 | Data Layer | Создать схемы Area | S | 📝 TODO |
| 22 | Data Layer | Создать схемы Project | S | 📝 TODO |
| 23 | Data Layer | Создать схемы Subtask | S | 📝 TODO |
| 24 | Data Layer | Создать схемы Notification | S | 📝 TODO |
| 25 | Data Layer | Создать схемы Task (Create, Update, Response) | M | 📝 TODO |
| 26 | Data Layer | Создать базовый репозиторий | S | 📝 TODO |
| 27 | Data Layer | Создать репозиторий Tag | S | 📝 TODO |
| 28 | Data Layer | Создать репозиторий Context | S | 📝 TODO |
| 29 | Data Layer | Создать репозиторий Area | S | 📝 TODO |
| 30 | Data Layer | Создать репозиторий Project | S | 📝 TODO |
| 31 | Data Layer | Создать репозиторий Subtask | S | 📝 TODO |
| 32 | Data Layer | Создать репозиторий Notification | S | 📝 TODO |
| 33 | Data Layer | Создать репозиторий Task с фильтрами | M | 📝 TODO |
| 34 | Core Business | Создать TagService (CRUD) | S | 📝 TODO |
| 35 | Core Business | Создать ContextService (CRUD) | S | 📝 TODO |
| 36 | Core Business | Создать AreaService (CRUD) | S | 📝 TODO |
| 37 | Core Business | Создать ProjectService (CRUD + complete) | M | 📝 TODO |
| 38 | Core Business | Создать SubtaskService (CRUD) | S | 📝 TODO |
| 39 | Core Business | Создать NotificationService | S | 📝 TODO |
| 40 | Core Business | Создать RemindersService (Celery) | L | 📝 TODO |
| 41 | Core Business | Создать TaskService (CRUD + операции GTD) | L | 📝 TODO |
| 42 | API/Interface | Создать health endpoint | S | 📝 TODO |
| 43 | API/Interface | Создать routes для tags (CRUD + задачи по тегу) | M | 📝 TODO |
| 44 | API/Interface | Создать routes для contexts (CRUD + задачи по контексту) | M | 📝 TODO |
| 45 | API/Interface | Создать routes для areas (CRUD + задачи по области) | M | 📝 TODO |
| 46 | API/Interface | Создать routes для projects (CRUD + complete + задачи проекта) | M | 📝 TODO |
| 47 | API/Interface | Создать routes для subtasks (CRUD вложенные под задачу) | M | 📝 TODO |
| 48 | API/Interface | Создать routes для notifications (GET список, GET по id) | S | 📝 TODO |
| 49 | API/Interface | Создать GTD routes (inbox, next-actions, waiting, someday) | M | 📝 TODO |
| 50 | API/Interface | Создать routes для tasks (CRUD + next-action + complete + schedule-reminder) | L | 📝 TODO |
| 51 | API/Interface | Зарегистрировать все routes в main.py с APIRouter | S | 📝 TODO |
| 52 | Validation & Errors | Добавить CORS middleware в main.py | S | 📝 TODO |
| 53 | Validation & Errors | Добавить middleware логирования запросов | S | 📝 TODO |
| 54 | Integration | Настроить Celery в app/services/reminders.py | M | 📝 TODO |
| 55 | Tests | Создать unit-тесты для репозиториев | L | 📝 TODO |
| 56 | Tests | Создать unit-тесты для сервисов | L | 📝 TODO |
| 57 | Tests | Создать integration-тесты для API endpoints | L | 📝 TODO |
| 58 | Docs | Обновить requirements.txt со всеми зависимостями | S | 📝 TODO |
| 59 | Docs | Создать README.md с инструкциями по запуску | M | 📝 TODO |
| 60 | Docs | Создать Dockerfile (опционально) | S | 📝 TODO |

## Как пользоваться

1. **Начните с 00-guide.md** — прочитайте руководство по выполнению
2. **Выполняйте задачи по порядку** — от L0-01 до L8-60
3. **После выполнения задачи** — переименуйте файл:
   - `L0-01-create-structure.md` → `DONE-L0-01-create-structure.md`
4. **Обновляйте README.md** — меняйте статус 📝 TODO на ✅ DONE

## Структура слоёв

### L0: Foundation (Основы)
- Настройка проекта, конфигурации, зависимостей
- Базовая инфраструктура приложения

### L1: Data Layer (Слой данных)
- SQLAlchemy модели
- Pydantic схемы
- Репозитории

### L2: Core Business (Бизнес-логика)
- Сервисы с бизнес-логикой
- Celery для фоновых задач

### L3: API/Interface (Интерфейс)
- FastAPI routes
- API endpoints

### L4: Validation & Errors (Валидация и ошибки)
- Middleware для CORS и логирования

### L5: Integration (Интеграции)
- Внешние сервисы (Celery, Redis)

### L7: Tests (Тесты)
- Unit-тесты для репозиториев и сервисов
- Integration-тесты для API

### L8: Docs (Документация)
- README, Dockerfile, финальные настройки

## Легенда усилий

- **XS** — ~30 минут
- **S** — ~1 час
- **M** — ~2 часа
- **L** — ~4 часа
