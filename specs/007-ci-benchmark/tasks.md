# Implementation Tasks: Continuous Improvement Validation

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create `benchmark` directory inside `self_improving_agent/`
- [x] T002 [P] Create `self_improving_agent/benchmark/__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Ensure database connection logic supports switching `config.DB_PATH` for isolation
- [x] T004 Create `BenchmarkReport` and `TaskResult` JSON schema definitions in `self_improving_agent/benchmark/metrics.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Benchmark Execution (Priority: P1) 🎯 MVP

**Goal**: The system must be able to execute a benchmark run against the multi-agent system in both baseline and learning modes.

**Independent Test**: Can be tested by running the benchmark command and observing the output of results.

### Implementation for User Story 1

- [x] T005 [US1] Create benchmark tasks definition file in `self_improving_agent/benchmark/tasks.py` with 10+ standard tasks
- [x] T006 [US1] Implement `runner.py` in `self_improving_agent/benchmark/` to accept `--mode` (baseline vs post_learning)
- [x] T007 [US1] Implement logic in `runner.py` to point to a temporary/isolated database when mode is `baseline`
- [x] T008 [US1] Implement execution loop in `runner.py` to run all tasks through the agent workflow
- [x] T009 [US1] Implement metric collection in `runner.py` to aggregate `correct`, `quality`, and `duration_ms` into the `BenchmarkReport`
- [x] T010 [US1] Output `BenchmarkReport` as JSON to a local `reports/` directory

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Validation Dashboard (Priority: P2)

**Goal**: Developers can view a "Continuous Improvement" dashboard in Streamlit to compare baseline and post-learning runs.

**Independent Test**: Can be tested by opening Streamlit and checking the new dashboard page for comparison metrics.

### Implementation for User Story 2

- [x] T011 [US2] Create `9_continuous_improvement.py` in `developer_ui/pages/`
- [x] T012 [US2] Implement JSON report loading logic to read saved benchmark reports
- [x] T013 [US2] Create side-by-side metric components for Correctness, Quality, Strategy, and Latency
- [x] T014 [US2] Display a detailed breakdown table of Task Results comparing "Before" and "After" performance

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - GraphQLite Relationships (Priority: P3)

**Goal**: The graph database must correctly link the entire execution and learning trace.

**Independent Test**: Can be tested by executing Cypher queries and verifying all expected edges exist.

### Implementation for User Story 3

- [x] T015 [US3] Verify graph edges in `graph.py` accurately link Task -> Experience -> Evaluation -> Lesson
- [x] T016 [US3] If missing, add logic to `graph.py` to ensure strategy and workflow nodes are linked to the execution trace

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T017 Write quickstart test script to automate running the baseline and post-learning benchmarks
- [x] T018 Code cleanup and refactoring in `runner.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### Parallel Opportunities

- Once Foundational phase completes, User Story 1 (Runner) and User Story 2 (Streamlit UI layout) can be started in parallel.
