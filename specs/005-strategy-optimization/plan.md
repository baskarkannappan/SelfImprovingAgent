# Implementation Plan: Strategy Optimization

**Branch**: `[005-strategy-optimization]` | **Date**: 2026-09-13 | **Spec**: [specs/005-strategy-optimization/spec.md](file:///c:/MyDrive/ProjectDrive/SelfImprovingAgents/specs/005-strategy-optimization/spec.md)

**Input**: Feature specification from `/specs/005-strategy-optimization/spec.md`

## Summary

Phase 4 introduces adaptive strategy selection, enabling the agent to learn which problem-solving strategy works best for a given task type (like "calculation"). It uses a deterministic scoring formula, executes strategies, logs performance to SQLite, and aggregates data to pick the best strategy for future tasks while reserving 10% for exploration.

## Technical Context

**Language/Version**: Python 3.11

**Primary Dependencies**: Google ADK 2, ADK Web, LiteLLM, Llama 3.2, SQLite, sqlite-vec, GraphQLite, nomic-embed-text, Streamlit, pytest

**Storage**: SQLite

**Testing**: pytest

**Target Platform**: Local CLI / web

**Project Type**: AI Agent (ADK application)

**Performance Goals**: Negligible execution overhead during strategy selection/evaluation.

**Constraints**: Local deterministic POC. No self-modifying Python code. No cloud LLMs.

**Scale/Scope**: Local POC with a predefined small set of strategies.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Code Quality**: New strategy logic will be strictly isolated into reusable modules (e.g., `strategy_selector`, `strategy_executor`, `strategy_evaluator`).
- **Testing Standards**: All new strategy functions will be covered by deterministic unit tests without relying purely on LLM output.
- **User Experience**: ADK Web remains unchanged for normal requests; Streamlit gets distinct read-only diagnostic pages.
- **Performance**: The score calculation and DB inserts are synchronous but optimized.

## Project Structure

### Documentation (this feature)

```text
specs/005-strategy-optimization/
├── plan.md              
├── research.md          
├── data-model.md        
├── quickstart.md        
└── tasks.md             
```

### Source Code (repository root)

```text
# Single project 
self_improving_agent/
├── agent.py (Entry point for adk run)
├── memory/
│   ├── memory.py
│   └── database.py
├── evaluation/
│   └── evaluator.py
├── learning/
│   └── learner.py
├── strategy/ (NEW MODULE)
│   ├── registry.py (Deterministic list of strategies)
│   ├── classifier.py (Task type classifier)
│   ├── selector.py (Scoring logic & exploration)
│   └── executor.py (Executes selected strategy)
└── config.py

developer_ui/
├── app.py
└── pages/
    ├── 1_strategy_registry.py
    ├── 2_strategy_performance.py
    └── 3_strategy_preferences.py

tests/
├── test_strategy_registry.py
├── test_strategy_selection.py
├── test_strategy_scoring.py
└── test_strategy_preferences.py
```

**Structure Decision**: A new `strategy` sub-package inside `self_improving_agent` will house all Phase 4 logic cleanly. Streamlit gets dedicated read-only pages in `developer_ui/pages/`. Tests are placed in `tests/`.

## Complexity Tracking

No violations found. The architecture aligns with the existing constraints.
