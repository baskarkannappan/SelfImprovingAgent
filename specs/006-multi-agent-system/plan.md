# Implementation Plan: Multi-Agent System

**Branch**: `006-multi-agent-system` | **Date**: 2026-09-13 | **Spec**: [spec.md](file:///C:/MyDrive/ProjectDrive/SelfImprovingAgents/specs/006-multi-agent-system/spec.md)

**Input**: Feature specification from `/specs/006-multi-agent-system/spec.md`

## Summary

This feature extends the Phase 4 system into a complete multi-agent architecture. It introduces specialized logical agents (Orchestrator, Planner, Retrieval, Strategy, Solver, Critic, Improvement, Final Answer) that communicate via structured objects. The system routes complex queries through this full pipeline while allowing simple tasks to bypass unnecessary planning overhead. The implementation will enforce hard execution limits and integrate performance learning.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: Google ADK 2, LiteLLM, FastAPI, SQLite, sqlite-vec, Streamlit

**Storage**: SQLite (relational) + sqlite-vec (vector embeddings)

**Testing**: pytest

**Target Platform**: Local Environment (Windows/Linux/Mac)

**Project Type**: ADK Agent Backend + Streamlit Developer UI

**Performance Goals**: Avoid unnecessary LLM calls (bypass Planner for simple tasks), execution within standard ADK timeout windows.

**Constraints**: Local model execution (Llama 3.2 via Ollama), no infinite loops (`MAX_AGENT_STEPS`, `MAX_RETRIES`), no source-code self-modification.

**Scale/Scope**: Local POC proving end-to-end self-improving orchestration without cloud dependencies.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Code Quality**: Ensure agents are well-isolated and modular. (PASS)
- **Testing Standards**: All new agent routing and bounds checking will be unit tested. (PASS)
- **User Experience Consistency**: ADK Web is maintained as the primary UI. (PASS)
- **Performance Requirements**: Short-circuiting simple tasks guarantees optimal performance. (PASS)

## Project Structure

### Documentation (this feature)

```text
specs/006-multi-agent-system/
├── plan.md              
├── research.md          
├── data-model.md        
├── quickstart.md        
├── contracts/           
└── tasks.md             
```

### Source Code (repository root)

```text
self_improving_agent/
├── agent.py                 # (Orchestrator hook entry point)
├── agents/                  # (New folder for specialized agents)
│   ├── orchestrator.py
│   ├── planner.py
│   ├── retrieval.py
│   ├── solver.py
│   ├── critic.py
│   ├── improvement.py
│   └── final_answer.py
├── strategy/                # (Existing Strategy Agent logic)
├── memory/                  # (Persistent DB logic)
└── developer_ui/            # (Streamlit application)
    └── pages/               # (New Workflow learning pages)
```

**Structure Decision**: A new `agents/` package will be created inside `self_improving_agent` to house the specialized logical agent implementations cleanly without bloating `agent.py`. `agent.py` will serve as the entry point delegating to the Orchestrator.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations detected. The structure perfectly aligns with the required modularity.
