# Data Model: Strategy Optimization

## SQLite Tables

### `strategies`
Stores the deterministic strategies available in the registry.
- `id` (TEXT, Primary Key)
- `name` (TEXT)
- `task_type` (TEXT) - e.g., 'calculation'
- `description` (TEXT)
- `steps` (JSON TEXT) - array of step names
- `enabled` (BOOLEAN)
- `created_at` (TIMESTAMP)

### `strategy_executions`
Records the execution instance of a strategy for a specific task.
- `id` (TEXT, Primary Key)
- `strategy_id` (TEXT, Foreign Key to `strategies`)
- `task_type` (TEXT)
- `experience_id` (TEXT, Foreign Key to existing `experiences`)
- `execution_start` (TIMESTAMP)
- `execution_end` (TIMESTAMP)
- `duration_ms` (INTEGER)
- `status` (TEXT) - 'success', 'failed'

### `strategy_performance`
Stores the evaluation metrics for a completed strategy execution.
- `id` (TEXT, Primary Key)
- `strategy_id` (TEXT, Foreign Key to `strategies`)
- `task_type` (TEXT)
- `experience_id` (TEXT, Foreign Key to `experiences`)
- `evaluation_id` (TEXT, Foreign Key to existing `evaluations`)
- `success` (BOOLEAN)
- `quality` (TEXT) - e.g., 'excellent', 'poor'
- `confidence` (TEXT) - e.g., 'high', 'low'
- `duration_ms` (INTEGER)
- `created_at` (TIMESTAMP)

### `strategy_preferences`
Stores the calculated preference for a task type based on aggregated performance.
- `id` (TEXT, Primary Key)
- `task_type` (TEXT)
- `strategy_id` (TEXT, Foreign Key to `strategies`)
- `score` (REAL)
- `rank` (INTEGER)
- `confidence` (TEXT)
- `sample_count` (INTEGER)
- `reason` (TEXT)
- `updated_at` (TIMESTAMP)

## GraphQLite Relationships
- `Task` -> `produces` -> `Experience` (existing)
- `Experience` -> `evaluated_by` -> `Evaluation` (existing)
- `Evaluation` -> `produces` -> `Lesson` (existing)
- `Experience` -> `used_strategy` -> `Strategy`
- `Strategy` -> `has_execution` -> `StrategyExecution`
- `StrategyExecution` -> `produced` -> `Experience`
- `StrategyExecution` -> `evaluated_by` -> `Evaluation`
- `Task` -> `preferred_strategy` -> `Strategy`
