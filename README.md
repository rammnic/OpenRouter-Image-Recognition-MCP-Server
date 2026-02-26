# OpenRouter Image Recognition MCP Server

MCP (Model Context Protocol) сервер для распознавания и анализа изображений через OpenRouter API с использованием vision моделей.

## Возможности

- Анализ одного или нескольких изображений
- Поддержка форматов: JPG, PNG, GIF, WebP, BMP
- Гибкий prompt - передаётся из Cline
- Работа с различными vision моделями через OpenRouter

## Требования

- Python 3.10+
- API ключ OpenRouter

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/rammnic/OpenRouter-Image-Recognition-MCP-Server.git
cd OpenRouter-Image-Recognition-MCP-Server
```

2. Создайте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -e .
```

4. Настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env и добавьте ваш API ключ
```

## Конфигурация

Создайте файл `.env` на основе `.env.example`:

```env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=openai/gpt-4o
```

Полный список доступных моделей: https://openrouter.ai/docs/models

## Подключение к Cline

### Шаг 1: Установка

```bash
cd путь/к/проекту
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

### Шаг 2: Настройка

1. Создайте файл `.env` на основе `.env.example` и добавьте ваш API ключ:
   ```bash
   cp .env.example .env
   # Отредактируйте .env и добавьте OPENROUTER_API_KEY
   ```

2. Откройте настройки Cline (MCP Settings) и добавьте конфигурацию:

```json
{
  "mcpServers": {
    "openrouter-image": {
      "command": "полный/путь/к/проекту/.venv/Scripts/python.exe",
      "args": ["-m", "openrouter_image_mcp.server"]
    }
  }
}
```

**Важно:** Укажите полный путь к Python в виртуальном окружении. Например:
- `C:\path\to\project\.venv\Scripts\python.exe`

API ключ автоматически загрузится из `.env` файла.

## Использование

### В Cline

1. Добавьте изображение в чат (drag & drop или paste)
2. Опишите что нужно сделать: "Найди ошибки на скриншоте"
3. Cline автоматически вызовет MCP инструмент `analyze_image`

### Примеры запросов

- "Проанализируй этот скриншот"
- "Что изображено на картинке?"
- "На первом скриншоте найди ошибки в консоли, на втором проверь верстку"
- "Сравни эти два изображения"

### Прямой запуск для тестирования

```bash
python -m openrouter_image_mcp.server
```

## Структура проекта

```
openrouter-image-mcp/
├── src/
│   └── openrouter_image_mcp/
│       ├── __init__.py
│       └── server.py           # MCP сервер
├── pyproject.toml              # Зависимости
├── .env.example                # Пример конфигурации
├── .gitignore
├── .clineignore
├── .clinerules
└── README.md
```

## Лицензия

MIT