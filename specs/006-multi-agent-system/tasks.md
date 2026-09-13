# Implementation Tasks: Multi-Agent System

This document outlines the actionable, dependency-ordered tasks required to implement the Multi-Agent System.

## Phase 1: Foundational Framework (5.1 - 5.2)

**Goal**: Establish the base agent interfaces, registry, and the core Orchestrator that controls workflow execution.

- [X] T001 [P] [US1] Create Agent Interface and `WorkflowState` dictionary structure in `self_improving_agent/agents/base.py`
- [X] T002 [US1] Create Agent Registry for discovering specialized agents in `self_improving_agent/agents/registry.py`
- [X] T003 [US1] Implement Workflow Controller logic in `self_improving_agent/agents/orchestrator.py`
- [X] T004 [US1] Update ADK hook in `self_improving_agent/agent.py` to route messages to the Orchestrator instead of directly to the LLM.

---

## Phase 2: Core Agents (5.3 - 5.7)

**Goal**: Implement the specialized logical agents that make up the multi-agent pipeline.

- [X] T005 [P] [US1] Implement Planner Agent (breaks down complex tasks) in `self_improving_agent/agents/planner.py`
- [X] T006 [P] [US1] Implement Retrieval Agent (fetches context) in `self_improving_agent/agents/retrieval.py`
- [X] T007 [P] [US1] Refactor Strategy logic into a dedicated Strategy Agent in `self_improving_agent/agents/strategy_agent.py`
- [X] T008 [US2] Implement Solver Agent (generates the main answer) in `self_improving_agent/agents/solver.py`
- [X] T009 [US3] Implement Critic Agent (evaluates Solver output) in `self_improving_agent/agents/critic.py`
- [X] T010 [US3] Implement Improvement Agent (handles retries and feedback) in `self_improving_agent/agents/improvement.py`
- [X] T011 [P] [US1] Implement Final Answer Agent (synthesizes the response) in `self_improving_agent/agents/final_answer.py`

---

## Phase 3: Persistence and Learning (5.8 - 5.10)

**Goal**: Store agent and workflow executions in the database and implement learning mechanisms.

- [X] T012 [P] [US4] Update database schema in `self_improving_agent/memory/database.py` with `agents`, `workflows`, `agent_executions`, `workflow_executions`, and `workflow_preferences` tables.
- [X] T013 [US4] Implement database write logic for workflow/agent executions in `self_improving_agent/agents/orchestrator.py`.
- [X] T014 [US4] Implement Workflow Learning logic (calculating best workflow) in `self_improving_agent/agents/workflow_learning.py`.
- [X] T015 [US4] Update GraphQLite schema in `self_improving_agent/memory/graph.py` with the new Multi-Agent relationships.

---

## Phase 4: Observability and Testing (5.11 - 5.12)

**Goal**: Make the new multi-agent behavior visible in the Dev UI and verify it works end-to-end.

- [X] T016 [P] [US4] Create Agent/Workflow Registry pages in `developer_ui/pages/5_agent_registry.py` and `developer_ui/pages/6_workflow_registry.py`.
- [X] T017 [P] [US4] Create Execution Trace observability page in `developer_ui/pages/7_execution_trace.py`.
- [X] T018 [P] [US4] Create Workflow Preferences UI in `developer_ui/pages/8_workflow_preferences.py`.
- [X] T019 [P] [US1] Implement `/test-multi-agent` and `/test-learning` slash commands in `self_improving_agent/agents/orchestrator.py`.
- [X] T020 Run end-to-end test scenarios from `quickstart.md`.
