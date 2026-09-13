# Quickstart Guide: Basic Google ADK Agent

## Prerequisites
- Docker Desktop running with the `llama3.2` container.
- Dependencies installed via `uv sync`.
- Environment variables configured in `.env`.

## Validation Steps

### 1. Run Automated Tests
Execute the test suite to verify module imports and configuration parsing:
```bash
uv run pytest tests/test_agent.py
```
**Expected Outcome**: All tests pass.

### 2. Start the Agent UI
Start the Google ADK Web interface:
```bash
uv run adk web
```
**Expected Outcome**: The terminal shows a local development server URL (e.g., `http://localhost:8080`).

### 3. Interact with the Agent
1. Open the URL in your browser.
2. Select the `self_improving_agent` from the interface.
3. Type: `Calculate 15% of 200.`
4. Verify the agent responds with `30`.

### 4. Verify Error Handling
1. Stop the Docker container running Llama 3.2.
2. Send a new message in the ADK Web UI.
3. Verify the agent responds with a clear error message regarding the unavailable LLM service, rather than crashing the web server.
