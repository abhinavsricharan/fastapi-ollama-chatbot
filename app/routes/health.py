from fastapi import APIRouter
from app.config import OLLAMA_MODEL

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "model": OLLAMA_MODEL,
        "message": "FastAPI + Ollama Chatbot is running 🚀"
    }
