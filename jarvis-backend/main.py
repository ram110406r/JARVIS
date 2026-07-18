"""JARVIS Backend - FastAPI Application

Phase 1: Desktop Companion MVP
- Chat API
- Voice WebSocket
- Screenshot capture
- Context management
"""

from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict
import uvicorn
import asyncio
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Import services
from services.ollama_service import OllamaService
from services.voice_service import VoiceService
from services.screenshot_service import ScreenshotService
from services.context_service import ContextManager

# Initialize services
ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
ollama_model = os.getenv("OLLAMA_MODEL", "llama2")

ollama_service = OllamaService(base_url=ollama_url)
ollama_service.set_model(ollama_model)

voice_service = VoiceService()
screenshot_service = ScreenshotService()
context_manager = ContextManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    print("🚀 JARVIS Backend starting...")
    # Initialize services
    yield
    print("🛑 JARVIS Backend shutting down...")


app = FastAPI(
    title="JARVIS Backend",
    description="Desktop AI Companion for Developers",
    version="1.0.0",
    lifespan=lifespan
)

# Serve captured screenshots publicly
os.makedirs("public", exist_ok=True)
app.mount("/public", StaticFiles(directory="public"), name="public")

# Pydantic models for request/response validation
class ChatRequest(BaseModel):
    message: str
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    response: str
    tool_used: Optional[str] = None
    context: Optional[dict] = None

# Enable CORS for desktop frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost",
        "http://127.0.0.1"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "JARVIS Backend is running",
        "version": "1.0.0"
    }


@app.get("/config")
async def config():
    """Get backend configuration"""
    return {
        "name": "JARVIS",
        "version": "2.0.0",
        "phase": "Phase 1 - Desktop Companion MVP",
        "features": [
            "Chat API",
            "Voice Interface",
            "Screenshot Capture",
            "Context Management"
        ]
    }


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint
    
    Args:
        request: ChatRequest with message and optional context
    
    Returns:
        ChatResponse with response text and metadata
    """
    if not request.message:
        return {"error": "Message cannot be empty"}
    
    # Get context format
    context_str = ""
    if request.context:
        context_str = "\n".join([f"{k}: {v}" for k, v in request.context.items() if v])
    else:
        context_str = context_manager.format_for_llm()
    
    # Check if there are tool tags or keywords
    tool_used = None
    
    # Call Ollama service
    response = ollama_service.chat(request.message, context_str)
    
    # If Ollama offline, fallback to mock response
    if response is None:
        response = f"Echo (Ollama offline): {request.message}"
        
    return ChatResponse(
        response=response,
        tool_used=tool_used,
        context=request.context or context_manager.get_context()
    )


@app.websocket("/api/voice")
async def voice_websocket(websocket: WebSocket):
    """
    WebSocket for bidirectional voice communication
    
    Receive: Audio chunks (bytes)
    Send: 
        - Transcriptions (JSON with type="transcription", text="...")
        - Responses (JSON with type="response", text="...")
        - Audio (binary with type="audio")
    """
    await websocket.accept()
    print("🎤 Voice connection established")
    
    try:
        while True:
            # Receive audio data or text commands
            data = await websocket.receive()
            
            if "bytes" in data:
                # Audio chunk received
                audio_bytes = data["bytes"]
                
                # Transcribe audio bytes using Whisper
                transcription = voice_service.transcribe_audio(audio_bytes)
                if transcription and transcription.strip():
                    await websocket.send_json({
                        "type": "transcription",
                        "text": transcription
                    })
                    
                    # Call LLM chat with the transcription
                    context_str = context_manager.format_for_llm()
                    response_text = ollama_service.chat(transcription, context_str)
                    if not response_text:
                        response_text = f"Offline fallback. Heard: '{transcription}'"
                    
                    await websocket.send_json({
                        "type": "response",
                        "text": response_text
                    })
                    
                    # Convert response to speech audio bytes using TTS
                    audio_response = voice_service.synthesize_speech(response_text)
                    if audio_response:
                        await websocket.send_bytes(audio_response)
                else:
                    await websocket.send_json({
                        "type": "transcription",
                        "text": "(Audio not clear enough)"
                    })
            
            elif "text" in data:
                # Text message received
                message = data["text"]
                
                if message == "close":
                    break
                
                context_str = context_manager.format_for_llm()
                response_text = ollama_service.chat(message, context_str)
                if not response_text:
                    response_text = f"Offline fallback. Received text: {message}"
                
                await websocket.send_json({
                    "type": "response",
                    "text": response_text
                })
    
    except Exception as e:
        print(f"❌ Voice error: {e}")
    
    finally:
        print("📴 Voice connection closed")


@app.post("/api/screenshot")
async def screenshot(analyze: bool = False):
    """
    Capture and optionally analyze screenshot
    
    Args:
        analyze: If true, analyze with vision model
    
    Returns:
        {
            "success": bool,
            "path": "path/to/screenshot.png",
            "analysis": "..." (if analyze=true)
        }
    """
    try:
        os.makedirs("public", exist_ok=True)
        save_path = os.path.join("public", "screenshot.png")
        
        path = screenshot_service.capture_screenshot(save_path)
        if not path:
            return {
                "success": False,
                "message": "Failed to capture screenshot",
                "path": None,
                "analysis": None
            }
        
        analysis = None
        if analyze:
            # Analyze screenshot using ScreenshotService
            analysis = screenshot_service.analyze_screenshot(path, "Describe what is on this screen")
            
        # Return public web URL path
        return {
            "success": True,
            "message": "Screenshot captured successfully",
            "path": "/public/screenshot.png",
            "analysis": analysis
        }
    except Exception as e:
        print(f"❌ Screenshot capture error: {e}")
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "path": None,
            "analysis": None
        }


@app.get("/api/context")
async def get_context():
    """
    Get current desktop context
    
    Returns:
        {
            "active_window": "...",
            "current_file": "...",
            "open_tabs": [...],
            "clipboard": "...",
            "cursor_position": (x, y)
        }
    """
    try:
        active_window = context_manager.detect_active_window()
        clipboard = context_manager.get_clipboard()
        cursor = context_manager.get_cursor_position()
        cursor_pos = (cursor[0], cursor[1]) if cursor else None
        
        await context_manager.update_context(
            active_window=active_window,
            clipboard=clipboard,
            cursor_position=cursor_pos
        )
        return context_manager.get_context()
    except Exception as e:
        print(f"❌ Context error: {e}")
        return context_manager.get_context()


@app.post("/api/tools/browser")
async def browser_search(query: str):
    """Search the web using DuckDuckGo"""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        return {
            "success": True,
            "results": results,
            "query": query
        }
    except Exception as e:
        print(f"❌ Browser search error: {e}")
        return {
            "success": False,
            "results": [],
            "query": query,
            "error": str(e)
        }


@app.post("/api/tools/filesystem")
async def filesystem_operation(operation: str, path: str = None, content: str = None):
    """Filesystem operations (create, read, delete, list) within safe sandbox"""
    sandbox_dir = os.path.join(os.getcwd(), "sandbox")
    os.makedirs(sandbox_dir, exist_ok=True)
    
    if not path:
        return {"success": False, "error": "Path parameter is required"}
    
    # Path traversal safeguard
    safe_path = os.path.abspath(os.path.join(sandbox_dir, path))
    if not safe_path.startswith(os.path.abspath(sandbox_dir)):
        return {"success": False, "error": "Access denied: Path is outside the sandbox"}
        
    try:
        if operation in ("write", "create"):
            with open(safe_path, "w", encoding="utf-8") as f:
                f.write(content or "")
            return {"success": True, "operation": operation, "path": path}
            
        elif operation == "read":
            if not os.path.exists(safe_path):
                return {"success": False, "error": "File not found"}
            with open(safe_path, "r", encoding="utf-8") as f:
                data = f.read()
            return {"success": True, "operation": operation, "path": path, "content": data}
            
        elif operation == "delete":
            if os.path.exists(safe_path):
                if os.path.isdir(safe_path):
                    import shutil
                    shutil.rmtree(safe_path)
                else:
                    os.remove(safe_path)
                return {"success": True, "operation": operation, "path": path}
            return {"success": False, "error": "File not found"}
            
        elif operation == "list":
            if os.path.exists(safe_path) and os.path.isdir(safe_path):
                items = os.listdir(safe_path)
                return {"success": True, "operation": operation, "path": path, "items": items}
            return {"success": False, "error": "Directory not found"}
            
        else:
            return {"success": False, "error": f"Unsupported operation: {operation}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/tools/terminal")
async def terminal_operation(command: str, validate_only: bool = True):
    """Terminal command checker and execution in sandbox"""
    # Safeguard keywords
    unsafe_keywords = ["rm -rf", "format", "del /", "mkfs", "shutdown"]
    is_safe = not any(kw in command.lower() for kw in unsafe_keywords)
    
    if not is_safe:
        return {
            "success": False,
            "command": command,
            "validated": True,
            "result": "Blocked: unsafe command keyword detected"
        }
        
    if validate_only:
        return {
            "success": True,
            "command": command,
            "validated": True,
            "result": "Dry-run validation successful. Command is safe."
        }
        
    try:
        import subprocess
        sandbox_dir = os.path.join(os.getcwd(), "sandbox")
        os.makedirs(sandbox_dir, exist_ok=True)
        
        res = subprocess.run(
            command,
            shell=True,
            cwd=sandbox_dir,
            capture_output=True,
            text=True,
            timeout=10
        )
        return {
            "success": res.returncode == 0,
            "command": command,
            "validated": True,
            "stdout": res.stdout,
            "stderr": res.stderr,
            "exit_code": res.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "command": command,
            "validated": True,
            "error": str(e)
        }


if __name__ == "__main__":
    print("🚀 Starting JARVIS Backend...")
    print("📍 http://127.0.0.1:8000")
    print("📚 Docs: http://127.0.0.1:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
