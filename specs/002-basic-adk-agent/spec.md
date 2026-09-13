# Feature Specification: Basic Google ADK Agent with ADK Web

**Feature Branch**: `[002-basic-adk-agent]`

**Created**: 2026-09-12

**Status**: Draft

**Input**: User description: "@[c:\MyDrive\ProjectDrive\SelfImprovingAgents\requirements\002-requirement2]"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Interact with the Agent via ADK Web (Priority: P1)

Users can open the ADK Web interface, select the `self_improving_agent`, and ask natural language or mathematical questions, receiving accurate and clear responses.

**Why this priority**: Validates the end-to-end integration of ADK Web, Google ADK 2, LiteLLM, and the local Llama 3.2 model.

**Independent Test**: Can be fully tested by launching `adk web`, selecting the agent, sending a prompt like "Calculate 15% of 200", and verifying the response is correct (e.g., 30).

**Acceptance Scenarios**:

1. **Given** the local LLM and ADK Web are running, **When** the user asks "Calculate 15% of 200.", **Then** the agent responds with "30".
2. **Given** the local LLM and ADK Web are running, **When** the user asks "What is 25 + 37?", **Then** the agent responds with "62".
3. **Given** the local LLM and ADK Web are running, **When** the user asks "Explain what an API is in simple English.", **Then** the agent provides a meaningful explanation.
4. **Given** the user has already asked a question, **When** the user asks a follow-up question, **Then** the agent considers the context of the session to respond.

---

### User Story 2 - Clear Error on LLM Unavailability (Priority: P2)

When the backend Llama 3.2 model is down, users should see a clear and understandable error message in the ADK Web interface instead of a generic system crash.

**Why this priority**: Essential for diagnosing environment issues gracefully without digging into console logs.

**Independent Test**: Shut down the Docker container for Llama 3.2, send a request via ADK Web, and verify a clear error message is returned.

**Acceptance Scenarios**:

1. **Given** the Llama 3.2 Docker container is stopped, **When** the user sends a message in ADK Web, **Then** the system returns an error like "Unable to connect to the configured LLM service. Verify that the Docker Llama 3.2 container is running."
2. **Given** the configured model name is incorrect, **When** the user sends a message, **Then** the system identifies the configured model in the error message and does not fall back to a cloud model.

---

### Edge Cases

- What happens when the model takes too long to respond? (Assume standard timeout).
- How does the system handle an incorrectly formatted `.env` file? (Assume explicit configuration error).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose exactly one root agent named `self_improving_agent`.
- **FR-002**: System MUST use Google ADK 2 and ADK Web as the exclusive user interface.
- **FR-003**: System MUST NOT include any custom CLI, custom chat UI, Blazor UI, React UI, REST endpoint for chat, or separate web applications.
- **FR-004**: System MUST NOT implement long-term memory, self-improvement, SQLite-vec usage, or GraphQLite storage in this phase.
- **FR-005**: System MUST connect to a local Llama 3.2 model using LiteLLM as the integration layer.
- **FR-006**: System MUST load configuration (LLM_BASE_URL, LLM_MODEL, LOG_LEVEL) from environment variables (e.g., `.env`).
- **FR-007**: System MUST implement basic application logging capturing timestamp, agent, model, request lifecycle, success/failure, and error information.
- **FR-008**: System MUST handle LLM unavailability gracefully with a user-friendly error message.
- **FR-009**: System MUST support multiple messages in a single session using ADK Web's built-in session capabilities.
- **FR-010**: System MUST include an automated test suite (`tests/test_agent.py`) verifying agent import, agent creation, configuration loading, basic model requests, and error handling.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Google ADK 2 is installed, and the agent is discoverable and selectable in ADK Web.
- **SC-002**: A user can successfully receive an accurate response from the local Llama 3.2 model via the ADK Web UI.
- **SC-003**: The agent correctly handles mathematical and general natural language queries.
- **SC-004**: The agent retains conversation context within a single ADK Web session.
- **SC-005**: Shutting down the Docker LLM container results in a controlled, human-readable error message in ADK Web instead of a crash.
- **SC-006**: Running `uv run pytest` executes and passes all automated tests.

## Assumptions

- Assumes Google ADK Web handles the chat UI adequately without needing any custom frontend code.
- Assumes the user has the Llama 3.2 model pulled and running locally in Docker Desktop.
- Assumes LiteLLM is compatible with the installed version of Google ADK 2.
