# Implementation Tasks: Semantic Memory

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create `self_improving_agent/memory` package structure and `developer_ui` directory.
- [x] T002 Add `sqlite-vec` and `streamlit` to project dependencies.
- [x] T003 Update `.env.example` and `config.py` with `MEMORY_TOP_K`, `MEMORY_SIMILARITY_THRESHOLD`, `EMBEDDING_MODEL`, `DATABASE_PATH`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Setup `self_improving_agent/memory/database.py` with SQLite connection and `sqlite-vec` initialization.
- [x] T005 Implement `initialize_database()` in `database.py` to create `experiences` and `experience_vectors` tables on startup.
- [x] T006 Implement `self_improving_agent/memory/embeddings.py` with `generate_embedding(text)` using Ollama `nomic-embed-text`.
- [x] T007 Implement unit tests in `tests/test_database.py` for database initialization and `sqlite-vec` loading.
- [x] T008 Implement unit tests in `tests/test_embeddings.py` verifying numeric vector generation.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and Retrieve Persistent Memories (Priority: P1) ⭐ MVP

**Goal**: Store past interactions and retrieve them via semantic search to build LLM context.

**Independent Test**: Can be fully tested by submitting a request in ADK Web, restarting the application, submitting a similar request, and verifying that the past experience was successfully retrieved and used as context.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T009 [P] [US1] Integration test for memory retrieval in `tests/test_retrieval.py`.

### Implementation for User Story 1

- [x] T010 [P] [US1] Implement `store_experience()` in `self_improving_agent/memory/memory.py` to save task, response, and embedding.
- [x] T011 [P] [US1] Implement `retrieve_similar_experiences(query, top_k, threshold)` in `self_improving_agent/memory/retrieval.py` using `sqlite-vec` vec_distance_cosine.
- [x] T012 [US1] Implement `build_memory_context(experiences)` in `self_improving_agent/memory/retrieval.py`.
- [x] T013 [US1] Integrate memory retrieval and storage into `self_improving_agent/agent.py` before and after Llama 3.2 execution.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Memory Isolation and Fallback (Priority: P2)

**Goal**: Ensure the agent functions normally when memory is unavailable or irrelevant.

**Independent Test**: Can be tested by asking completely unrelated questions and ensuring the agent still functions normally.

### Tests for User Story 2

- [x] T014 [P] [US2] Add unit test in `tests/test_retrieval.py` verifying fallback behavior with empty database.

### Implementation for User Story 2

- [x] T015 [US2] Update `self_improving_agent/agent.py` to catch database/embedding exceptions and gracefully bypass memory insertion.
- [x] T016 [US2] Update the agent instruction prompt in `agent.py` to explicitly prioritize the current request over conflicting memory context.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Developer Visualization (Priority: P2)

**Goal**: A read-only Streamlit application to inspect the SQLite database, view experiences, and test semantic search.

**Independent Test**: Can be fully tested by running `streamlit run developer_ui/app.py` and navigating through the various data views and semantic search tools.

### Implementation for User Story 3

- [x] T017 [P] [US3] Create `developer_ui/app.py` Streamlit entry point.
- [x] T018 [US3] Implement Database Overview and Experiences View in Streamlit (read-only SQLite queries).
- [x] T019 [US3] Implement Vector Data view in Streamlit.
- [x] T020 [US3] Implement Semantic Search manual testing UI in Streamlit reusing `retrieval.py` and `embeddings.py` logic.

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T021 [P] Update `README.md` with instructions for starting `adk web` and `streamlit`.
- [x] T022 Code cleanup and formatting using `ruff` or `black`.
- [x] T023 Run `quickstart.md` validation scenarios.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2)
- **User Story 2 (P2)**: Can start after User Story 1 (modifies `agent.py`)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2). Integrates with US1 components.

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel
- Tests for a user story marked [P] can run in parallel
