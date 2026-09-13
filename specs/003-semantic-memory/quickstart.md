# Quickstart Validation Guide: Semantic Memory

This guide outlines how to manually validate the semantic memory and developer visualization features.

## Prerequisites

1.  **Ollama**: Ensure Ollama is running locally.
2.  **Models**: Ensure `llama3.2` and `nomic-embed-text` are pulled and available in Ollama.
3.  **Dependencies**: Run `uv sync` to ensure `sqlite-vec` and `streamlit` are installed.

## Validation Scenarios

### Scenario 1: Agent Execution & Memory Creation

1. Start the ADK Web interface:
   ```bash
   uv run adk web
   ```
2. Open the ADK Web UI (`http://127.0.0.1:8000/dev-ui/?app=self_improving_agent`).
3. Submit the following task:
   `Calculate 15% of 200.`
4. Verify the agent returns `30`. This implicitly tests that the SQLite database was initialized and the memory was saved.

### Scenario 2: Developer Visualization

1. In a new terminal, start the Streamlit application:
   ```bash
   uv run streamlit run developer_ui/app.py
   ```
2. Open the Streamlit UI in your browser (usually `http://localhost:8501`).
3. **Database Overview**: Verify the database path and the number of experiences (should be at least 1).
4. **Experiences View**: Verify the "Calculate 15% of 200" task and its response are listed.
5. **Vector Data**: Inspect the vector to ensure it is populated with a float array.

### Scenario 3: Semantic Search via Streamlit

1. Navigate to the **Semantic Search** section in the Streamlit application.
2. Enter the query: `Calculate 25% of 400`
3. Click **Search Similar Memories**.
4. Verify that the previous "Calculate 15% of 200" experience is retrieved and displayed with its similarity score.

### Scenario 4: In-Agent Semantic Retrieval

1. Return to the ADK Web interface (or start a new session).
2. Submit the following task:
   `Calculate 20% of 500.`
3. Observe the ADK Web UI or the terminal logs. You should see logs indicating a memory search was performed and that it retrieved the previous experience.
4. Verify the agent returns `100`.
