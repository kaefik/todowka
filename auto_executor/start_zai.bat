@echo off
REM Быстрый старт для z.ai (GLM-4.7) - Windows

echo 🚀 Настройка z.ai для Автоматического Исполнителя Задач
echo ======================================================
echo.

REM Проверяем .env
if not exist .env (
    echo ⚠️  Файл .env не найден
    echo    Создаём из .env.zai.example...
    copy .env.zai.example .env >nul
    echo    ✅ .env создан
    echo.
    echo ⚠️  ВАЖНО: Необходимо установить ваш z.ai API ключ!
    echo.
    echo    1. Зайдите на https://z.ai/
    echo    2. Получите API ключ
    echo    3. Отредактируйте .env и установите ZAI_API_KEY
    echo.
    echo    Откройте .env в любом текстовом редакторе и установите ZAI_API_KEY
    pause
)

REM Проверяем API ключ (простая проверка)
findstr /C:"ZAI_API_KEY=" .env >nul 2>&1
if errorlevel 1 (
    echo ❌ ZAI_API_KEY не найден в .env
    echo    Пожалуйста, отредактируйте .env и установите ZAI_API_KEY
    pause
    exit /b 1
)

echo ✅ z.ai конфигурация найдена
echo.

REM Проверяем зависимости
echo 📦 Проверяем зависимости...
python -c "import openai" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  openai не установлен
    echo    Устанавливаем...
    pip install openai python-dotenv
    if errorlevel 1 (
        echo ❌ Ошибка установки openai
        pause
        exit /b 1
    )
    echo ✅ openai установлен
) else (
    echo ✅ openai установлен
)
echo.

REM Настройки
echo 🤖 Настройки:
echo    Провайдер: z.ai
echo    Модель: glm-4.7
echo    API URL: https://api.z.ai/api/coding/paas/v4
echo.

REM Запуск
echo ======================================================
echo 🚀 Запуск Автоматического Исполнителя Задач с z.ai...
echo ======================================================
echo.

set LLM_PROVIDER=zai
python auto_executor.py

if errorlevel 1 (
    echo.
    echo ❌ Ошибка выполнения
    pause
    exit /b 1
)

exit /b 0
