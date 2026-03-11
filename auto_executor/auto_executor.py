#!/usr/bin/env python3
"""
Автоматический исполнитель задач Todo API

Скрипт автоматически выполняет задачи из директории tasks/ используя LLM API.
Поддерживает OpenAI, Anthropic, и другие совместимые API.
"""

import os
import sys
import glob
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import subprocess

# ============ КОНФИГУРАЦИЯ ============

# Выберите провайдера LLM: 'openai', 'anthropic', 'ollama', 'custom'
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

# API настройки
API_KEY = os.getenv("OPENAI_API_KEY", "")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# Для Anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")

# Для z.ai
ZAI_API_KEY = os.getenv("ZAI_API_KEY", "")
ZAI_BASE_URL = os.getenv("ZAI_BASE_URL", "https://api.z.ai/api/coding/paas/v4")
ZAI_MODEL = os.getenv("ZAI_MODEL", "glm-4.7")

# Для Ollama (локальный LLM)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# Для Custom API
CUSTOM_API_KEY = os.getenv("CUSTOM_API_KEY", "")
CUSTOM_BASE_URL = os.getenv("CUSTOM_BASE_URL", "")
CUSTOM_MODEL = os.getenv("CUSTOM_MODEL", "")

# Настройки выполнения
AUTO_CONTINUE = False  # Если True, не спрашивает подтверждение (может изменяться во время выполнения)
MAX_CONTEXT_TASKS = 3  # Сколько предыдущих задач включать в контекст
USE_BASH_TOOLS = False  # Если True, LLM может выполнять bash команды

# ============ LLM КЛИЕНТЫ ============

class LLMClient:
    """Базовый класс для LLM клиентов"""
    
    def __init__(self, api_key: str, model: str, base_url: str = ""):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
    
    def chat(self, messages: List[Dict], temperature: float = 0.3) -> str:
        """Отправляет сообщение в LLM и получает ответ"""
        raise NotImplementedError


class OpenAIClient(LLMClient):
    """OpenAI клиент"""
    
    def __init__(self, api_key: str, model: str, base_url: str = ""):
        super().__init__(api_key, model, base_url)
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key, base_url=base_url or None)
        except ImportError:
            print("❌ Установите openai: pip install openai")
            sys.exit(1)
    
    def chat(self, messages: List[Dict], temperature: float = 0.3) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"ОШИБКА OpenAI: {str(e)}"


class AnthropicClient(LLMClient):
    """Anthropic клиент"""
    
    def __init__(self, api_key: str, model: str, base_url: str = ""):
        super().__init__(api_key, model, base_url)
        
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            print("❌ Установите anthropic: pip install anthropic")
            sys.exit(1)
    
    def chat(self, messages: List[Dict], temperature: float = 0.3) -> str:
        try:
            # Конвертируем сообщения в формат Anthropic
            system_prompt = ""
            user_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_prompt = msg["content"]
                else:
                    user_messages.append(msg)
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=temperature,
                system=system_prompt,
                messages=user_messages
            )
            return response.content[0].text
        except Exception as e:
            return f"ОШИБКА Anthropic: {str(e)}"


class ZaiClient(LLMClient):
    """z.ai клиент"""
    
    def __init__(self, api_key: str, model: str, base_url: str = ""):
        super().__init__(api_key, model, base_url or "https://api.z.ai/api/coding/paas/v4")
        
        try:
            from openai import OpenAI
            # z.ai API совместим с OpenAI API
            self.client = OpenAI(api_key=api_key, base_url=self.base_url)
        except ImportError:
            print("❌ Установите openai: pip install openai (z.ai использует OpenAI-совместимый API)")
            sys.exit(1)
    
    def chat(self, messages: List[Dict], temperature: float = 0.3) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"ОШИБКА z.ai: {str(e)}"


class OllamaClient(LLMClient):
    """Ollama клиент (локальный LLM)"""
    
    def __init__(self, api_key: str, model: str, base_url: str = ""):
        super().__init__(api_key, model, base_url or "http://localhost:11434")
        
        try:
            from ollama import Client
            self.client = Client(host=self.base_url)
        except ImportError:
            print("❌ Установите ollama: pip install ollama")
            sys.exit(1)
    
    def chat(self, messages: List[Dict], temperature: float = 0.3) -> str:
        try:
            # Конвертируем сообщения
            user_prompt = ""
            for msg in messages:
                if msg["role"] == "system":
                    user_prompt += f"СИСТЕМА: {msg['content']}\n\n"
                elif msg["role"] == "user":
                    user_prompt += f"ПОЛЬЗОВАТЕЛЬ: {msg['content']}\n\n"
                elif msg["role"] == "assistant":
                    user_prompt += f"АСИСТЕНТ: {msg['content']}\n\n"
            
            response = self.client.generate(
                model=self.model,
                prompt=user_prompt,
                options={
                    "temperature": temperature,
                    "num_predict": 4096
                }
            )
            return response["response"]
        except Exception as e:
            return f"ОШИБКА Ollama: {str(e)}"


# ============ ИНИЦИАЛИЗАЦИЯ LLM КЛИЕНТА ============

def get_llm_client() -> LLMClient:
    """Создаёт и возвращает LLM клиент"""
    if LLM_PROVIDER == "openai":
        if not API_KEY:
            print("❌ Не задан OPENAI_API_KEY")
            sys.exit(1)
        return OpenAIClient(API_KEY, MODEL, BASE_URL)
    
    elif LLM_PROVIDER == "anthropic":
        if not ANTHROPIC_API_KEY:
            print("❌ Не задан ANTHROPIC_API_KEY")
            sys.exit(1)
        return AnthropicClient(ANTHROPIC_API_KEY, ANTHROPIC_MODEL)
    
    elif LLM_PROVIDER == "zai":
        if not ZAI_API_KEY:
            print("❌ Не задан ZAI_API_KEY")
            sys.exit(1)
        return ZaiClient(ZAI_API_KEY, ZAI_MODEL, ZAI_BASE_URL)
    
    elif LLM_PROVIDER == "ollama":
        return OllamaClient("", OLLAMA_MODEL, OLLAMA_BASE_URL)
    
    elif LLM_PROVIDER == "custom":
        if not CUSTOM_API_KEY:
            print("❌ Не задан CUSTOM_API_KEY")
            sys.exit(1)
        return OpenAIClient(CUSTOM_API_KEY, CUSTOM_MODEL, CUSTOM_BASE_URL)
    
    else:
        print(f"❌ Неизвестный провайдер LLM: {LLM_PROVIDER}")
        sys.exit(1)


# ============ ЗАГРУЗКА ЗАДАЧ ============

def load_system_prompt():
    """Загружает системный промпт из 00-guide.md"""
    guide_path = "tasks/00-guide.md"
    if not os.path.exists(guide_path):
        return ""
    
    with open(guide_path, "r", encoding="utf-8") as f:
        return f.read()


def load_task(task_path: str) -> Dict:
    """Загружает содержимое задачи и возвращает словарь"""
    if not os.path.exists(task_path):
        return {"error": f"Файл не найден: {task_path}"}
    
    with open(task_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Извлекаем мета-данные из задачи
    metadata = {}
    lines = content.split('\n')
    
    for line in lines:
        if line.startswith('## Цель'):
            metadata['goal'] = line.replace('## Цель', '').strip()
        elif line.startswith('## Оценка усилия'):
            metadata['effort'] = line.replace('## Оценка усилия', '').strip()
    
    return {
        "path": task_path,
        "name": os.path.basename(task_path),
        "content": content,
        "metadata": metadata
    }


def get_task_files() -> List[str]:
    """Получает список всех задач в правильном порядке"""
    tasks = []
    
    # Порядок слоёв
    layer_order = ["L0", "L1", "L2", "L3", "L4", "L5", "L7", "L8"]
    
    for layer in layer_order:
        pattern = f"tasks/{layer}/*.md"
        files = glob.glob(pattern)
        
        # Сортируем файлы в каждом слое
        def task_sort_key(path: str) -> tuple:
            file_name = os.path.basename(path)
            file_stem = file_name.replace('.md', '')
            parts = file_stem.split('-')
            if len(parts) >= 2:
                layer_code = parts[0]
                task_number_str = parts[1].split('-')[0]
                try:
                    task_number = int(task_number_str)
                    return (layer_order.index(layer_code) if layer_code in layer_order else 99, task_number)
                except ValueError:
                    pass
            return (99, 0)
        
        tasks.extend(sorted(files, key=task_sort_key))
    
    return tasks


def get_completed_tasks() -> List[str]:
    """Получает список выполненных задач"""
    completed = []
    
    for layer in ["L0", "L1", "L2", "L3", "L4", "L5", "L7", "L8"]:
        pattern = f"tasks/{layer}/DONE-*.md"
        files = glob.glob(pattern)
        completed.extend(files)
    
    return completed


# ============ ВЫПОЛНЕНИЕ ЗАДАЧ ============

def build_context_history(completed_tasks: List[str], max_tasks: int = MAX_CONTEXT_TASKS) -> str:
    """Строит историю контекста из выполненных задач"""
    if not completed_tasks:
        return ""
    
    # Берём только последние max_tasks задач
    recent_tasks = completed_tasks[-max_tasks:]
    
    context = "Выполненные задачи (для контекста):\n"
    context += "=" * 60 + "\n"
    
    for task_path in recent_tasks:
        task_name = os.path.basename(task_path)
        task = load_task(task_path)
        
        context += f"\n### {task_name}\n"
        
        if 'metadata' in task and 'goal' in task['metadata']:
            context += f"Цель: {task['metadata']['goal']}\n"
        
        if 'metadata' in task and 'effort' in task['metadata']:
            context += f"Усилие: {task['metadata']['effort']}\n"
    
    context += "\n" + "=" * 60 + "\n"
    context += "Примечание: Используй эти задачи для понимания контекста проекта, но не повторяй код.\n"
    
    return context


def execute_task(task_path: str, llm_client: LLMClient, context_history: str = "") -> Dict:
    """Выполняет одну задачу через LLM"""
    task = load_task(task_path)
    
    if "error" in task:
        return {
            "success": False,
            "error": task["error"],
            "task": task
        }
    
    system_prompt = load_system_prompt()
    
    messages = [
        {"role": "system", "content": system_prompt},
    ]
    
    # Добавляем контекст
    if context_history:
        messages.append({
            "role": "system",
            "content": context_history
        })
    
    # Добавляем задачу
    task_prompt = f"""
Выполни следующую задачу:

{task['content']}

Важно:
1. Следуй инструкциям в "Подсказке для LLM"
2. Создавай/изменяй только указанные файлы
3. При завершении сообщи какие файлы были созданы/изменены
4. Включи примеры кода в своём ответе
5. После каждого шага сообщи что сделано
"""
    
    messages.append({
        "role": "user",
        "content": task_prompt
    })
    
    try:
        response = llm_client.chat(messages, temperature=0.3)
        
        return {
            "success": True,
            "response": response,
            "task": task
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "task": task
        }


def save_log(task_name: str, result: Dict):
    """Сохраняет результат выполнения в лог"""
    log_dir = "tasks/logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"{task_name}.log")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"Время выполнения: {timestamp}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Задача: {task_name}\n")
        f.write("=" * 60 + "\n\n")
        
        if result["success"]:
            f.write("РЕЗУЛЬТАТ: Успешно\n\n")
            f.write("Ответ LLM:\n")
            f.write("-" * 60 + "\n")
            f.write(result["response"])
        else:
            f.write("РЕЗУЛЬТАТ: Ошибка\n\n")
            f.write("Ошибка:\n")
            f.write(result.get("error", "Неизвестная ошибка"))
    
    return log_file


def mark_task_completed(task_path: str) -> bool:
    """Помечает задачу как выполненную (переименовывает файл)"""
    try:
        # Получаем директорию и имя файла
        dir_name = os.path.dirname(task_path)
        file_name = os.path.basename(task_path)
        
        # Формируем новое имя
        if file_name.startswith("DONE-"):
            return True  # Уже выполнена
        
        new_file_name = f"DONE-{file_name}"
        new_path = os.path.join(dir_name, new_file_name)
        
        # Переименовываем
        os.rename(task_path, new_path)
        return True
    except Exception as e:
        print(f"❌ Ошибка при переименовании: {e}")
        return False


def skip_task(task_path: str) -> bool:
    """Пропускает задачу (создаёт файл SKIP-)"""
    try:
        dir_name = os.path.dirname(task_path)
        file_name = os.path.basename(task_path)
        
        if file_name.startswith("SKIP-"):
            return True  # Уже пропущена
        
        new_file_name = f"SKIP-{file_name}"
        new_path = os.path.join(dir_name, new_file_name)
        
        os.rename(task_path, new_path)
        return True
    except Exception as e:
        print(f"❌ Ошибка при пропуске: {e}")
        return False


def unmark_task(task_path: str) -> bool:
    """Убирает префикс (DONE- или SKIP-)"""
    try:
        dir_name = os.path.dirname(task_path)
        file_name = os.path.basename(task_path)
        
        if file_name.startswith("DONE-"):
            new_file_name = file_name.replace("DONE-", "", 1)
            new_path = os.path.join(dir_name, new_file_name)
            os.rename(task_path, new_path)
            return True
        
        elif file_name.startswith("SKIP-"):
            new_file_name = file_name.replace("SKIP-", "", 1)
            new_path = os.path.join(dir_name, new_file_name)
            os.rename(task_path, new_path)
            return True
        
        return False
    except Exception as e:
        print(f"❌ Ошибка при разметке: {e}")
        return False


def update_readme():
    """Обновляет README.md с текущим статусом задач"""
    readme_path = "tasks/README.md"
    
    if not os.path.exists(readme_path):
        return
    
    # Получаем статусы задач
    all_tasks = get_task_files()
    completed_tasks = get_completed_tasks()
    
    # Читаем текущий README
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Обновляем таблицу статусов
    # (это простой пример, можно сделать более умный парсинг)
    pass  # TODO: Реализовать умное обновление README


# ============ МЕНЮ И УПРАВЛЕНИЕ ============

def print_menu() -> None:
    """Печатает меню управления"""
    print("\n" + "=" * 60)
    print("МЕНЮ УПРАВЛЕНИЯ")
    print("=" * 60)
    print("  y - Задача выполнена, переходи к следующей")
    print("  n - Задача не выполнена, повторим")
    print("  s - Пропустить задачу")
    print("  u - Снять отметку выполненной/пропущенной")
    print("  a - Продолжить автоматически (не спрашивать)")
    print("  q - Выйти")
    print("=" * 60)


# ============ ГЛАВНАЯ ФУНКЦИЯ ============

def main():
    """Главная функция выполнения всех задач"""
    
    # Объявляем глобальную переменную для возможности изменения
    global AUTO_CONTINUE
    
    # Проверяем окружение
    if LLM_PROVIDER == "openai" and not API_KEY:
        print("❌ Не задан OPENAI_API_KEY")
        print("   Установите переменную окружения:")
        print("   export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)
    
    # Инициализируем LLM клиент
    print(f"🚀 Инициализация {LLM_PROVIDER} клиента...")
    
    # Определяем модель для вывода
    if LLM_PROVIDER == "openai":
        model_name = MODEL
    elif LLM_PROVIDER == "anthropic":
        model_name = ANTHROPIC_MODEL
    elif LLM_PROVIDER == "zai":
        model_name = ZAI_MODEL
    elif LLM_PROVIDER == "ollama":
        model_name = OLLAMA_MODEL
    elif LLM_PROVIDER == "custom":
        model_name = CUSTOM_MODEL
    else:
        model_name = "неизвестно"
    
    print(f"   Модель: {model_name}")
    print(f"   API URL: {ZAI_BASE_URL if LLM_PROVIDER == 'zai' else BASE_URL if LLM_PROVIDER == 'openai' else '' if LLM_PROVIDER == 'anthropic' else OLLAMA_BASE_URL if LLM_PROVIDER == 'ollama' else ''}")
    
    try:
        llm_client = get_llm_client()
        print("✅ LLM клиент инициализирован\n")
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
        sys.exit(1)
    
    # Получаем список задач
    print("📋 Загрузка задач...")
    task_files = get_task_files()
    total_tasks = len(task_files)
    
    if total_tasks == 0:
        print("❌ Задачи не найдены!")
        print("   Убедитесь что директория tasks/ существует и содержит файлы задач")
        sys.exit(1)
    
    print(f"✅ Найдено {total_tasks} задач\n")
    
    # Получаем выполненные задачи
    completed_tasks = get_completed_tasks()
    print(f"📊 Уже выполнено: {len(completed_tasks)}/{total_tasks} задач")
    
    # Считаем по слоям
    layer_counts = {}
    for task in task_files:
        layer = os.path.basename(task).split('-')[0]
        if layer not in layer_counts:
            layer_counts[layer] = 0
        layer_counts[layer] += 1
    
    for layer, count in layer_counts.items():
        completed_in_layer = len([t for t in completed_tasks if layer in t])
        print(f"   {layer}: {completed_in_layer}/{count} выполнено")
    
    print("\n" + "=" * 60)
    print("НАЧИНАЕМ ВЫПОЛНЕНИЕ ЗАДАЧ")
    print("=" * 60 + "\n")
    
    # История контекста
    context_history = build_context_history(completed_tasks)
    
    # Главный цикл выполнения
    for i, task_path in enumerate(task_files, 1):
        task_name = os.path.basename(task_path)
        
        # Проверяем не выполнена ли задача
        if task_name.startswith("DONE-"):
            print(f"✅ [{i}/{total_tasks}] {task_name} - уже выполнена")
            continue
        
        if task_name.startswith("SKIP-"):
            print(f"⏭️  [{i}/{total_tasks}] {task_name} - пропущена")
            continue
        
        # Показываем информацию о задаче
        print(f"📝 [{i}/{total_tasks}] Выполняем: {task_name}")
        print("-" * 60)
        
        task = load_task(task_path)
        if 'metadata' in task:
            if 'goal' in task['metadata']:
                print(f"   Цель: {task['metadata']['goal']}")
            if 'effort' in task['metadata']:
                print(f"   Усилие: {task['metadata']['effort']}")
        print()
        
        # Выполняем задачу
        print("🤔 Обращаемся к LLM...")
        result = execute_task(task_path, llm_client, context_history)
        
        if not result["success"]:
            print(f"❌ Ошибка выполнения:")
            print(f"   {result['error']}")
            
            # Сохраняем лог ошибки
            save_log(task_name, result)
            
            # Спрашиваем что делать
            if not AUTO_CONTINUE:
                print_menu()
                choice = input("Что делаем? (y/n/s/u/q): ").lower()
                
                if choice == 'q':
                    print("\n🛑 Остановка выполнения")
                    break
                elif choice == 's':
                    skip_task(task_path)
                    print(f"⏭️  Задача пропущена")
                elif choice == 'u':
                    unmark_task(task_path)
                    print(f"↩️  Отметка снята")
                    continue  # Повторим
                elif choice == 'a':
                    AUTO_CONTINUE = True
                    continue  # Повторим
                # else - повторим
            
            continue
        
        # Выводим результат
        print("📤 Ответ LLM:\n")
        print(result["response"])
        print()
        
        # Сохраняем лог
        log_file = save_log(task_name, result)
        print(f"💾 Лог сохранён: {log_file}")
        
        # Автоматический режим
        if AUTO_CONTINUE:
            print("✅ Автоматически отмечаем как выполненную")
            mark_task_completed(task_path)
            
            # Добавляем в контекст (кратко)
            context_history += f"\n### {task_name}\n"
            if 'metadata' in task and 'goal' in task['metadata']:
                context_history += f"Выполнено: {task['metadata']['goal']}\n"
            
            print()
            continue
        
        # Интерактивный режим
        print_menu()
        choice = input("Задача выполнена успешно? (y/n/s/u/a/q): ").lower()
        
        if choice == 'y':
            # Отмечаем как выполненную
            if mark_task_completed(task_path):
                print("✅ Задача отмечена как выполненная")
                
                # Добавляем в контекст (кратко)
                context_history += f"\n### {task_name}\n"
                if 'metadata' in task and 'goal' in task['metadata']:
                    context_history += f"Выполнено: {task['metadata']['goal']}\n"
        
        elif choice == 's':
            # Пропускаем
            skip_task(task_path)
            print("⏭️  Задача пропущена")
        
        elif choice == 'u':
            # Снимаем отметку
            unmark_task(task_path)
            print("↩️  Отметка снята")
            continue  # Повторим
        
        elif choice == 'a':
            # Автоматический режим
            AUTO_CONTINUE = True
            print("🤖 Включён автоматический режим")
            
            # Отмечаем как выполненную
            mark_task_completed(task_path)
            
            # Добавляем в контекст (кратко)
            context_history += f"\n### {task_name}\n"
            if 'metadata' in task and 'goal' in task['metadata']:
                context_history += f"Выполнено: {task['metadata']['goal']}\n"
        
        elif choice == 'q':
            print("\n🛑 Остановка выполнения")
            break
        
        elif choice == 'n':
            print("🔄 Повторим задачу...")
            # Не переименовываем, повторим в следующем цикле
        
        else:
            print("❓ Неизвестная команда, повторим задачу...")
        
        print("=" * 60)
        print()
    
    # Итоги
    completed_count = len(get_completed_tasks())
    print("\n" + "=" * 60)
    print(f"🎉 Выполнение завершено!")
    print(f"📊 Статистика: {completed_count}/{total_tasks} задач выполнено")
    print("=" * 60)
    
    # Сохраняем итоговый лог
    summary_file = "tasks/logs/SUMMARY.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(summary_file, "a", encoding="utf-8") as f:
        f.write(f"\n{'=' * 60}\n")
        f.write(f"Сессия: {timestamp}\n")
        f.write(f"Провайдер: {LLM_PROVIDER}\n")
        f.write(f"Модель: {MODEL if LLM_PROVIDER == 'openai' else OLLAMA_MODEL if LLM_PROVIDER == 'ollama' else ANTHROPIC_MODEL}\n")
        f.write(f"Выполнено: {completed_count}/{total_tasks} задач\n")
        f.write("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Прервано пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
