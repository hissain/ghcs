# GitHub Code Search CLI (ghcs) - With Semantic Code Refinement

`ghcs` is a powerful command-line interface (CLI) tool for searching code on GitHub and downloading matched files. It allows you to search for code snippets using various filters such as language, user, repository, and path. Additionally, `ghcs` enables AI-powered code manipulation and refinement using large language models (LLMs) like Gemini. This makes it especially useful for developers working in CLI-based environments without a graphical user interface (e.g., remote servers).

## Features

- Search GitHub repositories for code using advanced filters (query, user, repository, language, path, etc.).
- Download matched files directly from GitHub.
- Extract, modify, enhance, and refine code using AI-powered transformations with models like Gemini.
- User-friendly CLI interface designed for seamless integration into developer workflows.

## Installation

To install `ghcs`, use pip:

```bash
pip install ghcs
```

For the latest updates, install directly from GitHub:

```bash
pip install git+https://github.com/hissain/ghcs.git
```

## Usage

To use `ghcs`, you need a GitHub Personal Access Token, which can be set using the `--token` argument or the `GITHUB_TOKEN` environment variable. For AI-powered code manipulation with `--remark`, you must set the `GEMINI_API_KEY` in your environment.

### Basic Search

```bash
ghcs 'search_term' --token YOUR_GITHUB_TOKEN
```

```bash
ghcs 'search_term' # When GITHUB_TOKEN is already set in .env
```

### Search with Filters

```bash
ghcs 'search_term' --user 'username' --repo 'username/repo' --language 'python' --path 'llama/train' --token YOUR_GITHUB_TOKEN --max-results MAX_RESULT_COUNT
```

### Download Matched Files

```bash
ghcs 'search_term' --download --token YOUR_GITHUB_TOKEN
```

### AI-Powered Code Extraction & Refinement

To extract specific code sections or apply AI-driven transformations on downloaded files:

- Use `--remark` to specify semantic modifications (requires `--download`).
- The refined code can be printed to the console or saved using `--output-file`.

__Example:__

```bash
ghcs "LoRA def train()" --user hissain --download --remark "Extract the training function for LoRA with proper imports" --output-file extracted_code.py --verbose
```

> **Note:** The `GEMINI_API_KEY` must be set in your environment variables or `.env` file to enable the `--remark` feature.

## CLI Arguments

### Positional Arguments

- **query**: Search term as a string (required).

### Optional Arguments

- `-l, --language` : Filter by programming language.
- `-u, --user` : Search within all repositories of a specific user.
- `-r, --repo` : Search within a specific repository (e.g., username/repo).
- `-p, --path` : Restrict search to a specific file path.
- `-t, --token` : GitHub Personal Access Token (or set `GITHUB_TOKEN` environment variable).
- `-m, --max-result` : Limit the number of search results.
- `-d, --download` : Download matched files.
- `-dd, --download-dir` : Specify the directory for downloaded files.
- `-v, --verbose` : Enable verbose logging.
- `-r, --remark` : AI instruction for refining downloaded files.
- `-o, --output-file` : Output file to save refined code (default: print to console).
- `-e, --extensions` : Specify file extensions to consider (e.g., `.py,.js`).
- `-h, --help` : Show help menu and exit.

### Example Commands

```bash
ghcs 'def train(' --language 'python' --user 'hissain' --path 'llama/train' --download --token YOUR_GITHUB_TOKEN --max-results 5
```

```bash
ghcs 'def train(' -l 'python' -p 'llama/train' -d -m 10
```

```bash
ghcs "def train()" --path llm --max-results 3 --download
```

With AI-powered refinement:

```bash
ghcs "def train LoRA" --path llm --download --remark "Extract only the forward pass function" --output-file forward_pass.py --max-results 5
```

## API Keys

- **GitHub Token:** Generate a personal access token at [GitHub Tokens](https://github.com/settings/tokens)
- **Gemini API Key:** Obtain from [Google AI Studio](https://aistudio.google.com/apikey)

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

**Md. Sazzad Hissain Khan**

- **Email:** hissain.khan@gmail.com
- **GitHub:** [hissain](https://github.com/hissain)

Feel free to modify and enhance this project as needed!

