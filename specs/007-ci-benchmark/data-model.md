# Phase 1: Data Model

## Existing Tables Used
The benchmark framework will reuse all tables created in Phase 1-5 (`experiences`, `evaluations`, `lessons`, `strategy_preferences`, `workflow_executions`, etc.).

## New Entity: BenchmarkResult (In-Memory / JSON)
Instead of modifying the core database schema, the benchmark framework will store its aggregated reports as JSON files or in-memory pandas DataFrames during the Streamlit session.

### BenchmarkReport
- `run_id`: UUID
- `timestamp`: DateTime
- `phase`: String ("baseline" or "post_learning")
- `total_tasks`: Integer
- `success_rate`: Float (0.0 - 1.0)
- `average_quality`: Float (1.0 - 4.0)
- `average_latency_ms`: Integer
- `lessons_retrieved`: Integer
- `lessons_reused`: Integer
- `critic_invocations`: Integer
- `improvement_invocations`: Integer
- `task_results`: List[TaskResult]

### TaskResult
- `task_id`: String
- `task_text`: String
- `correct`: Boolean
- `quality`: String
- `selected_strategy`: String
- `selected_workflow`: String
- `duration_ms`: Integer
