# Research: Self-Improvement Learning Loop

## Technical Context Unknowns Resolved

1. **Evaluator Model**:
   - Decision: Use the local `llama3.2` model via LiteLLM for subjective evaluations, with a fallback to simple deterministic rules if the task allows.
   - Rationale: The architecture specifies using the existing model. A separate cloud model is explicitly out of scope, avoiding API costs and ensuring local privacy.
   - Alternatives considered: Using a stronger remote LLM (GPT-4o) specifically for evaluation (rejected due to out of scope constraints).

2. **Graph Relational Storage**:
   - Decision: Use the pre-installed `graphqlite` library for relationship edges (`Task -> Experience -> Evaluation -> Lesson`).
   - Rationale: Requirement #28 explicitly mandates using the actual `graphqlite` API/version installed in the project rather than building custom `nodes`/`relationships` tables manually. 
   - Alternatives considered: Pure SQLite join tables or Neo4j (rejected, Neo4j is out of scope).

3. **Storage Pipeline Integration**:
   - Decision: Continue appending to SQLite. Use `sqlite-vec` for `Lesson` embeddings (via local `nomic-embed-text`), and use `graphqlite` for mapping evaluation IDs to lesson IDs.
   - Rationale: Maintains separation of concerns: structured records (SQLite), semantic search (sqlite-vec), relationships (GraphQLite).

4. **Streamlit UI Extensibility**:
   - Decision: The existing `developer_ui/app.py` read-only dashboard will be augmented with new pages/tabs for "Evaluations", "Lessons", and "Learning Trace" using Streamlit's dataframes and graphviz/networkx for simple visual graph structures.
   - Rationale: Reuses existing infrastructure without requiring a custom REST API or complex frontend architecture.

## Constitution Verification

All research conclusions comply with the project constitution. Local privacy is preserved. Modularity is maintained by separating the Learner, Evaluator, and Main Agent logical flows. Testing will be covered as mandated by the constitution.
