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

## Установка и настройка

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

4. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

5. Добавьте ваш API ключ в `.env`:
```env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=openai/gpt-4o
```

Полный список доступных моделей: https://openrouter.ai/docs/models

## Подключение к Cline

Откройте настройки Cline (MCP Settings) и добавьте конфигурацию:

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

### ⚠️ Важное ограничение

Cline обрабатывает прикреплённые изображения **до** вызова MCP-инструментов. 
Если основная модель в Cline не поддерживает Vision — вы получите ошибку 404.

### Как использовать

1. Сохраните изображение в доступную папку
2. В чате передайте путь к файлу и опишите задачу:
   > "Проанализируй изображение ./screenshot.png с помощью analyze_image, найди ошибки"

### Примеры запросов

- "Проанализируй изображение c:\path\to\screenshot.png"
- "Сравни два скриншота: ./before.png и ./after.png"
- "Что изображено на картинке ./photo.jpg? Используй analyze_image"

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
└── README.md
```

## Лицензия

MIT