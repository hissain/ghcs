import argparse
import os
from ghs.search import search_github
from ghs.downloader import download_file

def main():
    parser = argparse.ArgumentParser(description="Search GitHub code and download matched files.")
    parser.add_argument("--query", required=True, help="Search term.")
    parser.add_argument("--language", help="Programming language filter.")
    parser.add_argument("--repo", help="Search in a specific repository (e.g., username/repo).")
    parser.add_argument("--token", help="GitHub Personal Access Token (or set GITHUB_TOKEN env var).")

    args = parser.parse_args()
    token = args.token or os.getenv("GITHUB_TOKEN")

    if not token:
        print("Error: GitHub token is required. Set via --token or GITHUB_TOKEN env var.")
        return

    results = search_github(args.query, args.language, args.repo, token)
    
    for item in results:
        file_url = item["html_url"].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        file_path = item["path"]
        download_file(file_url, file_path, token)

if __name__ == "__main__":
    main()
