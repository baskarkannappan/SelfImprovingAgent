# Phase 0: Outline & Research

## Decision 1: Agent Abstraction vs Native ADK Agents

- **Decision**: We will implement the specialized agents as "logical agents" (Python classes/functions) within our single ADK Agent service rather than creating multiple separate ADK services.
- **Rationale**: The requirements specifically state: "All logical agents MAY use the same Llama 3.2 model... The architecture should treat these as separate logical roles. Do not require separate models." Implementing them as internal Python components avoids the massive overhead of managing multiple Uvicorn instances and HTTP inter-agent communication, keeping the POC fast and reliable while fulfilling the exact requirement.
- **Alternatives considered**: Deploying separate ADK agent microservices (rejected due to overhead and complexity).

## Decision 2: State Passing

- **Decision**: Agents will communicate by passing a structured `WorkflowState` object (or python dictionary) down the execution chain.
- **Rationale**: Meets requirement "System MUST communicate between agents using structured objects, not plain strings."
- **Alternatives considered**: Passing long strings of conversation history (rejected by requirements).

**Research Phase Complete.** All requirements and technical contexts are fully specified with no remaining ambiguities.
