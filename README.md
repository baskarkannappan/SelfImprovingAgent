# Self-Improving Agent - Phase 0

## Prerequisites
- Windows 10 or 11
- Python 3.11+
- uv (Python dependency manager)
- Git
- Docker Desktop

# SelfImprovingAgents

A POC for an autonomous agent using Google ADK 2 and a local Llama 3.2 model via LiteLLM.

## Setup

1. Install Python 3.11+ and `uv`.
2. Run `uv sync` to install dependencies.
3. Ensure Docker Desktop is running and you have pulled `llama3.2` via ollama (or run a local ollama container).
4. Copy `.env.example` to `.env` and verify the settings.

## Running the Agent

You can start the ADK agent using:
```bash
uv run adk web
```
This will run the web app with reloading enabled, listening on port 8000. It provides the standard ADK Developer UI for interacting with the agent.

To view the agent's semantic memory database, run the read-only Streamlit developer UI:
```bash
uv run streamlit run developer_ui/app.py
```
This will open a dashboard in your browser to inspect experiences, vector data, and test semantic search.

## Testing

Run the test suite with pytest:
```bash
uv run pytest
```

```env
LLM_BASE_URL=http://localhost:11434
LLM_MODEL=llama3.2
EMBEDDING_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=nomic-embed-text
DATABASE_PATH=data/agent.db
```

## Environment Validation
Run the comprehensive check script:
```bash
uv run python scripts/check_environment.py
```

## Tests
Run the test suite:
```bash
uv run pytest
```
