# JARVIS Architecture

## Vision 2.0 Context

JARVIS is transitioning from a terminal-based AI assistant to an intelligent desktop companion. This document describes:

1. **Current Architecture** — Terminal MVP (Phase 1 Foundation)
2. **Phase 1 Desktop Target** — Desktop widget with voice & vision
3. **Future Evolution** — Multi-phase architecture roadmap

See [VISION.md](../VISION.md) and [ROADMAP.md](../ROADMAP.md) for details.

---

## Current Architecture (Terminal MVP)

### Core Flow

```
User Input
    ↓
Trigger Keyword Check
    ↓
├─ YES → Force Browser Tool
│         ↓
│     Browser Search
│         ↓
│     LLM Final Answer
│
└─ NO → Direct LLM Call
        ↓
    Check for Tool Tags
        ↓
    ├─ Tool Found → Execute Tool
    │              ↓
    │          Tool Result
    │              ↓
    │          LLM Synthesis
    │
    └─ No Tool → Direct Response
```

### Component Structure

```
jarvis.py
├── call_llm()                 # Ollama API calls
├── contains_trigger_keyword() # Real-time query detection
├── force_browser_tool()       # Browser enforcement
├── sanitize_response()        # Hallucination detection
├── prune_conversation()       # Memory management
└── main()                     # REPL loop

tools/
├── router.py                  # Tool dispatcher
├── browser.py                 # DuckDuckGo search
├── filesystem.py              # Sandboxed file ops
├── terminal.py                # Command validation
└── common.py                  # Shared utilities (logging, etc.)

system_prompt.xml              # LLM system instructions
memory/context.json            # Conversation state
```

---

## Current Design Rules (Architecture Constraints)

### Core Principles
- Single user request = at most ONE tool call
- NEVER loop tool calls
- NEVER re-fetch internet data for same request
- After tool results, generate ONE final answer
- Use only Ollama local LLM
- Do NOT simulate chain-of-thought
- Prefer concise final responses

### Safety Rules
- Trigger keywords enforce browser tool usage
- Hallucination phrases block responses
- Filesystem access is sandboxed
- Terminal execution is dry-run (never execute)
- Conversation history is aggressively trimmed (max 10 messages)

---

## Phase 1 Target Architecture (Desktop)

### Desktop Component Structure

```
JARVIS Desktop
│
├── Frontend (Tauri + React)
│   ├── Main Window
│   │   ├── Chat interface
│   │   ├── Voice controls
│   │   └── Context display
│   ├── System Tray
│   │   ├── Quick access
│   │   └── Status
│   └── Floating Widget
│       ├── Voice activation
│       └── Quick queries
│
├── Backend API (FastAPI)
│   ├── /chat (POST)           # Send message
│   ├── /voice (WebSocket)     # Voice streaming
│   ├── /screenshot (POST)     # Screenshot + analysis
│   ├── /context (GET)         # Current context
│   └── /tools/{tool} (POST)   # Tool execution
│
├── Core Services
│   ├── Conversation Manager
│   ├── Tool Orchestrator
│   ├── Context Engine
│   ├── Voice Pipeline (STT/TTS)
│   └── Vision Pipeline (OCR, analysis)
│
└── Data Layer
    ├── Session Memory
    ├── User Preferences
    └── Knowledge Base (future)
```

### Voice Pipeline

```
Microphone
    ↓
Audio Capture
    ↓
Whisper (Speech-to-Text)
    ↓
LLM Processing
    ↓
Response Generation
    ↓
Piper (Text-to-Speech)
    ↓
Speaker Output
```

### Vision Pipeline

```
Screenshot
    ↓
Preprocessing
    ↓
├─ OCR Path
│  └─ PaddleOCR → Text extraction
│
└─ Vision Path
   └─ Qwen2.5-VL/Moondream → Analysis
   ↓
Context + Analysis
    ↓
User Response
```

---

## Phase 1+ Evolution

### Phase 2: Context Awareness

```
Desktop Service
├── Active Window Tracker
├── Application Detector
├── Project Detector (git root, package.json)
├── Browser Tab Monitor
├── File Watcher
├── Clipboard Monitor
└── Cursor Tracker
        ↓
Context Engine
        ↓
User Query (with context injected)
```

### Phase 5: Intelligent Planner

```
User Request
    ↓
Planner (LLM-based)
    ↓
├─ Task Decomposition
├─ Tool Selection
├─ Execution Plan
└─ Verification Strategy
    ↓
Tool Orchestrator
    ↓
Multi-Tool Execution
```

### Phase 10: Plugin System

```
Plugin Registry
├── Browser Plugin
├── Filesystem Plugin
├── Terminal Plugin
├── GitHub Plugin (example)
├── Docker Plugin (example)
└── Custom Plugins...
    ↓
Plugin Loader
    ↓
Permission System
    ↓
Tool Orchestrator
```

---

## Technology Stack Details

### Current (Terminal MVP)
- **Language:** Python 3.9+
- **CLI:** Rich
- **LLM:** Ollama
- **HTTP:** Requests
- **Search:** DuckDuckGo-Search

### Phase 1 Desktop
- **Desktop Framework:** Tauri (Rust + React)
- **Frontend:** React 18, TypeScript, Tailwind CSS
- **Backend:** FastAPI, AsyncIO
- **Voice:** Whisper (STT), Piper (TTS)
- **Vision:** PaddleOCR, Qwen2.5-VL or Moondream
- **Process:** Supervisor or systemd

### Future Phases
- **Memory:** SQLite + ChromaDB
- **Automation:** Playwright, PyAutoGUI
- **Integrations:** GitHub API, Docker API
- **Orchestration:** LangGraph (optional planner)

---

## Communication Protocols

### Current
- **LLM:** HTTP (Ollama REST API)
- **User:** STDIN/STDOUT

### Phase 1+
- **Frontend ↔ Backend:** WebSocket (real-time) + HTTP
- **Backend ↔ Ollama:** HTTP
- **Backend ↔ Services:** HTTP/gRPC
- **IPC:** Unix sockets (optional)

---

## Performance & Safety Considerations

### Performance
- Local-first execution (minimize cloud calls)
- Aggressive history pruning (memory efficiency)
- Async voice processing (non-blocking UI)
- Efficient screenshot handling (compression)

### Safety
- User confirmation for high-risk actions
- Audit logging of all operations
- Sandboxed execution where possible
- Permission-based tool access
- Response validation before display

---

## Development Phases & Architecture Changes

| Phase | Architecture Change | Key New Component |
|-------|---------------------|------------------|
| 1 | Terminal → Desktop | Floating widget, voice I/O |
| 2 | — | Context Engine |
| 3 | — | Vision Pipeline |
| 4 | — | Interactive Guidance System |
| 5 | Single Tool → Planner | Orchestrator, Plan Validator |
| 6 | — | Multi-Tool Sequencer |
| 7 | — | Repository Analyzer |
| 8 | — | Business Research Module |
| 9 | Session Memory → Persistent | Vector DB, SQLite layer |
| 10 | Hardcoded Tools → Plugins | Plugin Registry, Loader |

---

## Design Decisions & Rationale

### Why Local-First?
- Privacy: No data leaves the user's machine by default
- Performance: No network latency for local operations
- Reliability: Works offline or with poor connectivity
- Cost: No cloud infrastructure needed

### Why Tool-Based?
- Composability: Complex tasks built from simple tools
- Safety: Tool execution can be validated
- Transparency: Users see what JARVIS will do
- Extensibility: New tools added without core changes

### Why Tauri for Desktop?
- Lightweight: Smaller footprint than Electron
- Cross-platform: Windows, macOS, Linux
- Rust backend: Type-safe, performant
- Security: Secure IPC between frontend and backend

### Why AsyncIO for Backend?
- Concurrency: Multiple requests without threading
- Voice processing: Non-blocking audio capture/playback
- Websockets: Real-time updates to frontend
- Scalability: Handle multiple concurrent operations

---

## Future Considerations

- **Clustering:** Multi-machine JARVIS (future)
- **Federation:** Data sync across devices (future)
- **Agents:** Specialized AI agents for different domains (Phase 7+)
- **Learning:** User interaction feedback loops (Phase 9+)
- **Extension:** Third-party plugins and integrations (Phase 10)

---

**Current Status:** Phase 1 Planning
**Last Updated:** July 18, 2026

