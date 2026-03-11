# Автоматический Исполнитель Задач Todo API

Этот скрипт автоматически выполняет задачи из директории `tasks/` используя LLM API (OpenAI, Anthropic, Ollama и др.).

## Возможности

✅ **Автоматическое выполнение** всех задач по порядку  
✅ **Поддержка разных LLM**: OpenAI, Anthropic, z.ai, Ollama, кастомные API  
✅ **Интерактивный режим** с подтверждением каждой задачи  
✅ **Автоматический режим** — выполняет задачи без остановки  
✅ **Логирование** результатов выполнения каждой задачи  
✅ **Контекст истории** — передаёт информацию о выполненных задачах  
✅ **Возможность пропустить/повторить** задачи  

## Установка

### 1. Клонируйте репозиторий

```bash
cd todowka
```

### 2. Создайте виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Установите зависимости

```bash
pip install openai anthropic ollama python-dotenv
```

**Или только нужные:**
```bash
# Для OpenAI
pip install openai python-dotenv

# Для Anthropic
pip install anthropic python-dotenv

# Для Ollama
pip install ollama python-dotenv
```

## Конфигурация

### 1. Скопируйте файл настроек

```bash
cp .env.executor.example .env
```

### 2. Настройте провайдера LLM

#### OpenAI (рекомендуется)

Откройте `.env` и настройте:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4
```

**Как получить API ключ:**
1. Зайдите на https://platform.openai.com/api-keys
2. Создайте новый API ключ
3. Скопируйте и вставьте в `.env`

#### z.ai (GLM-4.7)

```env
LLM_PROVIDER=zai
ZAI_API_KEY=your-zai-api-key-here
ZAI_BASE_URL=https://api.z.ai/api/coding/paas/v4
ZAI_MODEL=glm-4.7
```

**Модель GLM-4.7 от z.ai**
- Высокая производительность для кодогенерации
- Оптимизирован для задач программирования
- OpenAI-совместимый API
- Поддерживает большой контекст

#### Ollama (бесплатно, локально)

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

**Установка Ollama:**
```bash
# Mac
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Скачайте с https://ollama.com/download

# Загрузите модель
ollama pull llama3
```

#### Кастомный API

```env
LLM_PROVIDER=custom
CUSTOM_API_KEY=your-custom-api-key
CUSTOM_BASE_URL=https://your-custom-api.com/v1
CUSTOM_MODEL=your-custom-model
```

### 3. Настройки выполнения

```env
# Автоматически продолжать без подтверждения (true/false)
AUTO_CONTINUE=false

# Сколько предыдущих задач включать в контекст (0-10)
MAX_CONTEXT_TASKS=3

# Позволить LLM выполнять bash команды (true/false)
# ⚠️  Опасно! Только для доверенных LLM!
USE_BASH_TOOLS=false
```

## Использование

### Базовый запуск

```bash
python auto_executor.py
```

### С переменными окружения

```bash
# OpenAI
LLM_PROVIDER=openai OPENAI_API_KEY=sk-... python auto_executor.py

# Ollama
LLM_PROVIDER=ollama python auto_executor.py

# Anthropic
LLM_PROVIDER=anthropic ANTHROPIC_API_KEY=sk-ant-... python auto_executor.py
```

### Режимы работы

#### Интерактивный режим (по умолчанию)

```bash
python auto_executor.py
```

Скрипт будет спрашивать подтверждение после каждой задачи:
```
📝 [1/60] Выполняем: L0/L0-01-create-structure.md
------------------------------------------------------------
   Цель: Инициализировать FastAPI проект с директориями и __init__.py файлами.
   Усилие: S

🤔 Обращаемся к LLM...
📤 Ответ LLM:
[ответ LLM...]

💾 Лог сохранён: tasks/logs/L0-01-create-structure.md.log

============================================================
МЕНЮ УПРАВЛЕНИЯ
============================================================
  y - Задача выполнена, переходи к следующей
  n - Задача не выполнена, повторим
  s - Пропустить задачу
  u - Снять отметку выполненной/пропущенной
  a - Продолжить автоматически (не спрашивать)
  q - Выйти
============================================================
Задача выполнена успешно? (y/n/s/u/a/q): 
```

#### Автоматический режим

В `.env`:
```env
AUTO_CONTINUE=true
```

Или во время работы выберите `a` для автоматического режима.

Скрипт будет выполнять задачи без остановки:
```
📝 [1/60] Выполняем: L0/L0-01-create-structure.md
...
✅ Автоматически отмечаем как выполненную

📝 [2/60] Выполняем: L0/L0-02-create-config.md
...
✅ Автоматически отмечаем как выполненную
```

## Управление задачами

### Просмотр статуса задач

```bash
# Все задачи
ls tasks/L0/
ls tasks/L1/
# и т.д.

# Выполненные задачи
ls tasks/L0/DONE-*.md
ls tasks/*/DONE-*.md

# Пропущенные задачи
ls tasks/*/SKIP-*.md
```

### Сброс состояния

#### Сбросить одну задачу

```bash
# Из выполненной в обычную
mv tasks/L0/DONE-L0-01-create-structure.md tasks/L0/L0-01-create-structure.md

# Из пропущенной в обычную
mv tasks/L0/SKIP-L0-01-create-structure.md tasks/L0/L0-01-create-structure.md
```

#### Сбросить все задачи

```bash
# Сбросить все DONE- задачи
for file in tasks/*/DONE-*.md; do
  newname=$(echo $file | sed 's/DONE-//')
  mv "$file" "$newname"
done

# Сбросить все SKIP-задачи
for file in tasks/*/SKIP-*.md; do
  newname=$(echo $file | sed 's/SKIP-//')
  mv "$file" "$newname"
done
```

### Просмотр логов

```bash
# Лог конкретной задачи
cat tasks/logs/L0-01-create-structure.md.log

# Все логи
ls tasks/logs/

# Итоговый лог
cat tasks/logs/SUMMARY.log
```

## Команды меню

| Команда | Описание |
|---------|----------|
| **y** | Задача выполнена, отмечаем как DONE и переходим к следующей |
| **n** | Задача не выполнена, повторим |
| **s** | Пропустить задачу (отмечаем как SKIP) |
| **u** | Снять отметку (DONE → обычная, SKIP → обычная) |
| **a** | Продолжать автоматически (не спрашивать подтверждения) |
| **q** | Выйти из скрипта |

## Структура директорий после выполнения

```
tasks/
├── README.md
├── 00-guide.md
├── logs/
│   ├── L0-01-create-structure.md.log
│   ├── L0-02-create-config.md.log
│   ├── ...
│   └── SUMMARY.log
├── L0/
│   ├── DONE-L0-01-create-structure.md
│   ├── DONE-L0-02-create-config.md
│   ├── ...
│   └── SKIP-L0-03-create-requirements.md
├── L1/
│   ├── L1-09-base-model.md
│   ├── L1-10-tag-model.md
│   └── ...
└── ...
```

## Советы и трюки

### 1. Начните с нескольких задач

Для тестирования:

```bash
# Сбросьте все задачи (см. выше)
# Выполните только первые 3 задачи
python auto_executor.py
# ... после 3 задач выберите 'q'
```

### 2. Используйте разные модели

```bash
# Быстрая (но менее точная) модель
OPENAI_MODEL=gpt-3.5-turbo python auto_executor.py

# Медленная (но более точная) модель
OPENAI_MODEL=gpt-4 python auto_executor.py
```

### 3. Настройте контекст

```bash
# Без контекста (быстрее, но менее точно)
MAX_CONTEXT_TASKS=0 python auto_executor.py

# С большим контекстом (медленнее, но более точно)
MAX_CONTEXT_TASKS=5 python auto_executor.py
```

### 4. Проверяйте логи

После выполнения проверьте логи:

```bash
# Последние логи
ls -lt tasks/logs/ | head -10

# Поиск ошибок
grep -i "ошибка" tasks/logs/*.log
grep -i "error" tasks/logs/*.log
```

## Проблемы и решения

### ❌ Не задан OPENAI_API_KEY

**Решение:** Установите переменную окружения или настройте в `.env`

```bash
export OPENAI_API_KEY='sk-your-key-here'
# или отредактируйте .env
```

### ❌ LLM не может найти файлы

**Решение:** Убедитесь что находитесь в корне проекта и директория `tasks/` существует

```bash
ls tasks/
pwd
```

### ❌ Слишком много токенов

**Решение:** Уменьшите `MAX_CONTEXT_TASKS` в `.env`

```env
MAX_CONTEXT_TASKS=1
```

### ❌ Скрипт зависает

**Решение:** Используйте Ctrl+C для прерывания

```bash
^C
⚠️  Прервано пользователем
```

## Дополнительные ресурсы

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Ollama Documentation](https://ollama.com/docs)
- [Python-dotenv Documentation](https://pypi.org/project/python-dotenv/)

## Лицензия

MIT License

## Связь

Для вопросов и предложений создайте issue в репозитории.
