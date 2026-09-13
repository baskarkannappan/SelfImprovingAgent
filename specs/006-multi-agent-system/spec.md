# Feature Specification: Multi-Agent System

**Feature Branch**: `006-multi-agent-system`

**Created**: 2026-09-13

**Status**: Draft

**Input**: User description: "@[c:\MyDrive\ProjectDrive\SelfImprovingAgents\requirements\006-requirement]"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Complex Task Execution (Priority: P1)

Users submit a complex query (e.g., "Design an order management architecture"), and the system intelligently orchestrates a full team of specialized agents to plan, retrieve, execute, and validate the answer.

**Why this priority**: This is the core functionality of Phase 5, proving that the system can delegate and coordinate complex workflows rather than relying on a single monolithic LLM call.

**Independent Test**: Can be fully tested by submitting a complex architecture query and verifying that the execution trace includes the Orchestrator, Planner, Retrieval, Strategy, Solver, and Critic agents.

**Acceptance Scenarios**:

1. **Given** a fresh system state, **When** the user asks a complex architectural question, **Then** the Orchestrator classifies the task as "complex", invokes the Planner to create steps, runs the Retrieval and Strategy agents for context, and executes the Solver.
2. **Given** the Solver completes its work, **When** the Critic evaluates it, **Then** the Final Answer Agent synthesizes the results and returns them to the user.

---

### User Story 2 - Simple Task Execution (Priority: P2)

Users submit a simple query (e.g., "What is 15% of 200?"), and the system executes a minimal workflow, bypassing unnecessary planning agents to save time and tokens.

**Why this priority**: Ensures the multi-agent system does not unnecessarily bloat simple requests, maintaining performance and user experience.

**Independent Test**: Can be fully tested by submitting a simple math question and verifying that the Planner and Retrieval agents are skipped.

**Acceptance Scenarios**:

1. **Given** a user request, **When** the request is simple, **Then** the Orchestrator classifies it as "simple" and routes it directly to the Solver, followed by the Critic, bypassing the Planner.

---

### User Story 3 - Retry and Improvement (Priority: P2)

When the Solver produces an inadequate response, the Critic identifies the flaws, and an Improvement Agent triggers a controlled retry with specific guidance.

**Why this priority**: Demonstrates self-correction within a single workflow execution, increasing reliability without infinite loops.

**Independent Test**: Can be fully tested by simulating a failed Critic evaluation and ensuring the Improvement Agent triggers a retry up to the `MAX_RETRIES` limit.

**Acceptance Scenarios**:

1. **Given** the Solver produces a response, **When** the Critic evaluates it as incomplete, **Then** the Improvement Agent is invoked to identify missing information and requests a retry from the Solver.
2. **Given** a retry is requested, **When** the system has reached `MAX_RETRIES`, **Then** the system gracefully returns a partial result instead of infinite looping.

---

### User Story 4 - Workflow Learning (Priority: P3)

The system records the success rates of different workflow executions and automatically selects the highest-performing workflow for future tasks of the same type.

**Why this priority**: Fulfills the self-improving aspect of the architecture, proving the system learns from its own execution history.

**Independent Test**: Can be fully tested by executing two different workflows for the same task type, ensuring the database records their success rates, and verifying the Orchestrator picks the best one next time.

**Acceptance Scenarios**:

1. **Given** multiple recorded workflow executions for "architecture" tasks, **When** a new architecture task arrives, **Then** the Orchestrator automatically selects the workflow combination with the highest historical success rate.

---

### Edge Cases

- What happens when a specialized agent (e.g., Retrieval Agent) crashes or times out? (The Orchestrator should catch the failure, log it, and use a fallback or continue with reduced context).
- How does the system handle an infinite back-and-forth between the Solver and Critic? (It enforces `MAX_AGENT_STEPS` and `MAX_RETRIES`).
- What if the user asks a question that doesn't fit any known strategy or workflow? (It defaults to a safe, generic fallback workflow).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST route all incoming tasks through an Orchestrator agent that coordinates execution.
- **FR-002**: System MUST classify tasks by complexity (simple, moderate, complex).
- **FR-003**: System MUST provide a Planner Agent to break complex requests into structured sub-tasks.
- **FR-004**: System MUST provide a Retrieval Agent to fetch relevant context from SQLite/sqlite-vec/GraphQLite.
- **FR-005**: System MUST execute tasks using a Solver Agent, guided by a Strategy Agent.
- **FR-006**: System MUST evaluate the Solver's output using a Critic Agent.
- **FR-007**: System MUST provide an Improvement Agent to request retries with specific feedback when evaluations fail.
- **FR-008**: System MUST enforce a hard limit on execution steps (`MAX_AGENT_STEPS`) and retries (`MAX_RETRIES`).
- **FR-009**: System MUST record execution metadata (success, quality, confidence, duration) for individual agents and entire workflows.
- **FR-010**: System MUST automatically select preferred workflows for future tasks based on aggregated historical workflow performance.
- **FR-011**: System MUST communicate between agents using structured objects, not plain strings.
- **FR-012**: System MUST expose `/test-agent`, `/test-workflow`, `/test-multi-agent`, and `/test-learning` commands for developer testing in the ADK Web UI.
- **FR-013**: System MUST update the Streamlit Developer UI to show Agent Registry, Agent Executions, Agent Performance, Workflow Registry, Workflow Performance, and Workflow Preferences.

### Key Entities

- **Agent**: Represents a logical specialized role (Orchestrator, Planner, Solver, etc.) with a specific prompt/behavior.
- **Workflow**: Represents a sequence of agent executions (e.g., Planner -> Retrieval -> Solver).
- **AgentExecution**: Records the performance and metadata of a single agent's run.
- **WorkflowExecution**: Records the end-to-end performance of a multi-agent workflow run.
- **WorkflowPreference**: The learned best workflow for a specific task type based on historical scores.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The system can successfully coordinate a multi-agent workflow (Orchestrator -> Planner -> Retrieval -> Strategy -> Solver -> Critic) to answer a complex prompt.
- **SC-002**: Simple tasks bypass the Planner and Retrieval agents, executing at least 30% faster than complex tasks.
- **SC-003**: The system survives an intentional agent timeout or failure without crashing the entire ADK process, returning a controlled partial response.
- **SC-004**: After 5 iterations of a task type, the system deterministically selects the highest-scoring workflow for the 6th iteration.
- **SC-005**: The system strictly terminates after `MAX_AGENT_STEPS` or `MAX_RETRIES` is reached, mathematically guaranteeing no infinite loops.

## Assumptions

- We will reuse the local Llama 3.2 model for all logical agents rather than spinning up different models.
- ADK Web remains the primary chat interface, and we will not build a custom chat UI.
- The system relies on the existing memory layer built in Phases 1-4.
- Source code will not be autonomously modified; the system learns strictly through SQLite database updates.
