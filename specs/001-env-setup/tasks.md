# Implementation Tasks: Phase 0 — POC Prerequisites and Development Environment

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize Python project with `uv init` for Python 3.11+ in the repository root.
- [x] T002 Update `pyproject.toml` with the required dependencies (`litellm`, `google-adk`, `pytest`, `sqlite-vec`, `graphqlite`) and run `uv sync`.
- [x] T003 [P] Create `.gitignore` to ignore `.venv/`, `.env`, `*.db`, `__pycache__/`, and `.pytest_cache/`.
- [x] T004 [P] Create `.env.example` with template variables `LLM_BASE_URL=http://localhost:11434`, `LLM_MODEL=llama3.2`, `EMBEDDING_BASE_URL=http://localhost:11434`, `EMBEDDING_MODEL=nomic-embed-text`, and `DATABASE_PATH=data/agent.db`.
- [x] T005 [P] Create the directory structure: `scripts/`, `tests/`, and `data/`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Implement configuration loading utility in `scripts/check_environment.py` to gracefully fall back to `.env.example` if `.env` is missing.

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Automated Environment Validation (Priority: P1) → MVP

**Goal**: Validate core tools (Python, uv, Git, Docker) are installed and available.

**Independent Test**: Can be fully tested by running `uv run python scripts/check_environment.py` and `uv run pytest`.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T007 [P] [US1] Create test suite in `tests/test_environment.py` covering tests for `python_environment`, `uv_availability`, `git_availability`, and `docker_availability`.

### Implementation for User Story 1

- [x] T008 [P] [US1] Implement basic structure of `scripts/check_environment.py` with the standard header/footer formatting per the `validation-output.md` contract.
- [x] T009 [US1] Add checks for Python version, uv, Git, and Docker Desktop to `scripts/check_environment.py` and ensure they output `[PASS]` or `[FAIL]`.

**Checkpoint**: At this point, User Story 1 should be fully functional.

---

## Phase 4: User Story 2 - Local Database Setup (Priority: P2)

**Goal**: Validate SQLite with vector and graph extensions.

**Independent Test**: Tests can create vector tables and graph nodes without errors.

### Tests for User Story 2

- [x] T010 [P] [US2] Add `test_sqlite`, `test_sqlite_vec` (vector insertion and similarity search), and `test_graphqlite` (create relationship and query) to `tests/test_environment.py`.

### Implementation for User Story 2

- [x] T011 [US2] Add database checks to `scripts/check_environment.py`: verify SQLite instantiation, sqlite-vec loading, and GraphQLite importing. Print `[PASS]` or `[FAIL]`.

**Checkpoint**: User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 - Local Model Connectivity (Priority: P2)

**Goal**: Validate LiteLLM, Google ADK 2, and local Llama 3.2 endpoints.

**Independent Test**: Tests can send prompts to the LLM and generate an embedding.

### Tests for User Story 3

- [x] T012 [P] [US3] Add `test_llm_connection` (prompt test), `test_embedding_model_available`, `test_adk_import`, and `test_litellm_import` to `tests/test_environment.py`.

### Implementation for User Story 3

- [x] T013 [US3] Add local LLM endpoint connectivity check to `scripts/check_environment.py` (test prompt to `llama3.2`).
- [x] T014 [US3] Add embedding model generation check to `scripts/check_environment.py`.
- [x] T015 [US3] Add Google ADK 2 and LiteLLM import checks to `scripts/check_environment.py`.

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T016 [P] Update `README.md` with prerequisites, Python setup (`uv venv`, `uv sync`), LLM configuration, and commands to run validation and tests.
- [x] T017 Ensure `scripts/check_environment.py` accurately exits with code `0` on success and `1` on failure per the validation contract.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Stories (Phase 3-5)**: Sequentially in priority order, though US2 and US3 can technically be done in parallel once US1 establishes the base script.
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Foundation
- **User Story 2 (P2)**: Integrates into US1 script structure
- **User Story 3 (P2)**: Integrates into US1 script structure

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- Testing framework definitions for each user story can run in parallel before their respective script implementations.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Ensure basic checks work and Docker validation passes/fails correctly.

### Incremental Delivery

1. Add User Story 2 → Validate database extensions.
2. Add User Story 3 → Validate LLM connectivity.
