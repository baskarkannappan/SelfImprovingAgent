# Implementation Tasks: Self-Improvement Learning Loop

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create `self_improving_agent/evaluator.py`, `self_improving_agent/learner.py`, and `self_improving_agent/graph.py` files.
- [x] T002 [P] Create `developer_ui/pages/evaluations.py` and `developer_ui/pages/lessons.py`.
- [x] T003 [P] Create test files: `tests/test_evaluator.py`, `tests/test_learner.py`, `tests/test_graph.py`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Setup database schema migrations for `Evaluation` and `Lesson` tables in `self_improving_agent/memory.py`.
- [x] T005 [P] Setup GraphQLite connection singleton and basic edge insertion methods in `self_improving_agent/graph.py`.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Evaluate Answers (Priority: P1) ⭐ MVP

**Goal**: The system needs to evaluate its own answers automatically after providing a response to the user.

**Independent Test**: Can be tested by having the system output an evaluation record with correct, quality, confidence, and reason fields after answering a prompt.

### Implementation for User Story 1

- [x] T006 [P] [US1] Implement `Evaluator` class in `self_improving_agent/evaluator.py` using `LiteLLM` to evaluate subjective answers.
- [x] T007 [P] [US1] Add `store_evaluation` method in `self_improving_agent/memory.py` ensuring `correct` is strictly limited to `true`, `false`, or `unknown`.
- [x] T008 [US1] Integrate `Evaluator` execution into the `after_agent_hook` in `self_improving_agent/agent.py` without blocking the main answer.
- [x] T009 [US1] Write automated test `test_evaluate_subjective_answer` in `tests/test_evaluator.py`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Extract Lessons (Priority: P1)

**Goal**: When the agent evaluates an answer and spots an opportunity for improvement or a reusable rule, it extracts a generic lesson.

**Independent Test**: Can be tested by providing an evaluation of an incorrect answer and checking if a valid lesson record (with text, type, confidence) is generated and stored in SQLite.

### Implementation for User Story 2

- [x] T010 [P] [US2] Implement `Learner` class in `self_improving_agent/learner.py` using `LiteLLM` to extract lessons.
- [x] T011 [P] [US2] Add `store_lesson` method in `self_improving_agent/memory.py`.
- [x] T012 [P] [US2] Generate lesson embedding using `nomic-embed-text` and save to sqlite-vec in `store_lesson` within `self_improving_agent/memory.py`.
- [x] T013 [US2] Integrate `Learner` into the `after_agent_hook` in `self_improving_agent/agent.py` after the evaluator logic.
- [x] T014 [US2] Write automated test `test_extract_lesson_from_failure` in `tests/test_learner.py`.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 4 - Retrieve Lessons for Context (Priority: P1)

**Goal**: When a new user request arrives, the system retrieves semantically relevant past lessons and injects them into the Main Agent's context.

**Independent Test**: Can be tested by asking a question similar to a past failure and observing if the relevant lesson is included in the LLM context.

### Implementation for User Story 4

- [x] T015 [P] [US4] Add semantic search method `search_lessons` in `self_improving_agent/memory.py`.
- [x] T016 [US4] Update `before_agent_hook` in `self_improving_agent/agent.py` to retrieve lessons and inject into a "RELEVANT LESSONS" prompt block.

**Checkpoint**: Core learning loop is now complete.

---

## Phase 6: User Story 3 - Graph Connections (Priority: P2)

**Goal**: The developer needs to see how experiences, evaluations, and lessons relate to each other.

**Independent Test**: Can be tested by querying the graph to find the Lesson produced by a specific Evaluation of a specific Experience.

### Implementation for User Story 3

- [x] T017 [P] [US3] Implement `link_experience_to_evaluation` and `link_evaluation_to_lesson` methods in `self_improving_agent/graph.py` using GraphQLite `PRODUCES_LESSON` and `EVALUATED_BY` edges.
- [x] T018 [US3] Add graph connection calls within `after_agent_hook` in `self_improving_agent/agent.py`.
- [x] T019 [US3] Write automated test `test_graph_relationships` in `tests/test_graph.py`.

**Checkpoint**: Graph tracking functional.

---

## Phase 7: User Story 5 - Developer UI Traceability (Priority: P3)

**Goal**: The developer needs to visualize evaluations, lessons, learning traces, and graph relationships in Streamlit.

**Independent Test**: Can be tested by opening the Streamlit app and viewing the Evaluations and Lessons tables, and checking the graph view for connections.

### Implementation for User Story 5

- [x] T020 [US5] Build the `/evaluations` page in `developer_ui/pages/evaluations.py` to list recent evaluations.
- [x] T021 [US5] Build the `/lessons` page in `developer_ui/pages/lessons.py` to list extracted lessons.
- [x] T022 [US5] Add cross-links in the UI so clicking on an Evaluation reveals the extracted Lesson, matching the graph relationships.

**Checkpoint**: UI observability complete.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T023 Run `pytest` to verify all new tests pass.
- [x] T024 Run `uv run python developer_ui/app.py` or start the streamlit UI to ensure it launches correctly without errors. Learner is cleanly caught and logged without aborting the app in `self_improving_agent/agent.py`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 (P1), User Story 2 (P1), and User Story 4 (P1) should ideally be executed sequentially or parallelized by different developers.
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### Parallel Opportunities

- T001, T002, T003 can be executed in parallel.
- Evaluator logic (T006, T007) can be built in parallel to Learner logic (T010, T011, T012).
- Streamlit UI pages (T020, T021) can be developed independently of the core agent loop once the database schema is defined.

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Evaluate Answers)
4. **STOP and VALIDATE**: Test User Story 1 independently by seeing an evaluation log.

### Incremental Delivery

1. Complete Setup + Foundational -> Foundation ready
2. Add User Story 1 -> Test independently -> Evaluation loop working
3. Add User Story 2 -> Test independently -> Lesson extraction working
4. Add User Story 4 -> Test independently -> Core feedback loop closed
5. Add User Story 3 (Graph) and User Story 5 (UI Traceability) -> Final observability delivery.
