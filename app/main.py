from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.routes import chat, health
import os
import webbrowser
import threading

app = FastAPI(
    title="FastAPI + Ollama Chatbot",
    description="An intermediate-level chatbot with streaming, session memory, and WebSocket support.",
    version="1.0.0",
)

# CORS — allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(chat.router, tags=["Chat"])
app.include_router(health.router, tags=["Health"])

# Serve static frontend files
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to the chat UI."""
    return RedirectResponse(url="/static/index.html")


@app.on_event("startup")
async def open_browser():
    """Auto-open the browser when the server starts."""
    def _open():
        import time
        time.sleep(1.5)  # Wait for server to be fully ready
        webbrowser.open("http://localhost:8000")
    threading.Thread(target=_open, daemon=True).start()
