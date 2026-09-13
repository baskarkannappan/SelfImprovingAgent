# Phase 0: Research & Decisions

## Isolation of Benchmark Runs
- **Decision**: Use a separate benchmark SQLite database (`benchmark.db`) for baseline runs, but allow learning runs to use the primary `self_improving_agent.db`.
- **Rationale**: The specification requires that the baseline run starts with an "empty history" while NOT deleting production data. By dynamically pointing the `config.DB_PATH` to a temporary or benchmark-specific database file during baseline execution, we can guarantee total isolation.
- **Alternatives considered**: Adding a `namespace` or `benchmark_run_id` column to every single table in the database. This was rejected because it would require extensive schema migrations and modify the core logic of the agent, introducing risk to the production path.

## Measurement of Correctness and Quality
- **Decision**: Aggregate the `correct` (true/false) and `quality` (excellent, good, acceptable, poor) fields from the `evaluations` table for the specific benchmark run. 
- **Rationale**: The Phase 3 evaluation model already produces these exact metrics. By querying the database for a specific `run_id`, we can average these scores.
- **Alternatives considered**: Using an external grading LLM. Rejected because it violates the requirement to reuse the existing Phase 3 evaluation architecture.

## Streamlit Visualization
- **Decision**: Create a new page `9_continuous_improvement.py` that queries the benchmark database and the primary database to generate comparison tables.
- **Rationale**: Streamlit natively supports displaying Pandas DataFrames and metrics side-by-side (`st.columns`), making it trivial to display the "Before" vs "After" metrics required by the spec.
