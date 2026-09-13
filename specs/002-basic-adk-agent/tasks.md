# Implementation Tasks: Basic Google ADK Agent

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 [P] Create the `self_improving_agent/` directory and add an empty `__init__.py`.
- [x] T002 [P] Update `.env.example` with `LLM_BASE_URL=http://localhost:11434`, `LLM_MODEL=llama3.2`, and `LOG_LEVEL=INFO`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Implement `self_improving_agent/config.py` to safely load environment variables using `python-dotenv`.

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Interact with the Agent via ADK Web (Priority: P1) → MVP

**Goal**: Users can open the ADK Web interface, select the `self_improving_agent`, and ask natural language or mathematical questions.

**Independent Test**: Can be fully tested by launching `adk web`, selecting the agent, sending a prompt like "Calculate 15% of 200", and verifying the response.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T004 [P] [US1] Create test suite in `tests/test_agent.py` testing module importability and configuration loading.
- [x] T005 [P] [US1] Add a test in `tests/test_agent.py` verifying that the agent can be instantiated successfully.

### Implementation for User Story 1

- [x] T006 [P] [US1] Implement `self_improving_agent/agent.py` by defining the root agent `self_improving_agent` using Google ADK 2.
- [x] T007 [US1] Configure the agent in `agent.py` to use LiteLLM to connect to the local Llama 3.2 model using the configured `config.py` endpoints.
- [x] T008 [US1] Provide the reasoning instructions to the agent in `agent.py`.
- [x] T009 [US1] Export the agent in `self_improving_agent/__init__.py` to ensure it is automatically discovered by `adk web`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently via `adk web`.

---

## Phase 4: User Story 2 - Clear Error on LLM Unavailability (Priority: P2)

**Goal**: When the backend Llama 3.2 model is down, users should see a clear and understandable error message in the ADK Web interface.

**Independent Test**: Shut down the Docker container for Llama 3.2, send a request via ADK Web, and verify a clear error message is returned.

### Tests for User Story 2

- [x] T010 [P] [US2] Add a test in `tests/test_agent.py` that mocks a failed LiteLLM/ADK model response and verifies the agent returns the controlled fallback message.

### Implementation for User Story 2

- [x] T011 [US2] Implement exception handling in the agent's interaction flow to catch LLM connection/timeout errors and return the user-friendly string "Unable to connect to the configured LLM service. Verify that the Docker Llama 3.2 container is running." to the ADK Web UI.

**Checkpoint**: User Stories 1 AND 2 should both work independently.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T012 [P] Implement basic logging (`logging` module) inside `agent.py` to capture request lifecycle and any model connection errors.
- [x] T013 Update `README.md` with instructions on how to start the LLM, run `adk web`, and test the agent.
- [x] T014 Run `uv run pytest` to ensure all tests pass.
- [ ] T015 Run `uv run adk web` to manually perform the manual acceptance tests defined in the spec.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Stories (Phase 3-4)**: Sequentially in priority order.
- **Polish (Final Phase)**: Depends on all user stories.

### Parallel Opportunities

- T004, T005, and T006 can be worked on concurrently since they represent defining the test boundary and the initial agent scaffolding.
