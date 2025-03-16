# GitHub Code Search CLI (ghcs)

`ghcs` is a command-line interface (CLI) tool for searching code on GitHub and downloading matched files. It allows you to search for code snippets, filter by language, user, repository, and path, and optionally download the matched files. This is effective utility specially when developers are on CLI non ui environment (i.e. on remote desktop).

## Features

- Search GitHub code with various filters (query, user, repository, language, path and so on).
- Download matched files directly from GitHub.
- Easy to use CLI interface.

## Installation

To install `ghcs`, simply use direct pip:
```bash
pip install ghcs
```

or for most updated, directly from Github, using

```bash
pip install git+https://github.com/hissain/ghcs.git
```

## Usage

To use the `ghcs` CLI, you need a GitHub Personal Access Token. You can set it via the `--token` argument or the `GITHUB_TOKEN` environment variable.

### Basic Search

```bash
ghcs 'search_term' --token YOUR_GITHUB_TOKEN
```

```bash
ghcs 'search_term' # when GITHUB_TOKEN is already set in .env
```

### Search with Filters

```bash
ghcs 'search_term' --user 'username' --repo 'username/repo' --language 'python' --path 'llama/train' --token YOUR_GITHUB_TOKEN --max-results MAX_RESULT_COUNT
```

### Download Matched Files

```bash
ghcs 'search_term' --download --token YOUR_GITHUB_TOKEN
```

### Arguments

__Positional:__

* `query:` Search term as an string (required).

__Optional:__

* `-l, --language:` Programming language filter.
* `-u,  --user:` Search in all repositories of a specific user.
* `-r, --repo:` Search in a specific repository (e.g., username/repo).
* `-p, --path:` Specify path specifier for filtering.
* `-t, --token:` GitHub Personal Access Token (or set GITHUB_TOKEN environment variable).
* `-m, --max-result:` Limit the search results to show or download.
* `-d, --download:` Download matched files.
* `-dd, --download-dir:` Download directory for downloading the matched files.
* `-v, --verbose`: Verbose logging for matched files.
* `-h, --help`: Show the help menu and exit.

GITHUB_TOKEN can be generated from https://github.com/settings/tokens

### Example
```bash
ghcs 'def train(' --language 'python' --user 'hissain' --path 'llama/train' --download --token YOUR_GITHUB_TOKEN --max-results 5

OR

ghcs 'def train(' -l 'python' -p 'llama/train' -d -m 10
```

```bash
ghcs "def train()" --path llm --max-results 3 --download
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author

Md. Sazzad Hissain Khan

* Email: hissain.khan@gmail.com
* GitHub: hissain

Feel free to modify the content as needed.
