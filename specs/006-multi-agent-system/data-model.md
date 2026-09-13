# Data Model: Multi-Agent System

This feature expands our SQLite persistent memory to track agent and workflow executions.

## Entities

### `agents`
Represents a logical specialized agent role.
- `id` (TEXT PRIMARY KEY) - e.g., 'orchestrator', 'planner', 'solver'
- `name` (TEXT)
- `description` (TEXT)
- `enabled` (BOOLEAN)

### `workflows`
Represents a specific registered sequence of agents.
- `id` (TEXT PRIMARY KEY) - e.g., 'simple_calculation', 'complex_architecture'
- `name` (TEXT)
- `task_type` (TEXT) - e.g., 'general', 'calculation', 'architecture'
- `agents_sequence` (TEXT JSON) - e.g., `["orchestrator", "solver", "critic"]`

### `agent_executions`
Records a single execution step.
- `id` (TEXT PRIMARY KEY)
- `workflow_execution_id` (TEXT)
- `agent_id` (TEXT)
- `status` (TEXT) - 'success', 'failed', 'partial'
- `duration_ms` (INTEGER)
- `confidence` (TEXT)
- `created_at` (TIMESTAMP)

### `workflow_executions`
Records an end-to-end user request handled by a workflow.
- `id` (TEXT PRIMARY KEY)
- `workflow_id` (TEXT)
- `experience_id` (INTEGER)
- `status` (TEXT)
- `success` (BOOLEAN)
- `quality` (TEXT)
- `duration_ms` (INTEGER)
- `created_at` (TIMESTAMP)

### `workflow_preferences`
Aggregated table summarizing the best workflows for a given task type.
- `task_type` (TEXT PRIMARY KEY)
- `workflow_id` (TEXT)
- `score` (REAL)
- `sample_count` (INTEGER)
- `updated_at` (TIMESTAMP)
