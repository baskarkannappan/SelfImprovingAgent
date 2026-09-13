Write-Host "Running Baseline Benchmark..."
uv run python -m self_improving_agent.benchmark.runner --mode baseline

Write-Host "Waiting 5 seconds..."
Start-Sleep -Seconds 5

Write-Host "Running Post-Learning Benchmark..."
uv run python -m self_improving_agent.benchmark.runner --mode post_learning

Write-Host "Done! Check Streamlit UI."
