# Quickstart: Validation Guide

This guide describes how to validate the multi-agent system execution.

## Prerequisites
- Docker LLM (Ollama) is running with Llama 3.2.
- The `self_improving_agent` ADK web server is running: `uv run adk web`
- The Streamlit Dev UI is running: `uv run streamlit run developer_ui/app.py`

## Test 1: Simple Task Bypass

1. Navigate to `http://127.0.0.1:8000/dev-ui`
2. Enter the prompt: `What is 20 + 30?`
3. **Expected Outcome**: The response should appear very quickly. Check the Streamlit "Multi-Agent Trace" or "Agent Executions" page to verify that the Planner and Retrieval agents were **skipped**. The trace should only show Orchestrator -> Solver -> Critic.

## Test 2: Complex Task Orchestration

1. In the ADK Web UI, enter the prompt: `Design a scalable microservice architecture for an order system.`
2. **Expected Outcome**: The system should take slightly longer as it orchestrates the full team. Check the Streamlit Dev UI to verify that the Orchestrator, Planner, Retrieval, Strategy, Solver, Critic, and Final Answer agents were all executed in sequence.

## Test 3: System Developer Commands

1. In the ADK Web UI, enter the command: `/test-multi-agent`
2. **Expected Outcome**: The system skips standard input processing and runs a hardcoded multi-agent test suite, returning a markdown summary of the agents executed and the final status directly in the chat.

## Test 4: Workflow Optimization Learning

1. Execute the complex task (Test 2) at least 5 times (to surpass `WORKFLOW_MIN_SAMPLES`).
2. Navigate to the Streamlit "Workflow Preferences" page.
3. **Expected Outcome**: You should see a calculated score for the "architecture" task type, and the system should have successfully recorded the most optimal workflow combination.
