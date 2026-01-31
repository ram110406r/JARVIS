
# JARVIS - Just A Rather Very Intelligent System

A local, system-level AI assistant running on a laptop with strict safety enforcement and real-time internet access.

## Overview

JARVIS is a controlled, deterministic AI agent that runs locally via Ollama. It integrates with multiple tools (browser, filesystem, terminal) while maintaining strict rules to prevent hallucination and ensure accurate, up-to-date responses.

**Key Philosophy:** Stability and correctness over verbosity.

## Features

### Core Capabilities
- **Local LLM Integration** — Runs on Ollama (supports llama3, mixtral, etc.)
- **Real-time Internet Access** — DuckDuckGo browser tool for live information
- **System-Level Tools** — Filesystem and terminal access (controlled)
- **Single-Cycle Execution** — Each request resolves in at most 2 LLM calls

### Safety & Enforcement Layer
- **Mandatory Browser Tool Enforcement** — Triggers on keywords: `latest`, `current`, `version`, `recent`, `update`, `release`, `breaking`, `live`, `real-time`
- **Hallucination Detection** — Blocks responses containing: `"knowledge cutoff"`, `"as of my knowledge"`, etc.
- **No Memory Fallback** — Cannot answer "latest/version" questions from training data
- **Single Tool Call Limit** — Max one tool per request
- **Deterministic Responses** — No looping, no recursion, no chatbot behavior

## Architecture

```
jarvis.py                  # Main controller with enforcement layer
├── tools/
│   ├── router.py         # Tool routing logic
│   ├── browser.py        # Internet access via DuckDuckGo
│   ├── filesystem.py     # Safe file operations
│   └── terminal.py       # Shell command execution
├── system_prompt.xml     # LLM system prompt (11 sections)
└── memory/
    └── context.json      # Conversation context storage
```

## Installation

### Requirements
- Python 3.8+
- Ollama (running locally)
- `requests` library
- `rich` library (for terminal formatting)

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd JARVIS

# Install dependencies
pip install requests rich

# Ensure Ollama is running
ollama serve  # In another terminal

# Start JARVIS
python jarvis.py
```

## Usage

### Basic Interaction

```
🤖 JARVIS online. Internet tools available.

🧑‍💻 You: What is the latest Python version?
[ENFORCED] Trigger keyword detected. Browser tool mandatory.

🤖 JARVIS (with internet):
Python 3.13.1 is the latest stable release (released January 2025).
```

### Without Trigger Keywords (Normal LLM Mode)

```
🧑‍💻 You: What is Python used for?

🤖 JARVIS:
Python is a versatile programming language used for...
```

### With Optional Tool Usage

If the LLM requests a tool (non-enforced cases), JARVIS will invoke it and summarize results:

```
🤖 JARVIS:
<tool:browser>current weather in New York</tool:browser>

🤖 JARVIS (with internet):
The current weather in New York is...
```

## Enforcement Rules

### 1. Mandatory Browser Keywords

These keywords **force** browser tool invocation:

| Keyword | Triggers Browser |
|---------|------------------|
| `latest` | ✅ |
| `current` | ✅ |
| `now` | ✅ |
| `today` | ✅ |
| `version` | ✅ |
| `recent` | ✅ |
| `update` | ✅ |
| `release` | ✅ |
| `breaking` | ✅ |
| `live` | ✅ |
| `real-time` | ✅ |

### 2. Execution Flow

**With Trigger Keywords:**
1. Python detects keyword
2. Browser tool invoked directly (before LLM)
3. LLM called ONCE to summarize results
4. Final answer based only on live data

**Without Trigger Keywords:**
1. LLM processes query
2. If LLM requests tool, invoke it
3. LLM summarizes tool results
4. Final answer provided

### 3. Hallucination Prevention

Banned phrases that trigger hard fail:
- `"knowledge cutoff"`
- `"as of my knowledge"`
- `"as of my training"`
- `"my knowledge"`
- `"i cannot access"`

If detected, JARVIS raises a `RuntimeError` and blocks the response.

### 4. Single-Cycle Guarantee

- Max 1 tool invocation per request
- Max 2 LLM calls per request
- No recursive reasoning
- No automatic retries

## Tools

### Browser (`<tool:browser>`)
**Function:** Fetch real-time information from DuckDuckGo

```
<tool:browser>query</tool:browser>
```

**Use Cases:**
- Latest versions/releases
- Current events
- Real-world facts
- Stock prices, weather, news

**Enforcement:** Mandatory for trigger keywords

### Filesystem (`<tool:filesystem>`)
**Function:** Safe file read/write operations

```
<tool:filesystem>read /path/to/file</tool:filesystem>
```

**Permissions:** Restricted to approved directories

### Terminal (`<tool:terminal>`)
**Function:** Shell command execution

```
<tool:terminal>command</tool:terminal>
```

**Mode:** Dry-run by default; explicit approval required for state-changing commands

## Configuration

### System Prompt
Located in `system_prompt.xml`. Contains 11 enforced sections:

1. **Core Identity** — Name, description, persona
2. **Execution Model** — Single-cycle principles
3. **Tool Access Policy** — Available tools
4. **Tool Call Rules** — Format, limits, frequencies
5. **Tool Result Handling** — Authoritative results, no re-fetching
6. **Conversation Management** — Stateless, fresh requests
7. **Internet Safety** — No hallucination, mandatory browser usage
8. **Mandatory Tool Enforcement** — Keyword triggers, memory invalidation
9. **Strict Response Format** — Tool call format, no filler
10. **Ban Chatbot Patterns** — Forbidden phrases
11. **Performance Optimization** — Short, direct answers

### LLM Model
Edit `OLLAMA_URL` and `MODEL` in `jarvis.py`:

```python
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3"  # or "mixtral"
```

## Exit Commands

```
exit
quit
Ctrl+C
```

## Troubleshooting

### Exit Code 1
- Check Ollama is running: `ollama serve`
- Verify network connectivity for browser tool
- Check `system_prompt.xml` is present

### Browser Tool Returns Empty
- Check internet connection
- Verify DuckDuckGo is accessible
- Query may have no results

### Hallucination Error
- LLM attempted to answer from memory on a "latest/version" question
- Browser tool should have been invoked first
- Check system prompt enforcement is active

## Performance Notes

- **Cold Start:** First query takes ~2-3s (LLM initialization)
- **Trigger Keyword Query:** ~4-6s (browser + LLM)
- **Normal Query:** ~1-2s (LLM only)
- **Memory:** Conversation history stored in process (not persisted)

## Future Enhancements

- [ ] Persistent conversation storage
- [ ] Tool caching for repeated queries
- [ ] Additional tool types (email, calendar, code execution)
- [ ] Prompt optimization for speed
- [ ] Offline fallback mode

## License

Private project. Use at own risk.

## Author

Local AI Research Project
Date: January 2026

---

**Last Updated:** January 25, 2026
