# GitHub Code Search CLI (ghs)

`ghs` is a command-line interface (CLI) tool for searching code on GitHub and downloading matched files. It allows you to search for code snippets, filter by language, user, repository, and path, and optionally download the matched files.

## Features

- Search GitHub code with various filters (query, user, repository, language, path).
- Download matched files directly from GitHub.
- Easy to use CLI interface.

## Installation

To install `ghs`, clone the repository and install the dependencies:

```sh
git clone https://github.com/hissain/ghs.git
cd ghs
pip install -r requirements.txt
```

## Usage

To use the `ghs` CLI, you need a GitHub Personal Access Token. You can set it via the `--token` argument or the `GITHUB_TOKEN` environment variable.

### Basic Search

```bash
ghs --query 'search_term' --token YOUR_GITHUB_TOKEN
```

### Search with Filters

```bash
ghs --query 'search_term' --user 'username' --repo 'username/repo' --language 'python' --path '*.py' --token YOUR_GITHUB_TOKEN
```

### Download Matched Files

```bash
ghs --query 'search_term' --download --token YOUR_GITHUB_TOKEN
```

### Arguments

* `--query:` Search term (required).
* `--language:` Programming language filter.
* `--user:` Search in all repositories of a specific user.
* `--repo:` Search in a specific repository (e.g., username/repo).
* `--path:` Specify path specifier for filtering.
* `--token:` GitHub Personal Access Token (or set GITHUB_TOKEN environment variable).
* `--download:` Download matched files.

###Example
```bash
ghs --query 'def main' --language 'python' --user 'hissain' --path '*.py' --download --token YOUR_GITHUB_TOKEN
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author

Md. Sazzad Hissain Khan

* Email: hissain.khan@gmail.com
* GitHub: hissain

Feel free to modify the content as needed.