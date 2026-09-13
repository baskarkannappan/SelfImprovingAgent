# Research Notes: Basic Google ADK Agent

## 1. Google ADK 2 + LiteLLM Integration

**Decision**: The agent will define its model configuration to bridge through LiteLLM's OpenAI-compatible API layer to reach the local Llama 3.2 instance.

**Rationale**: Google ADK 2 agents require a model interface. LiteLLM acts as a universal adapter. By configuring the agent to use LiteLLM, we can seamlessly point it to `ollama/llama3.2` running at the local Docker endpoint (`http://localhost:11434`) without writing custom HTTP clients.

**Alternatives Considered**: 
- Native HTTP requests to Ollama API: Rejected as it bypasses ADK's native model integration features and complicates conversation handling.

## 2. Directory Structure and Agent Discovery

**Decision**: The agent logic will reside in `self_improving_agent/agent.py` at the repository root.

**Rationale**: `adk web` dynamically discovers agents in the current working directory. By placing the agent package at the root, running `adk web` from the project root will automatically find and load `self_improving_agent`.

**Alternatives Considered**:
- Creating a deeply nested `src/` directory: Rejected because it may require additional `PYTHONPATH` manipulation or ADK configuration to ensure discovery.

## 3. Configuration Management

**Decision**: Use `python-dotenv` within `self_improving_agent/config.py` to load `.env` with a fallback to `.env.example`.

**Rationale**: Keeps credentials and endpoints out of source code while providing a smooth developer experience out of the box.

**Alternatives Considered**:
- Hardcoding values: Rejected as it violates the specification requirements.
