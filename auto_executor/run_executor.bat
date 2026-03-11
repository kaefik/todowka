@echo off
REM Скрипт для быстрого запуска Автоматического Исполнителя Задач (Windows)

echo 🚀 Автоматический Исполнитель Задач Todo API
echo ==============================================
echo.

REM Проверяем Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден
    echo Установите Python с https://python.org
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python найден: %PYTHON_VERSION%
echo.

REM Проверяем зависимости
echo 📦 Проверяем зависимости...
if not exist requirements.executor.txt (
    echo ❌ Файл requirements.executor.txt не найден
    exit /b 1
)

python -c "import openai" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  openai не установлен
    echo Установите: pip install openai
) else (
    echo ✅ openai установлен
)

python -c "import anthropic" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  anthropic не установлен
    echo Установите: pip install anthropic
) else (
    echo ✅ anthropic установлен
)

python -c "import ollama" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  ollama не установлен
    echo Установите: pip install ollama
) else (
    echo ✅ ollama установлен
)

python -c "import dotenv" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  python-dotenv не установлен
    echo Установите: pip install python-dotenv
) else (
    echo ✅ python-dotenv установлен
)
echo.

REM Проверяем .env
if not exist .env (
    echo ⚠️  Файл .env не найден
    echo    Создаём из .env.executor.example...
    copy .env.executor.example .env >nul
    echo    ✅ .env создан
    echo    ⚠️  Не забудьте настроить API ключ в .env!
    echo.
)

echo.
echo ==============================================
echo 🚀 Запуск Автоматического Исполнителя Задач...
echo ==============================================
echo.

REM Запускаем executor
python auto_executor.py

if errorlevel 1 (
    echo.
    echo ❌ Ошибка выполнения
    exit /b 1
)

exit /b 0
