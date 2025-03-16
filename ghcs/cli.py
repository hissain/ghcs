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
    parser.add_argument("--repo", help="Search in a specific repository (e.g., username/repo).")
    parser.add_argument("-p", "--path", help="Specify path specifier for filtering.")
    parser.add_argument("-m", "--max-results", type=int, help="Maximum number of results to return.")
    parser.add_argument("-t", "--token", help="GitHub Personal Access Token (or set GITHUB_TOKEN env var).")
    parser.add_argument("-d", "--download", action="store_true", help="Download matched files.")
    parser.add_argument("-dd", "--download-dir", default="codes", help="Directory to save downloaded files.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging.")
    parser.add_argument("-r", "--remark", help="Description of what should be extracted from the downloaded files.")
    parser.add_argument("-o", "--output-file", help="Output file to save the extracted code (default: print to console).")
    parser.add_argument("-e", "--extensions", help="Comma-separated list of file extensions to consider for extraction (e.g., .py,.js)")

    args = parser.parse_args()
    token = args.token or os.getenv("GITHUB_TOKEN")
    verbose = args.verbose

    if not token:
        print("Error: GitHub token is required. Set via -t/--token or GITHUB_TOKEN env var.")
        return

    if not args.query:
        print("Error: Search term is required.")
        return

    if verbose:
        print(f"Searching GitHub for: {args.query}")
        print(f"Language: {args.language}")
        print(f"User: {args.user}")
        print(f"Repository: {args.repo}")
        print(f"Path: {args.path}")
        print(f"Max Results: {args.max_results}")
        print(f"Download: {args.download}")
        print(f"Download Directory: {args.download_dir}")
        print(f"Verbose: {args.verbose}")
        if args.remark:
            print(f"Extraction remark: {args.remark}")
    
    results = search_github(
        query=args.query,
        user=args.user,
        repo=args.repo,
        language=args.language,
        path=args.path,
        max_results=args.max_results,
        token=token,
        verbose=verbose,
    )

    print(f"Found {len(results)} matching files.")
    
    # Keep track of whether we downloaded any files
    downloaded_any = False
    
    for item in results:
        file_url = item["html_url"].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        file_path = item["path"]

        if args.download:
            if verbose:
                print(f"Downloading: {file_url}")
            save_path = download_file(file_url, file_path, token, args.download_dir)
            if save_path:
                downloaded_any = True
        else:
            if verbose:
                print(f"Matched file: {file_path}\n(URL: {file_url})")
            else:
                print(f"Matched file: {file_path}")
    
    # Process extraction with Gemini if remark is provided and files were downloaded
    print(args.remark), print(args.download), print(downloaded_any)
    if args.remark and args.download and downloaded_any:
        if verbose:
            print(f"Extracting code based on remark: '{args.remark}'")
        
        # Parse extensions if provided
        file_extensions = None
        if args.extensions:
            file_extensions = args.extensions.split(',')
            if verbose:
                print(f"Filtering files by extensions: {file_extensions}")
        
        from ghcs.extractor import extract_code_with_gemini, convert_nb_to_python
        
        convert_nb_to_python(args.download_dir, verbose=verbose)
        extracted_code = extract_code_with_gemini(
            args.download_dir, 
            args.remark, 
            verbose=verbose,
            file_extensions=file_extensions
        )
        
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(extracted_code)
            print(f"Extraction saved to: {args.output_file}")
        else:
            print("\nExtracted Code:")
            print("=" * 80)
            print(extracted_code)
            print("=" * 80)

if __name__ == "__main__":
    main()