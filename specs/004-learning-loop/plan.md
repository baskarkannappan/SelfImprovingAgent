# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

Phase 3 introduces the first version of the self-improvement loop for the ADK agent. It augments the agent's memory capability by enabling it to evaluate its own responses, learn from its mistakes or insights by creating persistent "Lessons", and use GraphQLite to track the graph relationships between tasks, experiences, evaluations, and lessons. Streamlit UI will be expanded to provide a tracing interface for these components.

## Technical Context

**Language/Version**: Python 3.11

**Primary Dependencies**: `google-adk`, `litellm`, `fastapi`, `sqlite3`, `sqlite-vec`, `graphqlite`

**Storage**: SQLite (Structured Data), sqlite-vec (Embeddings), GraphQLite (Relationships)

**Testing**: `pytest`

**Target Platform**: Local environment

**Project Type**: Local AI Agent Framework

**Performance Goals**: Fast local execution without relying on cloud APIs.

**Constraints**: Local deployment only, LLMs run locally via ollama (llama3.2 and nomic-embed-text), Streamlit UI remains strictly read-only.

**Scale/Scope**: Single developer environment

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Code Quality**: All components (Evaluator, Learner) will be properly abstracted.
- **Testing Standards**: Automated tests required for evaluation logic, lesson generation, and graph relationships.
- **User Experience Consistency**: The Streamlit Developer View will remain consistent with Phase 2's design.
- **Performance Requirements**: Synchronous loop evaluation should be kept performant.

## Project Structure

### Documentation (this feature)

```text
specs/004-learning-loop/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)
```text
self_improving_agent/
├── agent.py
├── evaluator.py
├── learner.py
├── memory.py
├── graph.py
└── utils.py

developer_ui/
├── app.py
└── pages/
    ├── evaluations.py
    └── lessons.py

tests/
├── test_evaluator.py
├── test_learner.py
└── test_graph.py
```

**Structure Decision**: The source code is organized as a single package project matching Option 1. We will introduce `evaluator.py`, `learner.py`, and `graph.py` to handle the new components.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None      | N/A        | N/A                                 |
