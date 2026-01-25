from duckduckgo_search import DDGS

def handle_browser(query: str):
    """
    Fetches real-time search results from DuckDuckGo.
    Returns clean, structured data.
    """

    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append({
                "title": r.get("title"),
                "snippet": r.get("body"),
                "source": r.get("href")
            })

    return results
