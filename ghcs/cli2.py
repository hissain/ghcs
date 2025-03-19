import argparse
import os
import time
import tempfile
from urllib.parse import quote_plus
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import dotenv

dotenv.load_dotenv()

def setup_driver(headless=True):
    """Set up and return a Chrome WebDriver instance with custom cache directory."""
    chrome_options = Options()
    # if headless:
    #     chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # Use a temporary directory for ChromeDriver
    temp_dir = tempfile.mkdtemp()
    
    # Try multiple approaches to initialize the driver
    try:
        # First try: Use Chrome directly if it's in the PATH
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"First driver attempt failed: {e}")
        
        try:
            # Second try: Specify a custom path for ChromeDriver
            os.environ["CHROMEDRIVER_PATH"] = os.path.join(temp_dir, "chromedriver")
            service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
        except Exception as e:
            print(f"Second driver attempt failed: {e}")
            
            try:
                # Final fallback: Use whatever Chrome browser is available
                from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
                driver = webdriver.Chrome(options=chrome_options, desired_capabilities=DesiredCapabilities.CHROME)
                return driver
            except Exception as e:
                print(f"All attempts to initialize Chrome driver failed: {e}")
                raise RuntimeError("Could not initialize Chrome driver. Make sure Chrome is installed.")

def search_github_selenium(query, user=None, repo=None, language=None, path=None, max_results=None, verbose=False):
    """
    Search GitHub code using Selenium to scrape the web interface.
    """
    driver = None
    results = []
    
    try:
        driver = setup_driver()
        
        # Construct GitHub search URL
        search_url = "https://github.com/search?type=code&q="
        search_parts = []
        
        # Add main query
        search_parts.append(quote_plus(query))
        
        # Add filters
        if user:
            search_parts.append(f"user:{user}")
        if repo:
            search_parts.append(f"repo:{repo}")
        if language:
            search_parts.append(f"language:{language}")
        if path:
            search_parts.append(f"path:{path}")
        
        # Combine all parts
        search_query = "+".join(search_parts)
        full_url = f"{search_url}{search_query}"
        
        if verbose:
            print(f"Searching using URL: {full_url}")
            
        driver.get(full_url)
        
        # Wait for search results to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".code-list-item, .code-list .flex-auto"))
            )
        except TimeoutException:
            if verbose:
                print("Timeout waiting for search results. GitHub might be rate limiting or no results found.")
            return results
        
        # Process results page by page until we have enough results
        page_num = 1
        while len(results) < (max_results or float('inf')):
            if verbose:
                print(f"Processing page {page_num}...")
                
            # Give time for page to fully load
            time.sleep(2)
            
            # Extract results from current page (handle different GitHub UI patterns)
            items = driver.find_elements(By.CSS_SELECTOR, ".code-list-item, .code-list .flex-auto")
            
            if not items:
                if verbose:
                    print("No items found on this page. Page structure might have changed.")
                break
                
            for item in items:
                if len(results) >= (max_results or float('inf')):
                    break
                    
                try:
                    # Extract repository and file information (handle different GitHub UI layouts)
                    repo_name = ""
                    file_path = ""
                    file_url = ""
                    
                    # Try different CSS selectors based on GitHub's UI variations
                    try:
                        # New GitHub UI
                        repo_element = item.find_element(By.CSS_SELECTOR, "a[data-testid='search-result-repo-name']")
                        repo_name = repo_element.text.strip()
                        file_element = item.find_element(By.CSS_SELECTOR, "a[data-testid='search-result-path']")
                        file_path = file_element.text.strip()
                        file_url = file_element.get_attribute("href")
                    except:
                        # Alternative/older GitHub UI
                        try:
                            repo_element = item.find_element(By.CSS_SELECTOR, ".f4.text-normal")
                            repo_name = repo_element.text.strip()
                            file_element = item.find_element(By.CSS_SELECTOR, ".f4 a")
                            file_path = file_element.text.strip()
                            file_url = file_element.get_attribute("href")
                        except:
                            # Last resort: try to find any links
                            links = item.find_elements(By.TAG_NAME, "a")
                            for link in links:
                                href = link.get_attribute("href")
                                if href and "/blob/" in href:
                                    file_url = href
                                    file_path = link.text.strip()
                                elif repo_name == "" and href and "github.com/" in href:
                                    repo_name = link.text.strip()
                    
                    if file_url and "/blob/" in file_url:
                        # Convert to raw URL format
                        raw_url = file_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                        
                        result = {
                            "repository": repo_name,
                            "path": file_path,
                            "html_url": file_url,
                            "raw_url": raw_url
                        }
                        
                        results.append(result)
                        
                        if verbose:
                            print(f"Found: {repo_name}/{file_path}")
                            
                except Exception as e:
                    if verbose:
                        print(f"Error parsing result item: {e}")
            
            # Try to navigate to next page if available
            try:
                next_buttons = driver.find_elements(By.CSS_SELECTOR, ".pagination a[rel='next'], a.next_page")
                if next_buttons:
                    next_buttons[0].click()
                    page_num += 1
                    # Wait for new results to load
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".code-list-item, .code-list .flex-auto"))
                    )
                else:
                    if verbose:
                        print("No next page button found. Ending search.")
                    break
            except Exception as e:
                if verbose:
                    print(f"Error navigating to next page: {e}")
                break
    
    except Exception as e:
        print(f"Error during search: {e}")
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
    
    return results[:max_results] if max_results else results

def download_file(url, file_path, download_dir):
    """Download a file from GitHub without requiring a token."""
    try:
        # Create directory structure
        repo_path = os.path.dirname(file_path)
        save_dir = os.path.join(download_dir, repo_path)
        os.makedirs(save_dir, exist_ok=True)
        
        # Full path to save the file
        save_path = os.path.join(download_dir, file_path)
        
        # Download the file
        response = requests.get(url)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        return save_path
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Search GitHub code and download matched files using Selenium.")
    parser.add_argument("query", nargs="?", help="Search term.")
    parser.add_argument("-l", "--language", help="Programming language filter.")
    parser.add_argument("-u", "--user", help="Search in all repositories of a specific user.")
    parser.add_argument("--repo", help="Search in a specific repository (e.g., username/repo).")
    parser.add_argument("-p", "--path", help="Specify path specifier for filtering.")
    parser.add_argument("-m", "--max-results", type=int, help="Maximum number of results to return.")
    parser.add_argument("-d", "--download", action="store_true", help="Download matched files.")
    parser.add_argument("-dd", "--download-dir", default="codes", help="Directory to save downloaded files.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging.")
    parser.add_argument("-r", "--remark", help="Description of what should be extracted from the downloaded files.")
    parser.add_argument("-o", "--output-file", help="Output file to save the extracted code (default: print to console).")
    parser.add_argument("-e", "--extensions", help="Comma-separated list of file extensions to consider for extraction (e.g., .py,.js)")

    args = parser.parse_args()
    verbose = args.verbose

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
    
    results = search_github_selenium(
        query=args.query,
        user=args.user,
        repo=args.repo,
        language=args.language,
        path=args.path,
        max_results=args.max_results,
        verbose=verbose,
    )

    print(f"Found {len(results)} matching files.")
    
    # Keep track of whether we downloaded any files
    downloaded_any = False
    
    for item in results:
        file_url = item["raw_url"]
        file_path = item["path"]

        if args.download:
            if verbose:
                print(f"Downloading: {file_url}")
            save_path = download_file(file_url, file_path, args.download_dir)
            if save_path:
                downloaded_any = True
        else:
            if verbose:
                print(f"Matched file: {file_path}\n(URL: {file_url})")
            else:
                print(f"Matched file: {file_path}")
    
    # Process extraction with Gemini if remark is provided and files were downloaded
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