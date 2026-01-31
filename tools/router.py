from tools.browser import handle_browser
from tools.filesystem import handle_filesystem
from tools.terminal import handle_terminal


def extract_between(text, start, end):
    """Safely extract text between delimiters. Returns None if not found."""
    if start in text and end in text:
        return text.split(start)[1].split(end)[0].strip()
    return None


def route_tool(llm_output: str):
    """
    Route LLM output to appropriate tool.
    Returns str (tool result) or None (no tool call or failure).
    """
    if "<tool:browser>" in llm_output:
        query = extract_between(
            llm_output,
            "<tool:browser>",
            "</tool:browser>"
        )
        # Return None if extraction failed, otherwise return tool result
        if query is None:
            return None
        return handle_browser(query)

    elif "<tool:filesystem>" in llm_output:
        result = handle_filesystem(llm_output)
        return result if result else None

    elif "<tool:terminal>" in llm_output:
        result = handle_terminal(llm_output)
        return result if result else None

    return None
