from duckduckgo_search import DDGS


def handle_browser(query: str) -> str:
    """
    Fetches real-time search results from DuckDuckGo.
    Returns formatted string with bullet points or None on failure.
    """
    try:
        formatted_results = []
        
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=3):
                title = r.get("title", "")
                snippet = r.get("body", "")
                source = r.get("href", "")
                
                if title and snippet:
                    formatted_results.append(
                        f"• {title}\n  {snippet}\n  Source: {source}"
                    )
        
        # Return formatted string or None if no results
        return "\n\n".join(formatted_results) if formatted_results else None
    
    except Exception as e:
        # Log error but return None gracefully
        print(f"[Browser tool error: {e}]")
        return None
