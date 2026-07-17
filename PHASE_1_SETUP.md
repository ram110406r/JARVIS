# Phase 1 Setup Guide: Building the Desktop Companion

This guide provides practical next steps for building JARVIS Phase 1 — the desktop companion MVP.

---

## Current Status

- ✅ Terminal MVP with tool routing complete
- ✅ Safety enforcement working
- ✅ Conversation memory functional
- ✅ Vision 2.0 architecture designed

## Next Steps (Q3 2026)

Build the desktop foundation:
1. Tauri + React setup
2. FastAPI backend
3. Voice interface (Whisper + Piper)
4. Screenshot capture
5. Integration & testing

---

## 1. Desktop UI Foundation (Weeks 1-2)

### 1.1 Tauri Project Setup

```bash
# Install Tauri CLI
npm install -g @tauri-apps/cli

# Create Tauri project
cargo install tauri-cli
tauri init --ci --app-name jarvis --window-title "JARVIS"

# Or use create-tauri-app template
npm create tauri-app@latest -- --manager npm --ui react --typescript
```

### 1.2 Project Structure

```
jarvis-desktop/
├── src-tauri/              # Rust backend
│   ├── src/
│   │   ├── main.rs        # Tauri setup
│   │   ├── commands.rs    # Tauri commands
│   │   └── api.rs         # FastAPI integration
│   ├── Cargo.toml
│   └── tauri.conf.json
├── src/                     # React frontend
│   ├── components/
│   │   ├── ChatWindow.tsx
│   │   ├── VoiceControl.tsx
│   │   ├── StatusBar.tsx
│   │   └── Notifications.tsx
│   ├── pages/
│   │   └── Home.tsx
│   ├── hooks/
│   │   ├── useVoice.ts
│   │   └── useChat.ts
│   ├── styles/
│   └── App.tsx
├── package.json
├── vite.config.ts
└── tailwind.config.ts
```

### 1.3 React + TypeScript Setup

```bash
npm install react react-dom typescript
npm install -D tailwindcss postcss autoprefixer
npm install zustand axios

# Initialize Tailwind
npx tailwindcss init -p
```

### 1.4 Key React Components

**ChatWindow.tsx**
- Message history
- Input field
- Voice indicators

**VoiceControl.tsx**
- Push-to-talk button
- Recording indicator
- Transcription display

**StatusBar.tsx**
- Connection status
- Model name
- Temperature slider

**Notifications.tsx**
- System notifications
- Action buttons

---

## 2. FastAPI Backend Setup (Weeks 2-3)

### 2.1 Create FastAPI Service

```bash
pip install fastapi uvicorn websockets python-multipart
mkdir jarvis-backend
cd jarvis-backend
```

### 2.2 Project Structure

```
jarvis-backend/
├── main.py                 # FastAPI app
├── config.py              # Settings
├── deps.py                # Dependencies
├── routes/
│   ├── chat.py           # Chat endpoints
│   ├── voice.py          # Voice endpoints
│   ├── screenshot.py     # Screenshot endpoints
│   └── tools.py          # Tool endpoints
├── services/
│   ├── ollama_service.py # LLM integration
│   ├── voice_service.py  # Whisper + Piper
│   ├── vision_service.py # Vision/OCR
│   └── context_service.py # Context management
├── models/
│   ├── schemas.py        # Pydantic models
│   └── types.py
├── tools/                 # Existing tools (from terminal)
├── logs/
└── requirements.txt
```

### 2.3 FastAPI Main App

```python
# main.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="JARVIS Backend", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
from routes import chat, voice, screenshot, tools
app.include_router(chat.router, prefix="/api/chat")
app.include_router(voice.router, prefix="/api/voice")
app.include_router(screenshot.router, prefix="/api/screenshot")
app.include_router(tools.router, prefix="/api/tools")

@app.on_event("startup")
async def startup():
    # Initialize services
    pass

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

### 2.4 Key Endpoints

**POST /api/chat**
```json
{
  "message": "What is the latest Python version?",
  "context": {}
}
```

**WebSocket /api/voice**
- Bidirectional voice streaming
- Send audio chunks
- Receive transcriptions

**POST /api/screenshot**
```json
{
  "capture": true,
  "analyze": true
}
```

---

## 3. Voice Interface (Weeks 3-4)

### 3.1 Install Dependencies

```bash
pip install openai-whisper piper-tts pyaudio

# Or for better audio handling:
pip install faster-whisper  # Faster Whisper inference
```

### 3.2 Whisper (STT) Service

```python
# services/voice_service.py
import whisper

model = whisper.load_model("base")  # or "small", "medium"

def transcribe_audio(audio_path: str) -> str:
    result = model.transcribe(audio_path)
    return result["text"]
```

### 3.3 Piper (TTS) Service

```python
# Or ElevenLabs for higher quality
pip install piper-tts

# Usage:
from piper.tts import PiperTTS

tts = PiperTTS()

def synthesize_speech(text: str) -> bytes:
    audio_bytes = tts.synthesize(text, speaker="en_US-ryan-medium")
    return audio_bytes
```

### 3.4 Voice WebSocket Handler

```python
# routes/voice.py
from fastapi import WebSocket

@app.websocket("/api/voice")
async def voice_websocket(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        # Receive audio chunk
        data = await websocket.receive_bytes()
        
        # Process with Whisper
        text = await transcribe_audio_chunk(data)
        
        # Send transcription
        await websocket.send_json({"type": "transcription", "text": text})
        
        # Send to LLM
        response = await ollama_service.chat(text)
        
        # Synthesize speech
        audio = await tts_service.synthesize(response)
        
        # Send back
        await websocket.send_bytes(audio, media_type="audio/wav")
```

---

## 4. Screenshot & Vision (Weeks 4-5)

### 4.1 Screenshot Capture

```bash
pip install pillow mss
```

```python
# services/screenshot_service.py
import mss
from PIL import Image

def capture_screenshot() -> Image.Image:
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        screenshot = sct.grab(monitor)
        return Image.frombytes('RGB', screenshot.size, screenshot.rgb)
```

### 4.2 OCR with PaddleOCR

```bash
pip install paddleocr
```

```python
# services/vision_service.py
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='en')

def extract_text_from_image(image_path: str) -> str:
    result = ocr.ocr(image_path, cls=True)
    text = "\n".join([line[0][1] for line in result])
    return text
```

### 4.3 Vision Model (Qwen2.5-VL or Moondream)

```bash
pip install transformers torch pillow

# Option 1: Qwen2.5-VL (recommended)
# Option 2: Moondream (lightweight)
```

```python
# Vision model integration
from transformers import Qwen2VLForConditionalGeneration, Qwen2VLProcessor

model = Qwen2VLForConditionalGeneration.from_pretrained("Qwen/Qwen2-VL")
processor = Qwen2VLProcessor.from_pretrained("Qwen/Qwen2-VL")

def analyze_screenshot(image_path: str, question: str) -> str:
    inputs = processor(
        text=question,
        images=image_path,
        return_tensors="pt"
    )
    outputs = model.generate(**inputs)
    response = processor.decode(outputs[0])
    return response
```

### 4.4 Screenshot Endpoint

```python
# routes/screenshot.py
from fastapi import APIRouter
from services.screenshot_service import capture_screenshot
from services.vision_service import analyze_screenshot

router = APIRouter()

@router.post("/capture")
async def capture():
    image = capture_screenshot()
    image.save("current_screenshot.png")
    return {"success": True, "path": "current_screenshot.png"}

@router.post("/analyze")
async def analyze(question: str):
    analysis = analyze_screenshot("current_screenshot.png", question)
    return {"analysis": analysis}
```

---

## 5. Context Management (Week 5)

### 5.1 Context Service

```python
# services/context_service.py
from typing import Dict, Any

class ContextManager:
    def __init__(self):
        self.context: Dict[str, Any] = {
            "active_window": None,
            "current_file": None,
            "open_tabs": [],
            "clipboard": None,
        }
    
    async def update_context(self, **kwargs):
        self.context.update(kwargs)
    
    def get_context(self) -> Dict[str, Any]:
        return self.context
    
    def format_for_llm(self) -> str:
        """Format context as string for LLM context injection"""
        lines = ["Current Context:"]
        if self.context["active_window"]:
            lines.append(f"- Active Window: {self.context['active_window']}")
        if self.context["current_file"]:
            lines.append(f"- Current File: {self.context['current_file']}")
        return "\n".join(lines)
```

### 5.2 Context Injection in Chat

```python
# routes/chat.py
@router.post("/chat")
async def chat(message: str, use_context: bool = True):
    if use_context:
        context_str = context_manager.format_for_llm()
        message = f"{context_str}\n\nUser: {message}"
    
    response = await ollama_service.chat(message)
    return {"response": response}
```

---

## 6. Integration with Terminal MVP (Week 6)

### 6.1 Reuse Existing Tools

The `tools/` directory from the terminal MVP can be reused:

```python
# services/tool_service.py
from tools.router import route_tool
from tools.browser import handle_browser
from tools.filesystem import handle_filesystem

class ToolService:
    async def execute_tool(self, tool_call: str) -> str:
        return route_tool(tool_call)
```

### 6.2 Tool Endpoints

```python
# routes/tools.py
@router.post("/browser")
async def browser_search(query: str):
    result = await tool_service.execute_browser(query)
    return result

@router.post("/filesystem")
async def filesystem_op(operation: str):
    result = await tool_service.execute_filesystem(operation)
    return result
```

---

## 7. System Tray & Hotkeys (Week 6-7)

### 7.1 Tauri System Tray

```rust
// src-tauri/src/main.rs
use tauri::SystemTrayMenu;

fn main() {
    let tray_menu = SystemTrayMenu::new()
        .add_item(MenuItem::new("Show", "show".to_string()))
        .add_item(MenuItem::new("Hide", "hide".to_string()))
        .add_native_item(SystemTrayMenuItem::Separator)
        .add_item(MenuItem::new("Exit", "quit".to_string()));

    tauri::Builder::default()
        .system_tray(SystemTray::new().with_menu(tray_menu))
        .on_system_tray_event(|app, event| match event {
            SystemTrayEvent::LeftClick { .. } => {
                // Show window
            }
            _ => {}
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### 7.2 Global Hotkey

```bash
npm install @tauri-apps/plugin-global-shortcut
```

```rust
// Register hotkey
let _ = tauri::GlobalShortcutManager::new(app)
    .register("cmd+shift+space", || {
        // Activate voice input
    });
```

---

## 8. Testing & Deployment (Week 7-8)

### 8.1 Testing

```bash
# Frontend tests
npm test

# Backend tests
pytest tests/

# Integration tests
pytest tests/integration/
```

### 8.2 Building

```bash
# Build Tauri app
tauri build

# Output in src-tauri/target/release/
```

### 8.3 Distribution

- Windows: `.msi` installer
- macOS: `.dmg` bundle
- Linux: AppImage or `.deb`

---

## Development Checklist

### Week 1-2: Desktop UI
- [ ] Tauri project initialized
- [ ] React component structure created
- [ ] Tailwind CSS configured
- [ ] ChatWindow component built
- [ ] VoiceControl component built

### Week 2-3: Backend API
- [ ] FastAPI app created
- [ ] Chat endpoints implemented
- [ ] Ollama integration working
- [ ] Conversation memory integrated
- [ ] CORS configured

### Week 3-4: Voice
- [ ] Whisper integration
- [ ] Audio capture working
- [ ] Piper TTS integration
- [ ] WebSocket voice streaming
- [ ] Frontend voice UI working

### Week 4-5: Vision
- [ ] Screenshot capture working
- [ ] PaddleOCR integrated
- [ ] Vision model selected & integrated
- [ ] Screenshot analysis endpoint
- [ ] Frontend screenshot preview

### Week 5-6: Context
- [ ] Context manager implemented
- [ ] Active window detection
- [ ] File tracking
- [ ] Context injection in LLM calls
- [ ] Context UI display

### Week 6-7: Polish
- [ ] System tray integration
- [ ] Global hotkeys
- [ ] Notifications
- [ ] Error handling
- [ ] Logging

### Week 7-8: Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing
- [ ] Performance optimization
- [ ] Build & deploy

---

## Key Resources

- **Tauri Docs:** https://tauri.app/v1/guides/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Whisper Docs:** https://github.com/openai/whisper
- **PaddleOCR:** https://github.com/PaddlePaddle/PaddleOCR
- **Qwen2.5-VL:** https://huggingface.co/Qwen/Qwen2-VL

---

## Success Criteria

✅ Desktop app launches and stays on-screen
✅ Push-to-talk captures voice input
✅ Transcription displays in real-time
✅ LLM generates responses
✅ Voice output plays through speakers
✅ Screenshots can be captured and analyzed
✅ Context awareness functions
✅ System tray integration works
✅ Tests pass
✅ Single-file build works (installer)

---

**Phase 1 Target:** End of Q3 2026
**Current Date:** July 18, 2026
**Time Remaining:** ~2.5 months
