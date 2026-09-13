# Quickstart Validation: Self-Improvement Learning Loop

## Prerequisites
- A running local instance of Ollama with `llama3.2` and `nomic-embed-text` models.
- Python 3.11 environment with `uv` dependencies synced.
- An initialized ADK SQLite database.

## Validation Scenarios

### 1. Verification of E2E Learning
**Purpose**: Confirm that answering a question generates an evaluation and potentially a lesson.
**Commands**:
1. Start the ADK web server: `uv run adk web`
2. Start the Streamlit developer UI: `uv run streamlit run developer_ui/app.py`
3. Ask the agent via ADK Web: "What is 15% of 200?"
4. Inspect the Streamlit Developer UI under the "Evaluations" tab and confirm an Evaluation was generated for the answer (should be `correct: true`, `confidence: high`).

### 2. Failure Identification
**Purpose**: Confirm the system learns from explicitly poor behavior.
**Commands**:
1. Temporarily hardcode a broken answer in the agent logic (e.g. `response_text = "35"`).
2. Ask the agent: "What is 15% of 200?"
3. Check the "Evaluations" tab to see `correct: false`. 
4. Check the "Lessons" tab to verify a lesson (e.g. "Verify percentage calculations") was successfully generated and recorded.

### 3. Graph Traceability
**Purpose**: Confirm the graph relationships persist via GraphQLite.
**Commands**:
1. Run a test script or inspect the "Learning Trace" graph visual in Streamlit.
2. Confirm the visual path maps `Experience -> Evaluation -> Lesson`.
3. Confirm the application did not crash or block the user's primary conversational turn while processing the evaluation.
