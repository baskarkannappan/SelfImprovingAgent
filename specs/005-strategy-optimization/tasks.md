# Tasks: Strategy Optimization

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create `strategy` module directory structure in `self_improving_agent/strategy/`
- [X] T002 [P] Create empty `developer_ui/pages/1_strategy_registry.py`, `2_strategy_performance.py`, and `3_strategy_preferences.py` files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Update SQLite schema in `self_improving_agent/memory/database.py` with `strategies`, `strategy_executions`, `strategy_performance`, and `strategy_preferences` tables
- [X] T004 [P] Add Strategy entities and relationships to the GraphQLite schema in `self_improving_agent/memory/memory.py`
- [X] T005 [P] Add Strategy-related configurations (e.g., `STRATEGY_MIN_SAMPLES`, `STRATEGY_EXPLORATION_RATE`) to `self_improving_agent/config.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Cold Start Exploration (Priority: P1) 🚀 MVP

**Goal**: System recognizes lack of data for a new task category, explores an available strategy, executes, evaluates, and stores performance.

**Independent Test**: Trigger a calculation task and verify in SQLite that a random strategy was chosen and its execution and performance were saved.

### Implementation for User Story 1

- [X] T006 [P] [US1] Create `self_improving_agent/strategy/registry.py` to define and load the predefined strategy dictionary (`direct_calculation`, `verify_calculation`, etc.)
- [X] T007 [P] [US1] Create `self_improving_agent/strategy/classifier.py` to determine the task type (e.g., `calculation`)
- [X] T008 [P] [US1] Create `self_improving_agent/strategy/selector.py` with the exploration fallback logic (e.g., random choice when no history exists)
- [X] T009 [US1] Create `self_improving_agent/strategy/executor.py` to route the task to the selected strategy steps and record `strategy_executions`
- [X] T010 [US1] Update `self_improving_agent/agent.py` to integrate the classifier, selector, and executor into the main agent workflow
- [X] T011 [US1] Update `self_improving_agent/evaluation/evaluator.py` to calculate strategy effectiveness alongside answer quality and persist to `strategy_performance`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Adaptive Exploitation (Priority: P1)

**Goal**: System identifies and selects the best-performing strategy based on historical data.

**Independent Test**: Populate historical records and ensure the selector correctly picks the strategy with the highest score (skipping exploration).

### Implementation for User Story 2

- [X] T012 [P] [US2] Create SQL queries to aggregate performance data per strategy in `self_improving_agent/memory/database.py`
- [X] T013 [P] [US2] Update `selector.py` to compute the deterministic score (success, quality, confidence) and determine the `strategy_preferences`
- [X] T014 [US2] Implement the `STRATEGY_MIN_SAMPLES` logic in `selector.py` to prevent premature optimization
- [X] T015 [US2] Persist the calculated preferences into the `strategy_preferences` table when evaluated

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Developer Testing Commands (Priority: P2)

**Goal**: Developer slash commands in ADK Web for testing and visualization in Streamlit.

**Independent Test**: Type `/test-strategy comparison` and verify the output stats; check Streamlit for data visibility.

### Implementation for User Story 3

- [X] T016 [P] [US3] Add command intercept logic in `self_improving_agent/agent.py` (`handle_user_message`) for `/test-strategy`
- [X] T017 [US3] Implement the simulation logic for `/test-strategy comparison` that outputs aggregated statistics directly to the chat
- [X] T018 [P] [US3] Implement `developer_ui/pages/1_strategy_registry.py` to list available strategies from DB
- [X] T019 [P] [US3] Implement `developer_ui/pages/2_strategy_performance.py` to show execution history and stats
- [X] T020 [P] [US3] Implement `developer_ui/pages/3_strategy_preferences.py` to display the calculated best strategies

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T021 [P] Update `developer_ui/app.py` to include the new pages in the navigation sidebar
- [X] T022 [P] Create unit tests for deterministic scoring in `tests/test_strategy_scoring.py`
- [X] T023 [P] Create unit tests for strategy selection in `tests/test_strategy_selection.py`
- [X] T024 Run `quickstart.md` validation end-to-end to ensure all flows work seamlessly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US1 must be completed first to establish the execution and evaluation pipeline.
  - US2 builds on US1 by adding historical scoring.
  - US3 can be done in parallel with US2 after US1 is completed.
- **Polish (Final Phase)**: Depends on all user stories being complete

### Parallel Opportunities

- Creating the UI files (T002, T018-T020, T021) can run entirely in parallel with backend tasks once the database tables are defined.
- Within US1, the `registry.py`, `classifier.py`, and `selector.py` modules can be built in parallel.
- Unit tests can be written in parallel by different developers.

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 & 2 (Database & GraphQLite).
2. Complete Phase 3 (Exploration, Execution, Evaluation).
3. **STOP and VALIDATE**: Test User Story 1 independently to ensure new tasks are explored and saved properly without breaking the existing AI flow.
