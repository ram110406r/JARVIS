# JARVIS Backend — Phase 1

FastAPI backend for JARVIS desktop companion.

## Quick Start

### 1. Create Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # macOS/Linux
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Backend

```bash
python main.py
```

Backend will start at: **http://127.0.0.1:8000**

API Docs: **http://127.0.0.1:8000/docs**

## Project Structure

```
jarvis-backend/
├── main.py                    # FastAPI app & endpoints
├── requirements.txt           # Python dependencies
├── .env                       # Configuration (create locally)
├── services/
│   ├── __init__.py
│   ├── ollama_service.py      # LLM integration
│   ├── voice_service.py       # Whisper + TTS
│   ├── screenshot_service.py  # Screenshots & OCR
│   └── context_service.py     # Desktop context
├── tools/                     # (Phase 1+) Tool implementations
├── routes/                    # (Phase 1+) API route modules
└── tests/                     # (Phase 1+) Test suite
```

## API Endpoints

### Health & Config
- **GET** `/health` — Health check
- **GET** `/config` — Backend configuration

### Chat
- **POST** `/api/chat` — Send message
  ```json
  {
    "message": "What is the latest Python version?",
    "context": {}
  }
  ```

### Voice
- **WebSocket** `/api/voice` — Bidirectional voice communication
  - Send: Audio bytes
  - Receive: Transcriptions & responses

### Screenshots
- **POST** `/api/screenshot?analyze=true` — Capture & analyze
- **POST** `/api/screenshot?analyze=false` — Capture only

### Context
- **GET** `/api/context` — Get current desktop context

### Tools
- **POST** `/api/tools/browser?query=` — Web search
- **POST** `/api/tools/filesystem` — File operations
- **POST** `/api/tools/terminal` — Terminal command (dry-run)

## Configuration

Create `.env` file:

```env
# Ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Backend
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
DEBUG=true

# Voice (optional)
WHISPER_MODEL=base
TTS_PROVIDER=piper  # or elevenlabs

# Features
ENABLE_VOICE=true
ENABLE_VISION=true
ENABLE_CONTEXT=true
```

## Prerequisites

### Required
- Python 3.9+
- pip

### For Voice (Weeks 3-4)
```bash
pip install openai-whisper faster-whisper piper-tts gtts
```

### For Vision (Weeks 4-5)
```bash
pip install paddleocr pillow
```

### For Context (Week 5)
```bash
pip install pygetwindow pyperclip pyautogui
```

### Full Installation
```bash
pip install -r requirements-full.txt
```

## Development

### Run with Auto-Reload
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Run Tests
```bash
pytest tests/ -v
```

### Check Types
```bash
mypy services/
```

## Integration with Frontend

The desktop frontend (React) will connect to:
- **HTTP:** `/api/*` endpoints for REST calls
- **WebSocket:** `/api/voice` for real-time voice

CORS is enabled for localhost connections.

## Integration with Ollama

Ensure Ollama is running:
```bash
ollama serve
```

Then specify model in `.env` or code:
```python
service.set_model("llama2")  # or mistral, neural-chat, etc.
```

## Phase 1 Progress

- [x] FastAPI skeleton
- [x] Service layer (OllamaService, VoiceService, ScreenshotService, ContextManager)
- [x] Basic endpoints
- [ ] Whisper integration (Week 3)
- [ ] Piper integration (Week 3)
- [ ] Screenshot capture (Week 4)
- [ ] PaddleOCR integration (Week 4)
- [ ] Vision model integration (Week 4-5)
- [ ] Context detection (Week 5)
- [ ] Tool implementations (Week 5-6)
- [ ] Testing (Week 6-7)
- [ ] React frontend (Weeks 1-2 parallel)

## Troubleshooting

**Ollama connection error:**
```
❌ Cannot connect to Ollama. Ensure Ollama is running: ollama serve
```
Run: `ollama serve` in another terminal

**Module not found:**
```
pip install -r requirements.txt
```

**Port already in use:**
```
python main.py --port 8001
```

## Next Steps

1. **Week 3:** Install and integrate Whisper & Piper
2. **Week 4:** Add screenshot capture and OCR
3. **Week 5:** Implement context detection
4. **Week 6-7:** Build React frontend and connect

See [PHASE_1_SETUP.md](../PHASE_1_SETUP.md) for full timeline.

---

**Status:** Phase 1 Backend Foundation ✅ Complete
**Last Updated:** July 18, 2026
