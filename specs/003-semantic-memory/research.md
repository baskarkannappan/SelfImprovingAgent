# Phase 0: Outline & Research

## Technical Context Resolution

The feature requirements explicitly define the technology stack, so no deep research tasks are needed to select alternatives. The following decisions are finalized based on the project constraints:

1. **Storage Engine**: SQLite
   - *Rationale*: Mandated by requirements for persistent storage.
   - *Alternative considered*: PostgreSQL, Neo4j (out of scope for Phase 2).

2. **Vector Search**: sqlite-vec
   - *Rationale*: Mandated by requirements for semantic vector search natively within SQLite.

3. **Embedding Generation**: `nomic-embed-text` via Ollama
   - *Rationale*: Mandated local embedding model. Will integrate with the existing LiteLLM setup or direct Ollama API depending on ADK capabilities.

4. **Developer Visualization**: Streamlit
   - *Rationale*: Mandated by requirements for a read-only developer UI to inspect SQLite and vector data.

## Best Practices & Patterns

1. **Memory Service Abstraction**: 
   - The memory functionality (generate_embedding, store_experience, retrieve_similar_experiences, build_memory_context) will be abstracted into a dedicated `memory/` module (`self_improving_agent/memory/`) rather than tightly coupled to the root agent.
   
2. **Deterministic Retrieval**:
   - The retrieval flow will be deterministically controlled by Python code before invoking the LLM, rather than relying on the LLM to write SQL queries.

3. **Read-Only Streamlit**:
   - Streamlit will connect to the same SQLite database (`data/agent.db`) using read-only queries to prevent accidental modifications to the agent's memory.
