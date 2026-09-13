# Quickstart: Continuous Improvement Benchmark

## 1. Run Baseline Benchmark
First, run the benchmark dataset against an empty isolated database to establish the baseline.

```bash
uv run python -m self_improving_agent.benchmark.runner --mode baseline
```

## 2. Execute Learning Tasks
Next, use the ADK Web UI or an automated script to pass the 5 mandatory learning prompts (or normal chat usage) through the system so it can generate lessons and evaluate strategies.

## 3. Run Post-Learning Benchmark
Run the exact same benchmark dataset again, but this time allow it to use the primary database that contains the learned experiences.

```bash
uv run python -m self_improving_agent.benchmark.runner --mode post_learning
```

## 4. View Results
Open the Streamlit Dev UI and navigate to the "Continuous Improvement" page to see the side-by-side comparison.

```bash
uv run streamlit run developer_ui/app.py
```
