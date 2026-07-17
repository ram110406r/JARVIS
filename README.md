
# JARVIS - Just A Rather Very Intelligent System

> **An AI Operating System for Developers and Founders**

JARVIS is evolving from a terminal-based AI assistant into an intelligent **desktop AI companion**—similar to HeyClicky—focused on developers, founders, and productivity professionals.

## Vision 2.0

See [VISION.md](VISION.md) for the complete long-term vision, or [ROADMAP.md](ROADMAP.md) to track progress.

### Current Phase: Phase 1 — Desktop Companion (MVP)

JARVIS is currently a controlled, deterministic AI agent that runs locally via Ollama. It integrates with browser, filesystem, and terminal tools while preserving strict safeguards against hallucination and unsafe operations.

This terminal interface is the foundation for the desktop companion experience that will replace it in Phase 1.

## Installation

### Prerequisites
- Python 3.9+
- Ollama running locally
- Internet connection (for browser searches)

### Setup

```bash
# 1. Install dependencies
python -m pip install -r requirements.txt

# 2. Run tests to verify setup
python -m pytest -q

# 3. Start Ollama (in a separate terminal)
ollama serve

# 4. Run JARVIS
python jarvis.py
```

### Configuration

Edit [jarvis.py](jarvis.py#L9-L10) to customize:

```python
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3"  # or mistral, neural-chat, etc.
```

## Architecture

Current architecture is documented in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), including Phase 1+ evolution.

**Current (Terminal MVP):**
```text
jarvis.py                  # Main controller with enforcement logic
├── tools/
│   ├── router.py         # Tool routing logic
│   ├── browser.py        # Browser search (DuckDuckGo)
│   ├── filesystem.py     # Sandboxed file operations
│   ├── terminal.py       # Dry-run command validation
│   └── common.py         # Shared utilities
├── system_prompt.xml     # LLM system prompt
├── memory/               # Conversation state
└── logs/                 # Runtime logs
```

**Phase 1 Target (Desktop):**
See [VISION.md](VISION.md#high-level-architecture) for the desktop companion architecture with voice, vision, and context awareness.

## Current Tools

### Browser
```
<tool:browser>query</tool:browser>
```
Real-time search via DuckDuckGo.

### Filesystem
```
<tool:filesystem>create file 'name.txt' content 'hello'</tool:filesystem>
```
Sandboxed file operations (create, read, list, delete).

### Terminal
```
<tool:terminal>echo hello</tool:terminal>
```
Dry-run command inspection (validation only, no execution).

### Coming in Phase 1
- Voice input/output
- Screenshot capture & analysis
- OCR support
- Context awareness
- See [VISION.md](VISION.md) for the complete roadmap

## Safety & Design

JARVIS maintains strict safety constraints:

- ✅ **Trigger keywords** enforce browser tool for real-time queries
- ✅ **Hallucination detection** blocks knowledge cutoff responses
- ✅ **Sandboxed filesystem** restricts file operations
- ✅ **Dry-run terminal** validates but never executes commands
- ✅ **Bounded history** aggressively prunes conversation
- ✅ **Single tool per request** prevents tool chaining loops

For detailed design rules, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## What's Next?

JARVIS is transitioning to a **desktop companion** experience:

**Phase 1 (Q3-Q4 2026):** Desktop widget, voice input/output, screenshots
**Phase 2 (Q4 2026 - Q1 2027):** Context awareness
**Phase 3 (Q1-Q2 2027):** Vision system
**Phase 5 (Q3 2027):** Intelligent planner
**Phase 7 (Q1 2028):** Developer assistant
**Phase 10 (Q4 2028):** Plugin ecosystem

See [ROADMAP.md](ROADMAP.md) for detailed milestones and [VISION.md](VISION.md) for the complete 10-phase roadmap.

## Testing

Run the test suite:

```bash
python -m pytest -q
python -m pytest -q --cov=tools    # With coverage
python -m pytest -v                 # Verbose output
```

---

## Troubleshooting

**Ollama connection error:**
```bash
ollama serve
```

**Ensure prerequisites:**
- Python 3.9+
- Internet connection
- Ollama running on localhost:11434

**Check logs:**
See `logs/` directory for detailed error messages.

---

## Developer Notes

**Current Phase:** Phase 1 — Desktop Companion (MVP)
**Status:** Terminal foundation ready, desktop build begins Q3 2026

- [x] Terminal MVP with tool routing
- [x] Safety enforcement
- [x] Conversation memory
- [ ] Desktop widget (Tauri + React)
- [ ] Voice interface (Whisper + Piper)
- [ ] Screenshot analysis

For development guidelines, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## Contributing

This is a private research project. Contributions follow:
- Test coverage required
- Architecture changes documented
- Safety constraints preserved
- Phase alignment maintained

---

## License

Private project. Use at own risk.

## Author

Local AI Research Project
**Vision 2.0 Initiated:** July 18, 2026

---

**Last Updated:** July 18, 2026  
**Current Phase:** Phase 1 — Desktop Companion (MVP)  
**Next Milestone:** Tauri desktop foundation (August 2026)
