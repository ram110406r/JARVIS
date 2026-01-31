"""
JARVIS CONTROLLER

IMPORTANT RULES (DO NOT VIOLATE):
- Never call the LLM more than twice per user request
- Never allow recursive tool invocation
- Tools are single-pass only
- Tool results are final and authoritative
- Mandatory browser tool enforcement for trigger keywords
"""


import requests
from tools.router import route_tool
from rich import print

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3"  # or "mixtral"

# TRIGGER KEYWORDS FOR MANDATORY BROWSER TOOL INVOCATION
TRIGGER_KEYWORDS = [
    "latest", "current", "now", "today",
    "version", "recent", "update", "release",
    "breaking", "live", "real-time"
]

# BANNED PHRASES THAT INDICATE HALLUCINATION
BANNED_PHRASES = [
    "knowledge cutoff",
    "as of my knowledge",
    "as of my training",
    "my knowledge",
    "i cannot access"
]

def load_system_prompt():
    with open("system_prompt.xml", "r", encoding="utf-8") as f:
        return f.read()

SYSTEM_PROMPT = load_system_prompt()

conversation = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

# Conversation pruning settings
MAX_CONVERSATION_HISTORY = 10  # Keep system prompt + last N messages

# ============================================================================
# CORE LLM INTERFACE
# ============================================================================

def call_llm(messages: list) -> str | None:
    """
    Make a single LLM call to Ollama.
    
    Args:
        messages: List of message dicts with 'role' and 'content' keys
    
    Returns:
        Assistant response text, or None on error
    """
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False
            },
            timeout=30
        ).json()
        
        return response["message"]["content"]
    
    except requests.ConnectionError:
        print("\n❌ Cannot connect to Ollama. Ensure Ollama is running: ollama serve")
        return None
    except KeyError as e:
        print(f"\n❌ Ollama response error: Missing key {e}")
        return None
    except ValueError as e:
        print(f"\n❌ Ollama response error: Invalid response {e}")
        return None
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return None

def prune_conversation() -> None:
    """
    Keep conversation under control by maintaining only recent messages.
    Preserves system prompt and last MAX_CONVERSATION_HISTORY messages.
    """
    if len(conversation) > MAX_CONVERSATION_HISTORY + 1:
        # Keep system prompt (index 0) and last N messages
        system_msg = conversation[0]
        recent_msgs = conversation[-(MAX_CONVERSATION_HISTORY):]
        conversation.clear()
        conversation.append(system_msg)
        conversation.extend(recent_msgs)

# ============================================================================
# MANDATORY BROWSER TOOL ENFORCEMENT
# ============================================================================

def contains_trigger_keyword(query: str) -> bool:
    """
    Check if query contains any trigger keyword that mandates browser usage.
    Returns True if a keyword is found, False otherwise.
    """
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in TRIGGER_KEYWORDS)

def sanitize_response(response: str) -> None:
    """
    Check response for banned phrases indicating hallucination.
    Raises RuntimeError if hallucination patterns are detected.
    """
    response_lower = response.lower()
    for phrase in BANNED_PHRASES:
        if phrase in response_lower:
            raise RuntimeError(
                f"HALLUCINATION DETECTED: Response contains '{phrase}'. "
                f"This indicates memory-based answer to query requiring browser tool.\n"
                f"Response: {response}"
            )

def force_browser_tool(user_input: str) -> str:
    """
    Directly invoke browser tool without waiting for LLM.
    Constructs tool call and routes it immediately.
    """
    tool_call = f"<tool:browser>{user_input}</tool:browser>"
    tool_result = route_tool(tool_call)
    return tool_result

def ask_jarvis_final_answer(user_input: str, tool_result: str):
    """
    LLM-only call to generate final answer using tool results.
    Instructs LLM to use ONLY tool data and not call tools again.
    Returns tuple (success: bool, reply: str).
    """
    prompt = (
        f"User asked: {user_input}\n\n"
        f"Tool result:\n{tool_result}\n\n"
        f"Using ONLY the tool result above, answer the user directly.\n"
        f"Do not mention knowledge cutoffs.\n"
        f"Do not repeat the tool output verbatim.\n"
        f"Provide a concise, direct answer."
    )
    
    conversation.append({"role": "user", "content": prompt})
    
    reply = call_llm(conversation)
    
    if reply is None:
        # Error already printed by call_llm()
        conversation.pop()  # Remove message that failed
        return False, ""
    
    conversation.append({"role": "assistant", "content": reply})
    
    # Sanitize response for hallucination indicators
    try:
        sanitize_response(reply)
    except RuntimeError as e:
        print(f"\n⚠️ {e}")
        conversation.pop()  # Remove the failed response
        return False, ""
    
    prune_conversation()
    return True, reply

def main():
    print("🤖 JARVIS online. Internet tools available.")

    while True:
        user_input = input("\n🧑‍💻 You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Shutting down JARVIS.")
            break

        # KEYWORD ENFORCEMENT: Check for trigger keywords
        if contains_trigger_keyword(user_input):
            print("[ENFORCED] Trigger keyword detected. Browser tool mandatory.")
            
            # Force browser tool invocation BEFORE LLM
            tool_result = force_browser_tool(user_input)
            
            if not tool_result:
                print("🤖 JARVIS: Browser tool could not retrieve information.")
                continue
            
            # Call LLM only ONCE to summarize tool result
            success, final_reply = ask_jarvis_final_answer(user_input, tool_result)
            if success:
                print(f"\n🤖 JARVIS (with internet):\n{final_reply}")
        
        else:
            # NORMAL FLOW: No trigger keywords, use standard LLM flow
            conversation.append({"role": "user", "content": user_input})

            reply = call_llm(conversation)
            
            if reply is None:
                # Error already printed by call_llm(), message already removed
                conversation.pop()  # Remove user message that failed
                continue

            conversation.append({"role": "assistant", "content": reply})

            print(f"\n🤖 JARVIS:\n{reply}")

            # Check if LLM requested a tool
            tool_result = route_tool(reply)

            if tool_result:
                conversation.append({
                    "role": "system",
                    "content": f"Tool result:\n{tool_result}"
                })

                conversation.append({
                    "role": "user",
                    "content": "Summarize the tool result and answer the user."
                })
                
                final_reply = call_llm(conversation)
                
                if final_reply is None:
                    # Error already printed by call_llm()
                    conversation.pop()  # Remove user message that failed
                    conversation.pop()  # Remove tool result that failed
                    continue

                conversation.append({"role": "assistant", "content": final_reply})
                print(f"\n🤖 JARVIS (with tool):\n{final_reply}")
            
            prune_conversation()


if __name__ == "__main__":
    main()
