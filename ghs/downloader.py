import requests
import os

def download_file(url, path, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Downloaded: {path}")
    else:
        print(f"Failed to download {url}")
