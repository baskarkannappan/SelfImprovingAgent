# Quickstart Validation Guide: Strategy Optimization

This guide explains how to validate the Phase 4 features from end-to-end locally using ADK Web and Streamlit.

## Prerequisites
- The local Ollama Llama 3.2 model must be running.
- The virtual environment must be active with `uv`.

## 1. Start the System
Run ADK Web and Streamlit in separate terminals:
```bash
uv run adk web
uv run streamlit run developer_ui/app.py
```

## 2. Trigger Strategy Exploration
In ADK Web, submit a calculation task:
```
What is 15% of 200?
```
**Expected Outcome**: The system classifies the task as `calculation`, realizes it has no historical data for this category, selects a strategy (e.g., `direct_calculation`), and provides the answer. 

## 3. Trigger Strategy Comparison Test
In ADK Web, run the developer test command to simulate executions:
```
/test-strategy comparison
```
**Expected Outcome**: The system runs simulations, aggregates the statistics for strategies like `verify_calculation` vs `direct_calculation`, and outputs the statistics. It identifies the "Best Strategy" based on the scoring logic.

## 4. Trigger Adaptive Strategy Exploitation
In a new ADK Web session, submit another calculation task:
```
What is 25% of 400?
```
**Expected Outcome**: The system remembers the previous tests, pulls the best `strategy_preference` for `calculation` (e.g., `verify_calculation`), and executes that strategy to generate the answer.

## 5. View Data in Developer UI
Open `http://localhost:8501` (Streamlit UI).
Navigate to the new Phase 4 views:
- **Strategy Registry**: Confirm the predefined strategies are listed.
- **Strategy Performance**: Confirm the executions from steps 2-4 are recorded with success rates and durations.
- **Strategy Preferences**: Confirm a preference was stored for the `calculation` task type with a high score.
