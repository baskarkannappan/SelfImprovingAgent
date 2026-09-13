# Phase 0: Outline & Research

## Decision 1: Database Schema for Strategy Data
- **Decision**: Add four new tables to the existing SQLite database: `strategies`, `strategy_executions`, `strategy_performance`, and `strategy_preferences`.
- **Rationale**: The requirements specifically ask to persist this information in SQLite and reuse existing Phase 2/3 tables where possible. By creating distinct tables for the strategy definitions, execution metadata, evaluation metrics, and calculated preferences, we maintain a normalized schema that maps cleanly to GraphQLite.
- **Alternatives considered**: Storing everything as JSON blobs in a single table, but this would prevent efficient GraphQLite queries and aggregations (like success rate calculation).

## Decision 2: Strategy Definition and Storage
- **Decision**: Define strategies as Python dictionaries or Pydantic models in code that are synced to the `strategies` table on startup (or via a registry). The LLM is NOT allowed to invent strategies on the fly.
- **Rationale**: Section 7 explicitly states the LLM MUST NOT invent arbitrary executable strategies and the registry must be deterministic.
- **Alternatives considered**: Allowing the LLM to generate JSON strategies, which was explicitly forbidden in the requirements.

## Decision 3: Strategy Selection Scoring
- **Decision**: Implement a simple deterministic scoring function in Python: `historical_success_score + quality_score + confidence_score`. Use a random number generator for the 10% exploration rate.
- **Rationale**: Section 10 and 11 specify a deterministic scoring mechanism and a simple configurable exploration rate (e.g., 10%) without needing a complex reinforcement learning algorithm.
- **Alternatives considered**: Using an LLM to decide the strategy, but the requirements explicitly advise against relying immediately on an LLM for selection and ask for a simple formula.

## Decision 4: GraphQLite Relationships
- **Decision**: Extend the GraphQLite schema to link `Task -> preferred_strategy -> Strategy`, `Experience -> used_strategy -> Strategy`, `Strategy -> has_execution -> StrategyExecution`, and `StrategyExecution -> evaluated_by -> Evaluation`.
- **Rationale**: Maps exactly to the GraphQLite Integration requirements in Section 22.

## Decision 5: Developer UI (Streamlit)
- **Decision**: Add new read-only views to the existing Streamlit app for Strategy Registry, Performance, Comparison, Preferences, and Execution Trace by querying SQLite/GraphQLite directly.
- **Rationale**: Keeps the testing and visualization local, testable, and strictly read-only as required in Section 31 and 32.
