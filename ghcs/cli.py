import argparse
import os
import dotenv
from ghcs.search import search_github
from ghcs.downloader import download_file

dotenv.load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Search GitHub code and download matched files.")
    parser.add_argument("query", nargs="?", help="Search term.")
    parser.add_argument("-l", "--language", help="Programming language filter.")
    parser.add_argument("-u", "--user", help="Search in all repositories of a specific user.")
    parser.add_argument("-r", "--repo", help="Search in a specific repository (e.g., username/repo).")
    parser.add_argument("-p", "--path", help="Specify path specifier for filtering.")
    parser.add_argument("-m", "--max-results", type=int, help="Maximum number of results to return.")
    parser.add_argument("-t", "--token", help="GitHub Personal Access Token (or set GITHUB_TOKEN env var).")
    parser.add_argument("-d", "--download", action="store_true", help="Download matched files.")
    parser.add_argument("-dd", "--download-dir", default="codes", help="Directory to save downloaded files.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging.")

    args = parser.parse_args()
    token = args.token or os.getenv("GITHUB_TOKEN")

    if not token:
        print("Error: GitHub token is required. Set via -t/--token or GITHUB_TOKEN env var.")
        return

    if not args.query:
        print("Error: Search term is required.")
        return

    print(f"Searching GitHub for: {args.query}")
    print(f"Language: {args.language}")
    print(f"User: {args.user}")
    print(f"Repository: {args.repo}")
    print(f"Path: {args.path}")
    print(f"Max Results: {args.max_results}")
    print(f"Download: {args.download}")
    print(f"Download Directory: {args.download_dir}")
    print(f"Verbose: {args.verbose}")
    
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
            if args.verbose:
                print(f"Matched file: {file_path}\n(URL: {file_url})")
            else:
                print(f"Matched file: {file_path}")

if __name__ == "__main__":
    main()