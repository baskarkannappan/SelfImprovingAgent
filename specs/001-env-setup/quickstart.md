# Quickstart: Validation Guide

This document describes how to execute the end-to-end validation for the Phase 0 environment setup.

## Prerequisites

1. Ensure **Docker Desktop** is installed and running on your Windows host.
2. Ensure you have the `llama3.2` and `nomic-embed-text` models pulled in your Docker container (e.g., via Ollama running in Docker).
3. Ensure **uv** is installed globally.
4. Clone the repository and navigate to the project root.

## Setup Steps

1. **Install Dependencies**
   ```bash
   uv sync
   ```

2. **Configure Environment**
   Copy the example environment file and adjust if necessary:
   ```bash
   cp .env.example .env
   ```
   *Note: Ensure `LLM_BASE_URL` matches your local Docker port mappings (e.g., `http://localhost:11434`).*

## Validation Execution

Run the environment validation script:
```bash
uv run python scripts/check_environment.py
```

**Expected Outcome**:
The script should output `[PASS]` for all components and exit with code `0`. Refer to the [Validation Output Contract](contracts/validation-output.md) for the exact format.

## Automated Test Execution

Run the `pytest` test suite to perform deeper validation of SQLite extensions and LLM connectivity:
```bash
uv run pytest
```

**Expected Outcome**:
All tests should pass. If Docker is not running or the LLM is inaccessible, tests will fail with clear network or connection errors.
