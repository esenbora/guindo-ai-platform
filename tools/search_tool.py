from crewai.tools import tool
import os
import requests


@tool("web_search")
def search_web(query: str) -> str:
    """Search the web using Serper API. Useful for finding LinkedIn profiles and research."""
    api_key = os.getenv('SERPER_API_KEY')
    if not api_key:
        return f"Searching for: {query}\n(Mock results - SERPER_API_KEY not configured)"

    url = "https://google.serper.dev/search"
    payload = {"q": query, "num": 10}
    headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        results = response.json()
        
        formatted = []
        if 'organic' in results:
            for item in results['organic'][:10]:
                formatted.append(
                    f"Title: {item.get('title', 'N/A')}\n"
                    f"Link: {item.get('link', 'N/A')}\n"
                    f"Snippet: {item.get('snippet', 'N/A')}\n"
                )
        
        return "\n---\n".join(formatted) if formatted else "No results found"
        
    except Exception as e:
        return f"Error during search: {str(e)}"


@tool("export_data")
def export_data(data: str, filename: str) -> str:
    """Export data to a file in the outputs directory."""
    try:
        import os
        from datetime import datetime
        
        os.makedirs('outputs', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = filename.rsplit('.', 1)[0]
        ext = filename.rsplit('.', 1)[1] if '.' in filename else 'txt'
        file_path = os.path.join('outputs', f"{base_name}_{timestamp}.{ext}")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data)
            
        return f"Successfully exported to {file_path}"
        
    except Exception as e:
        return f"Error exporting data: {str(e)}"
