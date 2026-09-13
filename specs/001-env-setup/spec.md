# Feature Specification: Phase 0 — POC Prerequisites and Development Environment

**Feature Branch**: `001-env-setup`

**Created**: 2026-09-12

**Status**: Draft

**Input**: User description: "/speckit-specify @[c:\MyDrive\ProjectDrive\SelfImprovingAgents\requirements\001-requirements]"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automated Environment Validation (Priority: P1)

As a developer, I want an automated script to validate my development environment so that I know all prerequisites are correctly installed and configured before starting Phase 1.

**Why this priority**: Without a validated environment, the subsequent agent implementation phases will encounter infrastructure issues. Validating the baseline is the primary goal of Phase 0.

**Independent Test**: Can be fully tested by running `uv run python scripts/check_environment.py` and receiving a PASS/FAIL report for all components.

**Acceptance Scenarios**:

1. **Given** a fresh project clone, **When** I run the validation script, **Then** it tests Python, uv, Git, Docker, Llama 3.2, SQLite, sqlite-vec, GraphQLite, ADK 2, and LiteLLM.
2. **Given** a missing or stopped dependency (e.g., LLM container), **When** I run the validation script, **Then** it clearly reports [FAIL] with an actionable error message.

---

### User Story 2 - Local Database Setup (Priority: P2)

As a developer, I want the project to use SQLite with vector and graph extensions so that the agent has memory capabilities without requiring external databases like PostgreSQL or Neo4j.

**Why this priority**: The agent's memory relies heavily on SQLite extensions, but the infrastructure must be proven to load correctly on Windows before implementation.

**Independent Test**: Can be tested independently by running `pytest` to execute tests that create a vector table, insert embeddings, and query a graph relationship.

**Acceptance Scenarios**:

1. **Given** a local SQLite database, **When** I perform a similarity search using `sqlite-vec`, **Then** it retrieves the nearest vector successfully.
2. **Given** a local SQLite database, **When** I use `GraphQLite` to define a relationship, **Then** I can query nodes and their related edges.

---

### User Story 3 - Local LLM Connectivity (Priority: P2)

As a developer, I want to confirm that LiteLLM and Google ADK can communicate with a local Docker-based Llama 3.2 model so that no cloud API keys are required.

**Why this priority**: Local offline reasoning is a core requirement, and ensuring the connection works is critical.

**Independent Test**: The validation script sends a prompt and successfully receives a response from `llama3.2`.

**Acceptance Scenarios**:

1. **Given** the Llama 3.2 container is running, **When** the script sends "Calculate 15% of 200", **Then** the LLM returns the correct result.
2. **Given** the embedding model endpoint, **When** the script requests an embedding, **Then** it receives a valid numeric vector.

### Edge Cases

- What happens when Docker Desktop is not running? The validation script must fail gracefully with a clear message.
- How does system handle missing environment variables in `.env`? The application should fall back to `.env.example` or raise configuration errors.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support Python 3.11+ using `uv` for dependency and virtual environment management.
- **FR-002**: System MUST NOT rely on globally installed Python packages.
- **FR-003**: System MUST verify the availability of Git and ensure a proper `.gitignore` is present.
- **FR-004**: System MUST communicate with a local Docker-based Llama 3.2 service and an embedding service without requiring local Ollama installations on the host OS.
- **FR-005**: System MUST use SQLite as the primary database, integrating `sqlite-vec` for vector operations and `GraphQLite` for graph operations.
- **FR-006**: System MUST use LiteLLM to interface between Google ADK 2 and the local Llama service.
- **FR-007**: System MUST provide an automated environment check script (`scripts/check_environment.py`) that outputs the status of all dependencies.
- **FR-008**: System MUST provide automated tests (`tests/test_environment.py`) via `pytest` to validate SQLite extensions and model connectivity.
- **FR-009**: System MUST read all configuration (LLM endpoints, models, DB paths) from an external `.env` file, providing a `.env.example`.

### Key Entities

- **Configuration**: Environment variables (e.g., `LLM_BASE_URL`, `DATABASE_PATH`).
- **Dependencies**: The required packages and tools (Python, uv, Docker, ADK, etc.).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The command `uv run python scripts/check_environment.py` executes successfully and reports PASS for all 13 dependencies.
- **SC-002**: The command `uv run pytest` executes successfully, passing all 9 environment tests.
- **SC-003**: The environment validation successfully generates a numeric embedding and performs a vector similarity search on a temporary table.
- **SC-004**: The environment validation successfully creates and queries a GraphQLite relationship (e.g., Task -> USES -> Strategy).
- **SC-005**: No agent reasoning, critic, learner, or self-improvement logic is implemented (strictly environment setup).

## Assumptions

- Development is performed on Windows 10 or Windows 11.
- Docker Desktop is installed, running, and hosts the `docker.io/llama3.2` image before the script runs.
- `nomic-embed-text` (or equivalent) is accessible for embeddings.
