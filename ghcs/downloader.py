import requests
import os

def download_file(url, path, token=None, download_dir="codes"):
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"token {token}"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            save_path = os.path.join(download_dir, path)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Downloaded: {save_path}")
            return save_path
        else:
            print(f"Failed to download {url}")
    except Exception as e:
        print(f"Error: {e}")
        print(f"Failed to download {url}")
        return None