# Todo API Documentation Index

Добро пожаловать в документацию Todo API!

## 🚀 Quick Start

1. **Прочитайте [README.md](README.md)** - краткое введение в API
2. **Посмотрите [API Examples](API_EXAMPLES.md)** - примеры запросов и ответов
3. **Запустите `./test_api.sh`** - для быстрого тестирования

## 📚 Полная документация

### Для всех
- **[README.md](README.md)** - Краткое введение в Todo API и ключевые endpoints

### Для разработчиков
- **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** - Полное руководство разработчика
  - Аутентификация и заголовки
  - Общие паттерны
  - GTD методология
  - Обработка ошибок
  - Лучшие практики

- **[API_EXAMPLES.md](API_EXAMPLES.md)** - Примеры запросов и ответов
  - Все endpoints с примерами
  - curl команды
  - JavaScript (fetch) примеры
  - Полный GTD workflow

- **[SCHEMA_DOCUMENTATION.md](SCHEMA_DOCUMENTATION.md)** - Схемы данных
  - Все сущности (Tag, Context, Area, Project, Task, Subtask, Notification)
  - Поля и валидация
  - Enum значения
  - Отношения между сущностями

### Для фронтенд-разработчиков
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Руководство по интеграции
  - Настройка API клиента
  - Common Operations для всех endpoints
  - Обработка ошибок
  - Real-time обновления
  - Примеры для React, Vue.js, Angular
  - TypeScript типы
  - Тестирование

### Для AI и LLM
- **[LLM_INSTRUCTIONS.md](LLM_INSTRUCTIONS.md)** - Инструкции для Claude, GPT-4 и других
  - Контекст и конфигурация
  - Важные замечания
  - Детали сущностей
  - GTD workflow
  - Шаблоны кода
  - Примеры промптов

### Для решения проблем
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Решение проблем
  - Проблемы с подключением
  - API ошибки
  - Проблемы с данными
  - Производительность
  - Вопросы разработки
  - Советы по отладке

### Техническая документация
- **[openapi.json](openapi.json)** - OpenAPI спецификация
  - Полное описание API в машинночитаемом формате
  - Используется для генерации документации
  - Можно импортировать в Postman/Insomnia

## 🎯 С чего начать?

### Я новичок в проекте
1. [README.md](README.md)
2. [API_EXAMPLES.md](API_EXAMPLES.md)
3. Запустите `./test_api.sh`

### Я фронтенд-разработчик
1. [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
2. [SCHEMA_DOCUMENTATION.md](SCHEMA_DOCUMENTATION.md)
3. [API_EXAMPLES.md](API_EXAMPLES.md)

### Я бэкенд-разработчик
1. [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
2. [SCHEMA_DOCUMENTATION.md](SCHEMA_DOCUMENTATION.md)
3. [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Я работаю с AI/LLM
1. [LLM_INSTRUCTIONS.md](LLM_INSTRUCTIONS.md)
2. [openapi.json](openapi.json)
3. [API_EXAMPLES.md](API_EXAMPLES.md)

### У меня проблемы
1. [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Проверьте здоровье API: `curl http://localhost:8000/api/v1/health`
3. Посмотрите интерактивную документацию: http://localhost:8000/docs

## 🌐 Интерактивная документация

Откройте в браузере:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Интерактивная документация позволяет:
- Просматривать все endpoints
- Пробовать запросы прямо в браузере
- Видеть схемы данных
- Получать примеры запросов

## 🛠️ Полезные инструменты

### Быстрый тест
```bash
./test_api.sh
```

### Health check
```bash
curl http://localhost:8000/api/v1/health
```

### Создать тег
```bash
curl -X POST http://localhost:8000/api/v1/tags \
  -H "Content-Type: application/json" \
  -d '{"name": "Work", "color": "#FF0000"}'
```

### Получить задачи
```bash
curl http://localhost:8000/api/v1/tasks
```

## 📋 GTD Methodology

Todo API реализует GTD (Getting Things Done) методологию:

1. **Capture** - захват задач в Inbox (`POST /api/v1/inbox`)
2. **Clarify** - уточнение деталей (`PUT /api/v1/tasks/{id}`)
3. **Organize** - организация с проектами, контекстами, тегами
4. **Engage** - выполнение (Next Actions)
5. **Review** - обзор задач по статусам

Подробнее: [GTD Workflow в DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md#gtd-methodology-implementation)

## 🔗 Связанные ресурсы

- **Репозиторий**: [GitHub]
- **Проблемы**: [GitHub Issues]
- **Автор**: [Ваше имя]

## 📝 Участие в разработке

Хотите внести вклад? Пожалуйста:
1. Прочтите документацию
2. Ознакомьтесь с GTD методологией
3. Создайте issue для обсуждения
4. Сделайте pull request

## 📞 Поддержка

Если у вас есть вопросы:
1. Проверьте [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Посмотрите интерактивную документацию: http://localhost:8000/docs
3. Запустите тестовый скрипт: `./test_api.sh`
4. Создайте issue в репозитории

---

**Удачи с Todo API! 🎉**