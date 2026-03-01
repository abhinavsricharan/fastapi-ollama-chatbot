# 🤖 FastAPI + Ollama Chatbot

An intermediate-level chatbot built with **FastAPI** and **Ollama** that supports real-time streaming responses, multi-turn conversation memory, and a clean browser-based chat UI.

---

## ✨ Features

- ⚡ **Streaming responses** via WebSockets (token by token)
- 🧠 **Conversation memory** — remembers context across messages per session
- 🌐 **Browser UI** — clean chat interface served at `localhost:8000`
- 🔌 **REST + WebSocket API** — flexible integration options
- ⚙️ **Configurable** via `.env` — swap models, prompts, and history limits easily

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| LLM Backend | Ollama (local) |
| Server | Uvicorn |
| HTTP Client | httpx |
| Data Validation | Pydantic |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- A model pulled in Ollama, e.g. `ollama pull llama3`

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/fastapi-ollama-chatbot.git
cd fastapi-ollama-chatbot
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
copy .env.example .env       # Windows
# cp .env.example .env       # Mac/Linux
```
Edit `.env` to set your model name, system prompt, etc.

### 5. Start the server
```bash
uvicorn app.main:app --reload
```

The browser will open automatically at **http://localhost:8000** 🎉

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Redirects to chat UI |
| `GET` | `/health` | Server health check |
| `POST` | `/chat` | Non-streaming chat |
| `WS` | `/ws/chat/{session_id}` | Streaming WebSocket chat |
| `GET` | `/history/{session_id}` | Get conversation history |
| `DELETE` | `/history/{session_id}` | Clear conversation history |

---

## 📁 Project Structure

```
fastapi-chatbot/
├── app/
│   ├── main.py              # App entry point
│   ├── config.py            # Settings from .env
│   ├── models/
│   │   └── schemas.py       # Pydantic data models
│   ├── routes/
│   │   ├── chat.py          # Chat & WebSocket endpoints
│   │   └── health.py        # Health check endpoint
│   └── services/
│       ├── llm_service.py   # Ollama API integration
│       └── memory_service.py# Session memory management
├── static/
│   └── index.html           # Browser chat UI
├── .env.example             # Environment variable template
├── requirements.txt         # Python dependencies
└── README.md
```

---

## ⚙️ Configuration (`.env`)

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama3` | Model to use |
| `SYSTEM_PROMPT` | `You are a helpful AI...` | Bot personality |
| `MAX_HISTORY` | `20` | Max messages remembered per session |

---

## 📄 License

MIT — free to use and modify.
