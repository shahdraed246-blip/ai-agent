# AI Agent

A toy command-line coding agent inspired by tools like Claude Code and Cursor. It accepts a natural-language task, reasons about which tools to use, and executes them autonomously — reading files, writing files, and running Python code — until the task is done or it gives up.

Built as part of [Boot.dev](https://boot.dev)'s "Build an AI Agent" course.

## Features

- Natural-language task input from the CLI
- Powered by free LLMs via OpenRouter (OpenAI-compatible API)
- Agentic loop: the model plans, calls tools, observes results, and iterates
- Four sandboxed tools, all restricted to a working directory: get_files_info, get_file_content, write_file, run_python_file
- Path validation on every tool call — the agent can never read, write, or execute anything outside its configured working directory

## Example

```sh
$ uv run main.py "list the files in the current directory, then read main.py and tell me what it does"
 - Calling function: get_files_info
 - Calling function: get_file_content
Final response:
main.py is the entry point for a calculator CLI app. It evaluates a math
expression passed as a command-line argument and prints the result as
formatted JSON.
```

## Setup

Requirements: Python 3.10+, uv, an OpenRouter account.

```sh
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
uv sync
```

Create a .env file in the project root with:

```
OPENROUTER_API_KEY='your_api_key_here'
```

## Usage

```sh
uv run main.py "your task here"
uv run main.py "your task here" --verbose
```

The agent operates only inside the calculator/ directory — a sample Python CLI app bundled in this repo for it to read, debug, and modify.

## Project Structure

```
├── calculator/          # Sample project the agent operates on
│   ├── main.py
│   ├── pkg/
│   └── tests.py
├── functions/            # Agent tools (all path-validated against escape attempts)
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── call_function.py       # Dispatches model tool-call requests to the real functions
├── config.py               # Shared constants (e.g. max file-read length)
├── prompts.py               # System prompt defining the agent's behavior
└── main.py                   # Entry point: CLI args, agent loop, model calls
```

## Safety Notes

This is a learning project, not a production-ready tool:
- Every file operation is validated to stay within the configured working directory — confirmed by testing that requests like reading /etc/passwd are correctly rejected
- run_python_file has a 30-second execution timeout
- The agent loop is capped at 20 iterations to prevent runaway token usage
- If the model requests a function that doesn't exist, the agent reports the error back to the model instead of crashing — the model can then self-correct

That said, giving an LLM write and execute access to a filesystem always carries risk. Don't point this at anything you're not prepared to lose, and don't use it unsupervised on real projects.

## Built With

- Python 3.12, uv
- OpenAI Python SDK (pointed at OpenRouter)
- OpenRouter for free LLM access
