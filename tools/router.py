from tools.browser import handle_browser
from tools.filesystem import handle_filesystem
from tools.terminal import handle_terminal

def extract_between(text, start, end):
    if start in text and end in text:
        return text.split(start)[1].split(end)[0].strip()
    return None

def route_tool(llm_output: str):
    if "<tool:browser>" in llm_output:
        query = extract_between(
            llm_output,
            "<tool:browser>",
            "</tool:browser>"
        )
        return handle_browser(query)

    elif "<tool:filesystem>" in llm_output:
        handle_filesystem(llm_output)

    elif "<tool:terminal>" in llm_output:
        handle_terminal(llm_output)

    return None
