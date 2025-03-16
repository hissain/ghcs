# GitHub Code Search CLI (ghcs)

`ghcs` is a command-line interface (CLI) tool for searching code on GitHub and downloading matched files. It allows you to search for code snippets, filter by language, user, repository, and path, and optionally download the matched files. This is effective utility specially when developers are on CLI non ui environment (i.e. on remote desktop).

## Features

- Search GitHub code with various filters (query, user, repository, language, path).
- Download matched files directly from GitHub.
- Easy to use CLI interface.

## Installation

To install `ghcs`, simply use direct pip:
```bash
pip install gscs
```

or for most updated, directly from Github, using

```bash
pip install git+https://github.com/hissain/ghcs.git
```

## Usage

To use the `ghcs` CLI, you need a GitHub Personal Access Token. You can set it via the `--token` argument or the `GITHUB_TOKEN` environment variable.

### Basic Search

```bash
ghcs --query 'search_term' --token YOUR_GITHUB_TOKEN
```

### Search with Filters

```bash
ghcs --query 'search_term' --user 'username' --repo 'username/repo' --language 'python' --path '*.py' --token YOUR_GITHUB_TOKEN --max-results MAX_RESULT_COUNT
```

### Download Matched Files

```bash
ghcs --query 'search_term' --download --token YOUR_GITHUB_TOKEN
```

### Arguments

* `--query:` Search term (required).
* `--language:` Programming language filter.
* `--user:` Search in all repositories of a specific user.
* `--repo:` Search in a specific repository (e.g., username/repo).
* `--path:` Specify path specifier for filtering.
* `--token:` GitHub Personal Access Token (or set GITHUB_TOKEN environment variable).
* `--max-result:` Limit the search results to show or download.
* `--download:` Download matched files.
* `--download-dir:` Download directory for downloading the matched files.

GITHUB_TOKEN can be generated from https://github.com/settings/tokens

### Example
```bash
ghcs --query 'def main' --language 'python' --user 'hissain' --path '*.py' --download --token YOUR_GITHUB_TOKEN --max-results 5
```

```bash
ghcs --query "def main()" --user hissain --max-results 3 --download
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author

Md. Sazzad Hissain Khan

* Email: hissain.khan@gmail.com
* GitHub: hissain

Feel free to modify the content as needed.
