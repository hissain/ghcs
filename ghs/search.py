import requests
import os

GITHUB_API_URL = "https://api.github.com/search/code"

def search_github(query, user=None, language=None, repo=None, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    search_query = f"{query}"
    if language:
        search_query += f" language:{language}"
    if repo:
        search_query += f" repo:{repo}"
    if user:
        search_query += f" user:{user}"

    params = {"q": search_query}
    print(f"Searching GitHub for: {search_query}")
    response = requests.get(GITHUB_API_URL, headers=headers, params=params)

    if response.status_code == 200:
        print(f"Found {response.json().get('total_count', 0)} matching files.")
        return response.json().get("items", [])
    else:
        print(f"Error: {response.status_code}, {response.json()}")
        return []
