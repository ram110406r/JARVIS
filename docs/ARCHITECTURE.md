# JARVIS Architecture Rules (Read First)

## Core Principles
- Single user request = at most ONE tool call
- NEVER loop tool calls
- NEVER re-fetch internet data for the same request
- After tool results, generate ONE final answer

## LLM Rules
- Use Ollama local LLM
- System prompt loaded from XML
- Do NOT simulate chain-of-thought
- Prefer concise final responses

## Tools
- browser: DuckDuckGo search only
- filesystem: sandboxed
- terminal: dry-run only

## Performance
- Trim conversation history aggressively
- Treat each request as independent unless stated
