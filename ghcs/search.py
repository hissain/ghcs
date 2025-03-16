import requests

GITHUB_API_URL = "https://api.github.com/search/code"

def search_github(query, user=None, repo=None, language=None, path=None, max_results=None, token=None):
    headers = {"Authorization": f"token {token}"}
    params = {"q": query}
    
    if user:
        params["q"] += f" user:{user}"
    if repo:
        params["q"] += f" repo:{repo}"
    if language:
        params["q"] += f" language:{language}"
    if path:
        params["q"] += f" path:{path}"
    if max_results:
        params["per_page"] = max_results

    print(f"Sending request to GitHub API with params: {params}")
    response = requests.get(GITHUB_API_URL, headers=headers, params=params)
    response.raise_for_status()
    results = response.json().get("items", [])
    print(f"GitHub API returned {len(results)} items.")
    return results