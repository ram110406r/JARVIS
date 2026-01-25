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

def ask_jarvis_final_answer(user_input: str, tool_result: str) -> str:
    """
    LLM-only call to generate final answer using tool results.
    Instructs LLM to use ONLY tool data and not call tools again.
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
    
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": conversation,
            "stream": False
        }
    ).json()
    
    reply = response["message"]["content"]
    conversation.append({"role": "assistant", "content": reply})
    
    # Sanitize response for hallucination indicators
    sanitize_response(reply)
    
    return reply

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
            final_reply = ask_jarvis_final_answer(user_input, tool_result)
            print(f"\n🤖 JARVIS (with internet):\n{final_reply}")
        
        else:
            # NORMAL FLOW: No trigger keywords, use standard LLM flow
            conversation.append({"role": "user", "content": user_input})

            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "messages": conversation,
                    "stream": False
                }
            ).json()

            reply = response["message"]["content"]
            conversation.append({"role": "assistant", "content": reply})

            print(f"\n🤖 JARVIS:\n{reply}")

            # Check if LLM requested a tool
            tool_result = route_tool(reply)

            if tool_result:
                conversation.append({
                    "role": "system",
                    "content": f"Tool result:\n{tool_result}"
                })

                # Call LLM once more to summarize tool result
                conversation.append({
                    "role": "user",
                    "content": "Summarize the tool result and answer the user."
                })
                
                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": MODEL,
                        "messages": conversation,
                        "stream": False
                    }
                ).json()

                final_reply = response["message"]["content"]
                conversation.append({"role": "assistant", "content": final_reply})
                print(f"\n🤖 JARVIS (with tool):\n{final_reply}")


if __name__ == "__main__":
    main()
