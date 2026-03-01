import httpx
import json
from typing import AsyncGenerator, List
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL, SYSTEM_PROMPT


def _build_messages(history: List[dict], user_message: str) -> List[dict]:
    """Construct the full message list: system prompt + history + new user message."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})
    return messages


async def stream_chat(history: List[dict], user_message: str) -> AsyncGenerator[str, None]:
    """
    Call Ollama /api/chat with stream=True.
    Yields text tokens as they arrive.
    """
    messages = _build_messages(history, user_message)
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": True,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream(
            "POST",
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    token = data.get("message", {}).get("content", "")
                    if token:
                        yield token
                    if data.get("done", False):
                        break
                except json.JSONDecodeError:
                    continue


async def chat(history: List[dict], user_message: str) -> str:
    """
    Non-streaming call to Ollama. Returns full response as string.
    """
    messages = _build_messages(history, user_message)
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", "")
