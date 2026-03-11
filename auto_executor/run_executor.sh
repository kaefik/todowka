#!/bin/bash
# Скрипт для быстрого запуска Автоматического Исполнителя Задач

set -e

echo "🚀 Автоматический Исполнитель Задач Todo API"
echo "=============================================="
echo

# Проверяем Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден"
    exit 1
fi

echo "✅ Python найден: $(python3 --version)"
echo

# Проверяем зависимости
echo "📦 Проверяем зависимости..."
if [ ! -f "requirements.executor.txt" ]; then
    echo "❌ Файл requirements.executor.txt не найден"
    exit 1
fi

# Проверяем установленные пакеты
python3 -c "import openai; print('✅ openai установлен')" 2>/dev/null || echo "⚠️  openai не установлен"
python3 -c "import anthropic; print('✅ anthropic установлен')" 2>/dev/null || echo "⚠️  anthropic не установлен"
python3 -c "import ollama; print('✅ ollama установлен')" 2>/dev/null || echo "⚠️  ollama не установлен"
python3 -c "import dotenv; print('✅ python-dotenv установлен')" 2>/dev/null || echo "⚠️  python-dotenv не установлен"
echo

# Проверяем .env
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не найден"
    echo "   Создаём из .env.executor.example..."
    cp .env.executor.example .env
    echo "   ✅ .env создан"
    echo "   ⚠️  Не забудьте настроить API ключ в .env!"
    echo
fi

# Загружаем переменные окружения
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "📋 Переменные окружения загружены из .env"
    echo
fi

# Проверяем LLM провайдера
if [ -z "$LLM_PROVIDER" ]; then
    echo "⚠️  LLM_PROVIDER не задан, использую openai"
    export LLM_PROVIDER=openai
fi

echo "🔧 Провайдер LLM: $LLM_PROVIDER"
echo

# Проверяем API ключ
case "$LLM_PROVIDER" in
    "openai")
        if [ -z "$OPENAI_API_KEY" ]; then
            echo "❌ OPENAI_API_KEY не задан"
            echo "   Установите переменную OPENAI_API_KEY в .env"
            exit 1
        fi
        echo "✅ OpenAI API ключ найден"
        ;;
    "zai")
        if [ -z "$ZAI_API_KEY" ]; then
            echo "❌ ZAI_API_KEY не задан"
            echo "   Установите переменную ZAI_API_KEY в .env"
            exit 1
        fi
        echo "✅ z.ai API ключ найден"
        ;;
    "anthropic")
        if [ -z "$ANTHROPIC_API_KEY" ]; then
            echo "❌ ANTHROPIC_API_KEY не задан"
            echo "   Установите переменную ANTHROPIC_API_KEY в .env"
            exit 1
        fi
        echo "✅ Anthropic API ключ найден"
        ;;
    "ollama")
        echo "✅ Ollama (локальный LLM)"
        ;;
    "custom")
        if [ -z "$CUSTOM_API_KEY" ]; then
            echo "❌ CUSTOM_API_KEY не задан"
            echo "   Установите переменную CUSTOM_API_KEY в .env"
            exit 1
        fi
        echo "✅ Custom API ключ найден"
        ;;
    *)
        echo "❌ Неизвестный провайдер: $LLM_PROVIDER"
        exit 1
        ;;
esac

echo
echo "=============================================="
echo "🚀 Запуск Автоматического Исполнителя Задач..."
echo "=============================================="
echo

# Запускаем executor
python3 auto_executor.py
