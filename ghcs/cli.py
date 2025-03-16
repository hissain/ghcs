import argparse
import os
import dotenv
from ghcs.search import search_github
from ghcs.downloader import download_file

dotenv.load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Search GitHub code and download matched files.")
    parser.add_argument("--query", required=True, help="Search term.")
    parser.add_argument("--language", help="Programming language filter.")
    parser.add_argument("--user", help="Search in all repositories of a specific user.")
    parser.add_argument("--repo", help="Search in a specific repository (e.g., username/repo).")
    parser.add_argument("--path", help="Specify path specifier for filtering.")
    parser.add_argument("--max-results", type=int, help="Maximum number of results to return.")
    parser.add_argument("--token", help="GitHub Personal Access Token (or set GITHUB_TOKEN env var).")
    parser.add_argument("--download", action="store_true", help="Download matched files.")
    parser.add_argument("--download-dir", default="codes", help="Directory to save downloaded files.")

    args = parser.parse_args()
    token = args.token or os.getenv("GITHUB_TOKEN")

    if not token:
        print("Error: GitHub token is required. Set via --token or GITHUB_TOKEN env var.")
        return

    print(f"Searching GitHub for: {args.query}")
    results = search_github(
        query=args.query,
        user=args.user,
        repo=args.repo,
        language=args.language,
        path=args.path,
        max_results=args.max_results,
        token=token
    )

    print(f"Found {len(results)} matching files.")
    
    for item in results:
        file_url = item["html_url"].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        file_path = item["path"]

        if args.download:
            download_file(file_url, file_path, token, args.download_dir)
        else:
            print(f"Matched file: {file_path} (URL: {file_url})")

if __name__ == "__main__":
    main()