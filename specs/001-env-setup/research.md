# Research: Phase 0 — POC Prerequisites and Development Environment

## Overview

The technical stack for the POC is explicitly defined by the requirements. This research document consolidates the rationale for these choices and ensures there are no unknowns before proceeding to implementation.

## Decisions

### Dependency Management
- **Decision**: `uv`
- **Rationale**: Provides extremely fast Python dependency resolution and virtual environment management without relying on global pip installations.
- **Alternatives considered**: Poetry, pipenv (rejected due to speed and complexity compared to uv).

### Local LLM Runtime
- **Decision**: `docker.io/llama3.2` via Docker Desktop
- **Rationale**: Ensures a repeatable, cross-platform local LLM execution without requiring host OS installations of Ollama.
- **Alternatives considered**: Ollama for Windows (rejected to keep dependencies containerized).

### Agent Orchestration
- **Decision**: Google ADK 2 + LiteLLM
- **Rationale**: ADK 2 provides the orchestrator pattern. LiteLLM provides a unified interface to proxy ADK's requests to the local Llama 3.2 Docker instance.
- **Alternatives considered**: LangChain, direct API calls (rejected as ADK 2 is the specified orchestrator).

### Memory & Graph Storage
- **Decision**: SQLite + sqlite-vec + GraphQLite
- **Rationale**: Keeps the entire memory subsystem localized to a single file database (`data/agent.db`), removing the need for heavy external services.
- **Alternatives considered**: PostgreSQL/pgvector, Neo4j (rejected as they violate the local-only lightweight requirement).

## Unknowns Resolved
All technical choices are clearly defined. No further research required.
