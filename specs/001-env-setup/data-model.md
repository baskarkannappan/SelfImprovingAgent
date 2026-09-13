# Data Model: Phase 0 — POC Prerequisites and Development Environment

*Note: As this feature strictly focuses on environment setup and infrastructure validation, there is no permanent business data model. The following describes the data structures used temporarily during the environment validation.*

## 1. Vector Store Validation (sqlite-vec)

During validation, a temporary vector table is created to ensure the extension loads and operates correctly.

### `test_embeddings`
- `id` (INTEGER, Primary Key)
- `embedding` (FLOAT VECTOR)

**Test Flow**:
1. Insert a 1536-dimensional (or matching `nomic-embed-text`) vector.
2. Execute a K-Nearest Neighbors (KNN) query against the table.
3. Validate result retrieval.

## 2. Graph Relationship Validation (GraphQLite)

During validation, a temporary graph structure is created to ensure relationships can be queried.

### Nodes
- **Task**: `{"name": "Calculate percentage"}`
- **Strategy**: `{"name": "Direct Calculation"}`

### Edges
- **USES**: `Task` → `Strategy`

**Test Flow**:
1. Insert `Task` and `Strategy` nodes.
2. Create the `USES` edge between them.
3. Query the `Task` to retrieve its connected `Strategy`.
