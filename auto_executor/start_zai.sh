#!/bin/bash
# Быстрый старт для z.ai (GLM-4.7)

echo "🚀 Настройка z.ai для Автоматического Исполнителя Задач"
echo "======================================================"
echo

# Проверяем API ключ
echo "🔑 Проверяем z.ai API ключ..."
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не найден"
    echo "   Создаём из .zai.example..."
    cp .env.zai.example .env
    echo "   ✅ .env создан"
    echo
    echo "⚠️  ВАЖНО: Необходимо установить ваш z.ai API ключ!"
    echo
    echo "   1. Зайдите на https://z.ai/"
    echo "   2. Получите API ключ"
    echo "   3. Отредактируйте .env и установите ZAI_API_KEY"
    echo
    
    read -p "Хотите открыть .env для редактирования? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} .env
    fi
    
    echo
    read -p "Продолжить? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Отменено"
        exit 1
    fi
fi

# Загружаем переменные окружения
source .env 2>/dev/null || true

# Проверяем API ключ
if [ -z "$ZAI_API_KEY" ] || [ "$ZAI_API_KEY" = "your-zai-api-key-here" ]; then
    echo "❌ ZAI_API_KEY не задан или имеет примерное значение"
    echo "   Пожалуйста, отредактируйте .env и установите ZAI_API_KEY"
    exit 1
fi

echo "✅ z.ai API ключ найден"
echo

# Проверяем зависимости
echo "📦 Проверяем зависимости..."
python3 -c "import openai" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ openai установлен"
else
    echo "⚠️  openai не установлен"
    echo "   Устанавливаем..."
    pip3 install openai python-dotenv
    if [ $? -eq 0 ]; then
        echo "✅ openai установлен"
    else
        echo "❌ Ошибка установки openai"
        exit 1
    fi
fi
echo

# Проверяем модель
echo "🤖 Настройки:"
echo "   Провайдер: z.ai"
echo "   Модель: ${ZAI_MODEL:-glm-4.7}"
echo "   API URL: ${ZAI_BASE_URL:-https://api.z.ai/api/coding/paas/v4}"
echo

# Запуск
echo "======================================================"
echo "🚀 Запуск Автоматического Исполнителя Задач с z.ai..."
echo "======================================================"
echo

export LLM_PROVIDER=zai
python3 auto_executor.py
