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

### Доступные модели

- `openai/gpt-4o` - по умолчанию, отличное качество
- `openai/gpt-4o-mini` - быстрее и дешевле
- `anthropic/claude-3.5-sonnet` - отличное vision
- `google/gemini-2.0-flash-exp` - очень быстрая
- `meta-llama/llama-3.2-90b-vision-instruct`

Полный список моделей: https://openrouter.ai/docs/models

## Подключение к Cline

Добавьте в настройки Cline (MCP Settings):

```json
{
  "mcpServers": {
    "openrouter-image": {
      "command": "python",
      "args": ["-m", "openrouter_image_mcp.server"],
      "env": {
        "OPENROUTER_API_KEY": "your_api_key"
      }
    }
  }
}
```

Или с указанием пути к проекту:

```json
{
  "mcpServers": {
    "openrouter-image": {
      "command": "python",
      "args": ["-m", "openrouter_image_mcp.server"],
      "cwd": "путь/к/проекту"
    }
  }
}
```

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