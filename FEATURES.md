# JARVIS Phase 1 Features

## Project Overview

JARVIS Vision 2.0 is an intelligent desktop AI companion for developers and founders. Phase 1 focuses on building the desktop foundation with voice, vision, and context awareness capabilities.

**Current Implementation:** Terminal-based MVP with tool routing, safety enforcement, and conversation memory.

**Next Phase:** Desktop widget with voice input/output, screenshot analysis, and context awareness.

See [VISION.md](VISION.md) for the 10-phase roadmap.

---

## Phase 1 — Desktop Companion (MVP) Features

### Core Features (Current)
- ✅ Local LLM integration (Ollama)
- ✅ Tool-based architecture
- ✅ Browser search (DuckDuckGo)
- ✅ Filesystem operations (sandboxed)
- ✅ Terminal command validation (dry-run)
- ✅ Conversation memory (bounded)
- ✅ Safety enforcement (hallucination detection)

### Phase 1 Desktop Roadmap
- 🔄 Floating desktop widget
- 🔄 Global hotkey system
- 🔄 Push-to-talk voice input
- 🔄 Voice output (text-to-speech)
- 🔄 Screenshot capture & analysis
- 🔄 OCR support
- 🔄 System tray integration
- 🔄 Notifications

---

## Architecture

```text
JARVIS Desktop (Phase 1 Target)
├── Desktop Widget (Tauri + React)
│   ├── Floating window
│   ├── Voice controls
│   ├── Chat interface
│   └── System tray
├── Backend API (FastAPI + Python)
│   ├── Tool orchestration
│   ├── LLM routing
│   ├── Context management
│   └── Logging
├── Tools
│   ├── Browser (DuckDuckGo)
│   ├── Filesystem (sandboxed)
│   ├── Terminal (dry-run)
│   ├── Python (code execution)
│   └── Vision (screenshot analysis)
└── Memory & Storage
    ├── Session memory
    ├── User preferences
    └── Knowledge base (future)
```

---

## Current Tool Components

### Browser Tool
**Purpose:** Fetch live results from DuckDuckGo.
**How it works:** Searches and returns structured results.
**Benefits:** Real-time information, reliable results.
**Limitations:** Requires network, limited to DuckDuckGo.

### Filesystem Tool
**Purpose:** Create, read, list, and delete files safely.
**How it works:** Validates paths, enforces sandbox restrictions.
**Benefits:** Safe local file handling.
**Limitations:** Restricted to sandbox directory.

### Terminal Tool
**Purpose:** Inspect and validate terminal commands (dry-run only).
**How it works:** Parses commands, checks against allowlist, prevents execution.
**Benefits:** Prevents accidental destructive operations.
**Limitations:** Commands are validated but not executed.

### Router
**Purpose:** Route LLM-generated tool requests to handlers.
**How it works:** Extracts `<tool:*>` tags from LLM output.
**Benefits:** Modular, maintainable architecture.
**Limitations:** Fixed set of tools (plugins in Phase 10).

---

## Safety Model

### Current Protections
- ✅ Trigger keywords enforce browser usage
- ✅ Hallucination phrase detection
- ✅ Sandboxed filesystem access
- ✅ Dry-run terminal validation
- ✅ Bounded conversation history

### Future Protections (Phase 5+)
- 🔄 Permission system
- 🔄 High-risk action confirmation
- 🔄 Audit logging
- 🔄 Action rollback capability

---

## Technology Stack

### Current
- Python 3.9+
- Ollama (local LLM)
- FastAPI
- DuckDuckGo API
- Rich CLI

### Phase 1 (Desktop)
- Tauri (window management)
- React + TypeScript (UI)
- Whisper (voice input)
- Piper (voice output)
- PaddleOCR (optical character recognition)
- Qwen2.5-VL or Moondream (vision)

### Future Phases
- ChromaDB (semantic memory)
- PostgreSQL (long-term storage)
- GitHub API (developer assistant)
- Docker API (container management)

## Testing
The project now includes automated tests covering the core controller and tool handlers.

## Future Roadmap
- Add persistent memory storage
- Add richer logging and observability
- Add CI and packaging
