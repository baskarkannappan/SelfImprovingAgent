# Feature Specification: Phase 2 Persistent Semantic Memory

**Feature Branch**: `003-semantic-memory`

**Created**: 2026-09-12

**Status**: Draft

**Input**: User description: Phase 2 — Persistent Semantic Memory + Developer Visualization

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and Retrieve Persistent Memories (Priority: P1)

A user interacts with the agent through the web interface. The agent independently solves the request and then persistently stores the user's task and the generated response as an "experience" in a persistent data store, along with a vector embedding of the request. During a future session, when the user asks a semantically similar question, the agent retrieves the past experience and uses it as context to generate a new response.

**Why this priority**: Core functionality of Phase 2. Memory persistence and semantic retrieval are the primary goals.

**Independent Test**: Can be fully tested by submitting a request in the web interface, restarting the application, submitting a similar request, and verifying that the past experience was successfully retrieved and used as context.

**Acceptance Scenarios**:

1. **Given** an empty persistent data store, **When** the user asks "Calculate 15% of 200" in the web interface, **Then** the agent answers "30", stores the experience in the data store, and stores its embedding in the vector store.
2. **Given** the previously stored experience, **When** the user asks "Calculate 20% of 500", **Then** the agent retrieves the previous percentage calculation experience as context, generates a new correct response ("100"), and stores the new experience.

---

### User Story 2 - Memory Isolation and Fallback (Priority: P2)

When the memory system is unavailable or no relevant memories are found (either database is empty or similarity falls below the threshold), the agent still answers the user's request. Furthermore, the agent correctly prioritizes the current request over conflicting past memories.

**Why this priority**: Ensures the agent remains functional and reliable even when past experiences are irrelevant.

**Independent Test**: Can be tested by asking completely unrelated questions and ensuring the agent still functions normally.

**Acceptance Scenarios**:

1. **Given** no relevant experiences in the database, **When** the user asks a completely new question, **Then** the agent solves it independently without memory context.
2. **Given** past experiences with errors (e.g. status: error), **When** a similar question is asked, **Then** the agent follows the current instructions and does not blindly repeat a previous failure.

---

### User Story 3 - Developer Visualization (Priority: P2)

A developer uses a read-only application to inspect the persistent data store, view stored experiences, examine vector embeddings, and manually test semantic search queries to understand the memory system's behavior.

**Why this priority**: Essential for debugging and visually understanding the internal mechanics of the semantic memory system.

**Independent Test**: Can be fully tested by running the developer application and navigating through the various data views and semantic search tools.

**Acceptance Scenarios**:

1. **Given** an existing agent database, **When** the developer opens the application, **Then** they can see the total number of experiences and vector records.
2. **Given** the semantic search screen, **When** the developer enters a test query, **Then** the system generates an embedding, searches the vector store, and displays the Top-K matching experiences with their similarity scores.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST intercept user requests from the web interface and generate a semantic vector embedding via the local embedding service.
- **FR-002**: System MUST search the vector storage for semantically similar previous experiences and retrieve up to a configurable `MEMORY_TOP_K` results.
- **FR-003**: System MUST filter retrieved experiences based on a configurable `MEMORY_SIMILARITY_THRESHOLD`.
- **FR-004**: System MUST inject the retrieved relevant memories as context to the language model before generating a response.
- **FR-005**: System MUST persistently store each interaction (task text, response text, status, creation timestamp) in a persistent data store.
- **FR-006**: System MUST persist the generated vector embedding associated with the experience in the vector storage engine.
- **FR-007**: System MUST automatically create the data store and all required tables on the first run, without modifying existing data on subsequent runs.
- **FR-008**: System MUST provide a read-only developer UI that connects to the same data store to visualize tables, experiences, vectors, memory retrieval trace, and semantic search.
- **FR-009**: System MUST gracefully handle failures (e.g., unavailable embedding service, unavailable data store) by logging errors and proceeding to answer the user's request without memory context.
- **FR-010**: System MUST NOT evaluate or automatically learn from experiences (reserved for Phase 3).

### Key Entities *(include if feature involves data)*

- **Experience**: Represents a past interaction. Attributes include ID, task text (user request), task type (default to "general"), response text, status, optional metadata JSON, and creation timestamp.
- **Vector Record**: The semantic representation (embedding) of the user request, directly linked to the Experience ID and stored in the vector storage engine.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Persistent data store and tables are successfully created if they do not exist.
- **SC-002**: Experiences are persistently stored and can be reliably retrieved across application restarts.
- **SC-003**: The embedding service correctly generates numeric vector embeddings with consistent dimensions matching the vector store schema.
- **SC-004**: Semantic search successfully returns related past experiences based on cosine similarity or equivalent vector distance metric.
- **SC-005**: Developer application successfully runs, connects to the data store, and displays data without performing any write operations.
- **SC-006**: All 10 automated test cases (as defined in the feature description) pass successfully.

## Assumptions

- The environment is configured with a functional language model and embedding generation service.
- Python environment has necessary dependencies to support the vector storage engine natively.
- The developer application is for local use only and does not require authentication or security hardening.
- The web interface remains the primary interface for the agent's conversational execution.
