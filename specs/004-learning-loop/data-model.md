# Data Model: Self-Improvement Learning Loop

## Entities

### Evaluation
*Represents the Evaluator Agent's judgment on a Main Agent response.*
- `id` (INTEGER, Primary Key)
- `experience_id` (INTEGER, Foreign Key to experiences.id)
- `correct` (TEXT) - "true", "false", or "unknown"
- `quality` (TEXT) - "excellent", "good", "acceptable", or "poor"
- `confidence` (TEXT) - "high", "medium", or "low"
- `reason` (TEXT) - Concise explanation
- `created_at` (DATETIME)

### Lesson
*Represents extracted reusable knowledge stored for future retrieval.*
- `id` (INTEGER, Primary Key)
- `lesson_text` (TEXT)
- `lesson_type` (TEXT) - e.g., "error_prevention", "formatting", "verification"
- `source_experience_id` (INTEGER, Foreign Key to experiences.id)
- `source_evaluation_id` (INTEGER, Foreign Key to evaluations.id)
- `confidence` (TEXT)
- `created_at` (DATETIME)

### Lesson Embedding (sqlite-vec)
*Vector representation of the lesson text for semantic search.*
- `rowid` (INTEGER) - Mapped to `lessons.id`
- `embedding` (FLOAT VECTOR) - Dense vector array from `nomic-embed-text`

## Graph Relationships (GraphQLite)
GraphQLite will manage the semantic web of these entities using edges:
- `PRODUCES`: `Task` -> `Experience`
- `EVALUATED_BY`: `Experience` -> `Evaluation`
- `PRODUCES_LESSON`: `Evaluation` -> `Lesson`
- `APPLIES_TO`: `Lesson` -> `Future Task`

## Validation Rules
- `Evaluation.correct` must be constrained strictly to the values: `true`, `false`, `unknown`.
- A `Lesson` should only be created if the evaluation provides actionable and non-trivial feedback.
