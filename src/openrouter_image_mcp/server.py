"""MCP Server for image recognition via OpenRouter API."""

import base64
import os
from pathlib import Path
from typing import Optional

import httpx
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import AnyUrl

# Load .env from package directory (not from current working directory)
package_dir = Path(__file__).parent.parent.parent
load_dotenv(package_dir / ".env")

app = Server("openrouter-image-mcp")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


def encode_image_to_base64(image_path: str) -> str:
    """Read image file and encode to base64."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_mime_type(image_path: str) -> str:
    """Get MIME type based on file extension."""
    ext = Path(image_path).suffix.lower()
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
    }
    return mime_types.get(ext, "image/jpeg")


async def call_openrouter_api(
    image_paths: list[str],
    prompt: str,
    model: str = OPENROUTER_MODEL,
) -> str:
    """Send images to OpenRouter vision model and get response."""
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not set in environment")
    
    # Build messages with images
    user_message_content = []
    
    for image_path in image_paths:
        base64_image = encode_image_to_base64(image_path)
        mime_type = get_mime_type(image_path)
        
        user_message_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:{mime_type};base64,{base64_image}"
            }
        })
    
    # Add text prompt
    user_message_content.append({
        "type": "text",
        "text": prompt
    })
    
    messages = [
        {
            "role": "user",
            "content": user_message_content
        }
    ]
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 4096,
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Unexpected API response: {result}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="analyze_image",
            description=(
                "Анализирует одно или несколько изображений с помощью vision модели "
                "через OpenRouter API. Поддерживает анализ скриншотов, фотографий, "
                "диаграмм и других изображений. Можно передать несколько изображений "
                "для сравнения или анализа разных аспектов."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "image_paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Список путей к файлам изображений",
                        "minItems": 1,
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Вопрос или инструкция по анализу изображений",
                        "default": "Проанализируй изображение и опиши что на нём изображено",
                    },
                    "model": {
                        "type": "string",
                        "description": "Модель для анализа (по умолчанию из .env)",
                        "default": OPENROUTER_MODEL,
                    },
                },
                "required": ["image_paths", "prompt"],
            },
        )
    ]


@app.call_tool()
async def call_tool(
    name: str,
    arguments: dict | None,
) -> list[TextContent]:
    """Handle tool calls from Cline."""
    if name == "analyze_image":
        if not arguments:
            raise ValueError("Missing arguments for analyze_image")
        
        image_paths = arguments.get("image_paths", [])
        prompt = arguments.get(
            "prompt",
            "Проанализируй изображение и опиши что на нём изображено"
        )
        model = arguments.get("model", OPENROUTER_MODEL)
        
        if not image_paths:
            raise ValueError("No image paths provided")
        
        try:
            result = await call_openrouter_api(
                image_paths=image_paths,
                prompt=prompt,
                model=model,
            )
            return [TextContent(type="text", text=result)]
        except FileNotFoundError as e:
            return [TextContent(type="text", text=f"Ошибка: {str(e)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Ошибка API: {str(e)}")]
    
    raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())