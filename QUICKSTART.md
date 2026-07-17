# JARVIS Quick Reference

## What is JARVIS 2.0?

A **desktop AI companion** for developers and founders that:
- Runs locally for privacy
- Listens via voice
- Sees your screen (with permission)
- Understands your work context
- Executes complex tasks safely
- Never feels like "just a chatbot"

---

## Current Status

**Phase:** Terminal MVP (Foundation Complete)
**Next:** Phase 1 Desktop Companion (Q3-Q4 2026)

---

## How to Navigate Documentation

| Document | Purpose |
|----------|---------|
| **README.md** | Project overview, setup, current tools |
| **VISION.md** | 10-phase roadmap, core principles, ultimate goal |
| **ROADMAP.md** | Timeline, milestones, success metrics |
| **PHASE_1_SETUP.md** | Implementation guide for desktop MVP |
| **docs/ARCHITECTURE.md** | Technical architecture, design decisions |
| **FEATURES.md** | Current & planned features by phase |

---

## Running Current Version (Terminal MVP)

```bash
# Install
pip install -r requirements.txt

# Test
python -m pytest -q

# Run (with Ollama running)
python jarvis.py
```

Example:
```
🤖 JARVIS online. Internet tools available.
🧑‍💻 You: What is the latest Python version?
[ENFORCED] Trigger keyword detected. Browser tool mandatory.
🤖 JARVIS (with internet):
Python 3.13 is the latest version...
```

---

## Phase 1 Timeline (Q3-Q4 2026)

| Week | Focus | Deliverable |
|------|-------|-------------|
| 1-2 | Desktop UI | Tauri + React app |
| 2-3 | Backend API | FastAPI running |
| 3-4 | Voice | Whisper + Piper working |
| 4-5 | Vision | Screenshots + OCR |
| 5-6 | Context | Context awareness |
| 6-7 | Polish | System tray, hotkeys |
| 7-8 | Testing | Build & test |

See [PHASE_1_SETUP.md](PHASE_1_SETUP.md) for details.

---

## 10-Phase Roadmap Overview

1. **Phase 1** (Q3 2026) — Desktop widget, voice, vision
2. **Phase 2** (Q4 2026) — Context awareness
3. **Phase 3** (Q1 2027) — Vision system
4. **Phase 4** (Q2 2027) — Interactive guidance
5. **Phase 5** (Q3 2027) — Intelligent planner
6. **Phase 6** (Q4 2027) — Multi-tool execution
7. **Phase 7** (Q1 2028) — Developer assistant
8. **Phase 8** (Q2 2028) — Founder assistant
9. **Phase 9** (Q3 2028) — Memory system
10. **Phase 10** (Q4 2028) — Plugin ecosystem

---

## Architecture Overview

### Current (Terminal)
```
User → jarvis.py → Ollama → Tools → Response
```

### Phase 1 Target (Desktop)
```
Voice/Text → Desktop UI → FastAPI → Planner → Tools → Voice/Visual Output
```

### Phase 5+ (Intelligent)
```
Context + User Request → Planner → Multi-Tool Orchestrator → LLM → Result
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for full details.

---

## Tech Stack by Phase

### Current (Terminal)
- Python, Ollama, FastAPI (partial)

### Phase 1 (Desktop)
- **Frontend:** Tauri, React, TypeScript
- **Backend:** FastAPI, Python
- **Voice:** Whisper, Piper
- **Vision:** PaddleOCR, Qwen2.5-VL

### Phase 5+ (Orchestration)
- LangGraph (planner)
- Multiple specialized agents

### Phase 9+ (Memory)
- SQLite, ChromaDB (vector DB)

---

## Key Principles

✅ **Local-first** — Privacy, no cloud by default
✅ **Tool-based** — Composable, transparent execution
✅ **Human-in-the-loop** — Users make critical decisions
✅ **Safe** — Permissions, validation, explain-before-acting
✅ **Modular** — Plugin system (Phase 10)

---

## For Phase 1 Developers

1. **Start Here:** [PHASE_1_SETUP.md](PHASE_1_SETUP.md)
2. **Architecture:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
3. **Components:**
   - Desktop: Tauri + React
   - Backend: FastAPI
   - Voice: Whisper + Piper
   - Vision: PaddleOCR
4. **Reuse:** Existing tools from `tools/` directory

---

## Testing

```bash
# Terminal MVP tests
python -m pytest -q

# Phase 1 tests (frontend & backend)
npm test           # React tests
pytest             # Backend tests
```

---

## Contributing to JARVIS

1. **Report Issues:** Use GitHub Issues
2. **Suggest Features:** Reference phase in [ROADMAP.md](ROADMAP.md)
3. **Code:** Follow architecture in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
4. **PR:** Link to phase/milestone

---

## Vision Statement

> **An AI Operating System for Developers and Founders.**

A desktop-native AI companion that:
- Understands your work
- Sees your screen (with permission)
- Hears your voice
- Remembers your projects
- Plans complex tasks
- Uses tools intelligently
- Executes workflows safely
- Teaches interactively
- Automates repetitive work
- Assists continuously throughout your day

---

## Questions?

- **"How do I get started?"** → See [PHASE_1_SETUP.md](PHASE_1_SETUP.md)
- **"What's the big picture?"** → See [VISION.md](VISION.md)
- **"When will feature X ship?"** → See [ROADMAP.md](ROADMAP.md)
- **"How does the current MVP work?"** → See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **"How do I run it now?"** → See [README.md](README.md#installation)

---

**Status:** Vision 2.0 Initiated — July 18, 2026
**Phase:** Terminal MVP Complete → Phase 1 Desktop Begins Q3 2026
**Target:** AI Operating System for Developers & Founders by 2029
