# Feature Specification: Self-Improvement Learning Loop

**Feature Branch**: `004-learning-loop`

**Created**: 2026-09-12

**Status**: Draft

**Input**: User description: "Phase 3 — Self-Evaluation, Learning, and Graph Relationships"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Evaluate Answers (Priority: P1)

The system needs to evaluate its own answers automatically after providing a response to the user.

**Why this priority**: Essential foundation for self-improvement; the agent must recognize if it was correct or wrong before it can learn anything.

**Independent Test**: Can be tested by having the system output an evaluation record with correct, quality, confidence, and reason fields after answering a prompt.

**Acceptance Scenarios**:

1. **Given** a deterministic or subjective user request and a generated answer, **When** the evaluation phase occurs, **Then** a persistent evaluation record is created indicating correctness, quality, confidence, and reason.
2. **Given** a failing evaluation step, **When** the user request is served, **Then** the primary answer is still returned without disruption.

---

### User Story 2 - Extract Lessons (Priority: P1)

When the agent evaluates an answer and spots an opportunity for improvement or a reusable rule, it extracts a generic lesson.

**Why this priority**: Without extracting a lesson, the system cannot modify its future behavior based on past mistakes or successes.

**Independent Test**: Can be tested by providing an evaluation of an incorrect answer and checking if a valid lesson record (with text, type, confidence) is generated and stored in SQLite.

**Acceptance Scenarios**:

1. **Given** an evaluation containing a reusable mistake, **When** the Learner component analyzes it, **Then** a lesson is created and persisted to SQLite.
2. **Given** an evaluation of a trivial interaction with no reusable insight, **When** the Learner component analyzes it, **Then** no meaningless lesson is created.

---

### User Story 3 - Graph Connections (Priority: P2)

The developer needs to see how experiences, evaluations, and lessons relate to each other.

**Why this priority**: Needed for traceability and debugging the learning process via GraphQLite.

**Independent Test**: Can be tested by querying the graph to find the Lesson produced by a specific Evaluation of a specific Experience.

**Acceptance Scenarios**:

1. **Given** a completed learning cycle, **When** querying the GraphQLite store, **Then** the `Experience -> Evaluation` and `Evaluation -> Lesson` relationships are present.

---

### User Story 4 - Retrieve Lessons for Context (Priority: P1)

When a new user request arrives, the system retrieves semantically relevant past lessons and injects them into the Main Agent's context.

**Why this priority**: This completes the learning loop, actually applying past knowledge to future tasks.

**Independent Test**: Can be tested by asking a question similar to a past failure and observing if the relevant lesson is included in the LLM context.

**Acceptance Scenarios**:

1. **Given** a stored lesson about a specific topic and a new related user request, **When** the system retrieves context, **Then** the lesson is retrieved via sqlite-vec and presented in the RELEVANT LESSONS section.

---

### User Story 5 - Developer UI Traceability (Priority: P3)

The developer needs to visualize evaluations, lessons, learning traces, and graph relationships in Streamlit.

**Why this priority**: Provides observability to verify the AI's internal reasoning and learning operations.

**Independent Test**: Can be tested by opening the Streamlit app and viewing the Evaluations and Lessons tables, and checking the graph view for connections.

**Acceptance Scenarios**:

1. **Given** the learning loop has executed, **When** the developer visits the Streamlit UI, **Then** they can view read-only evaluations, lessons, and relationships associated with an experience.

### Edge Cases

- What happens when evaluation model fails or throws an exception? (The main answer should still be returned, error logged).
- What happens when the learner model fails? (The main answer and evaluation should remain available, error logged).
- How does the system handle "unknown" correctness on subjective questions? (The system supports an "unknown" correct state).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST create a persistent evaluation record in SQLite containing `experience_id`, `correct` (true, false, or unknown), `quality` (excellent, good, acceptable, poor), `confidence` (high, medium, low), and a concise `reason`.
- **FR-002**: System MUST evaluate answers without modifying the Main Agent's original answer.
- **FR-003**: System MUST NOT fail the user's primary response if the Evaluator or Learner processes fail.
- **FR-004**: System MUST analyze evaluations and create a persistent Lesson record containing `lesson_text`, `lesson_type`, `source_experience_id`, `source_evaluation_id`, and `confidence`.
- **FR-005**: System MUST ONLY create a lesson when reusable information is identified (no trivial/meaningless lessons).
- **FR-006**: System MUST generate an embedding for each Lesson using the `nomic-embed-text` model and store it in sqlite-vec.
- **FR-007**: System MUST retrieve relevant lessons from sqlite-vec and include them in the Main Agent's context prompt under a "RELEVANT LESSONS" block.
- **FR-008**: System MUST track relationships in GraphQLite mapping `Task -> Experience -> Evaluation -> Lesson`.
- **FR-009**: System MUST provide read-only views for Evaluations, Lessons, Learning Traces, and Graph Relationships in the Streamlit application.
- **FR-010**: System MUST read LLM, embedding, and similarity configurations from `.env` variables instead of hardcoding.
- **FR-011**: System MUST NOT autonomously rewrite its own Python source code, system prompts, or model weights.

### Key Entities *(include if feature involves data)*

- **Evaluation**: A judgment on the Main Agent's answer. Fields: `id`, `experience_id`, `correct`, `quality`, `confidence`, `reason`, `created_at`.
- **Lesson**: Reusable knowledge extracted from an evaluation. Fields: `id`, `lesson_text`, `lesson_type`, `source_experience_id`, `source_evaluation_id`, `confidence`, `created_at`.
- **Experience (existing)**: The user request and generated response.
- **Task (existing)**: The overarching user goal.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: System successfully evaluates 100% of generated answers without disrupting or delaying the user's synchronous response.
- **SC-002**: System generates persistent Lesson records for errors and correctly retrieves those lessons in 100% of subsequent semantically similar requests.
- **SC-003**: The Streamlit Developer UI accurately visualizes the `Experience -> Evaluation -> Lesson` graph trace for any given experience.
- **SC-004**: All new database records (Evaluations, Lessons, Vectors, GraphQLite nodes) persist safely across application restarts.

## Assumptions

- We assume synchronous evaluation/learning execution is acceptable for the POC phase as long as it handles errors safely, though it can be made asynchronous later.
- We assume the local Llama 3.2 model will act as the Main Agent, Evaluator, and Learner.
- We assume deterministic evaluation mechanisms can be plugged in later, but LLM-based evaluation will be used for subjective cases.
- We assume Streamlit is only for observability and will remain strictly read-only.
