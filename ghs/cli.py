import argparse
import os
import dotenv
from ghs.search import search_github
from ghs.downloader import download_file

dotenv.load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Search GitHub code and download matched files.")
    parser.add_argument("--query", required=True, help="Search term.")
    parser.add_argument("--language", help="Programming language filter.")
    parser.add_argument("--user", help="Search in all repositories of a specific user.")
    parser.add_argument("--repo", help="Search in a specific repository (e.g., username/repo).")
    parser.add_argument("--token", help="GitHub Personal Access Token (or set GITHUB_TOKEN env var).")
    parser.add_argument("--download", action="store_true", help="Download matched files.")

    args = parser.parse_args()
    token = args.token or os.getenv("GITHUB_TOKEN")

    if not token:
        print("Error: GitHub token is required. Set via --token or GITHUB_TOKEN env var.")
        return

    results = search_github(args.query, args.user, args.language, args.repo, token)

    print(f"Found {len(results)} matching files.")
    
    for item in results:
        file_url = item["html_url"].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        file_path = item["path"]

        if args.download:
            download_file(file_url, file_path, token)
        else:
            print(f"Matched file: {file_path} (URL: {file_url})")

if __name__ == "__main__":
    main()