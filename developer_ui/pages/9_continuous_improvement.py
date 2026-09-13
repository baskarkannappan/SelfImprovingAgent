import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Continuous Improvement", page_icon="📈", layout="wide")

st.title("📈 Continuous Improvement Validation")
st.markdown("Compare the **Baseline** (empty history) vs **Post-Learning** (with accumulated experiences) benchmark runs.")

REPORTS_DIR = "reports"

def load_reports():
    if not os.path.exists(REPORTS_DIR):
        return []
    
    reports = []
    for filename in os.listdir(REPORTS_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(REPORTS_DIR, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    reports.append(data)
            except Exception as e:
                st.error(f"Failed to load {filename}: {str(e)}")
    
    return sorted(reports, key=lambda x: x.get("timestamp", ""), reverse=True)

reports = load_reports()

if not reports:
    st.info("No benchmark reports found. Run `uv run python -m self_improving_agent.benchmark.runner --mode baseline` to generate the first one.")
    st.stop()

# Group by phase
baseline_reports = [r for r in reports if r["phase"] == "baseline"]
learning_reports = [r for r in reports if r["phase"] == "post_learning"]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Select Baseline Run")
    baseline_options = {f"{r['timestamp']} ({r['total_tasks']} tasks)": r for r in baseline_reports}
    if not baseline_options:
        st.warning("No baseline reports available.")
        selected_baseline = None
    else:
        selected_baseline_key = st.selectbox("Baseline:", list(baseline_options.keys()), index=0)
        selected_baseline = baseline_options[selected_baseline_key]

with col2:
    st.subheader("Select Post-Learning Run")
    learning_options = {f"{r['timestamp']} ({r['total_tasks']} tasks)": r for r in learning_reports}
    if not learning_options:
        st.warning("No post-learning reports available.")
        selected_learning = None
    else:
        selected_learning_key = st.selectbox("Post-Learning:", list(learning_options.keys()), index=0)
        selected_learning = learning_options[selected_learning_key]

st.divider()

if selected_baseline and selected_learning:
    st.header("Metrics Comparison")
    
    m1, m2, m3, m4, m5 = st.columns(5)
    
    # Success Rate
    bl_success = selected_baseline["success_rate"]
    pl_success = selected_learning["success_rate"]
    delta_success = pl_success - bl_success
    m1.metric("Success Rate", f"{pl_success*100:.1f}%", f"{delta_success*100:.1f}%")
    
    # Average Quality
    bl_quality = selected_baseline["average_quality"]
    pl_quality = selected_learning["average_quality"]
    delta_quality = pl_quality - bl_quality
    m2.metric("Avg Quality (1-4)", f"{pl_quality:.2f}", f"{delta_quality:.2f}")
    
    # Latency
    bl_latency = selected_baseline["average_latency_ms"]
    pl_latency = selected_learning["average_latency_ms"]
    delta_latency = pl_latency - bl_latency
    m3.metric("Avg Latency (ms)", f"{pl_latency}", f"{delta_latency}ms", delta_color="inverse")
    
    # Lessons Reused
    bl_reused = selected_baseline.get("lessons_reused", 0)
    pl_reused = selected_learning.get("lessons_reused", 0)
    delta_reused = pl_reused - bl_reused
    m4.metric("Lessons Reused", f"{pl_reused}", f"{delta_reused}")
    
    # Improvement Invocations
    bl_improv = selected_baseline.get("improvement_invocations", 0)
    pl_improv = selected_learning.get("improvement_invocations", 0)
    delta_improv = pl_improv - bl_improv
    m5.metric("Critic Interventions", f"{pl_improv}", f"{delta_improv}", delta_color="inverse")
    
    st.divider()
    
    st.header("Task Breakdown")
    
    # Build comparison dataframe
    bl_tasks = {t["task_id"]: t for t in selected_baseline.get("task_results", [])}
    pl_tasks = {t["task_id"]: t for t in selected_learning.get("task_results", [])}
    
    all_task_ids = sorted(list(set(bl_tasks.keys()).union(set(pl_tasks.keys()))))
    
    rows = []
    for tid in all_task_ids:
        bl = bl_tasks.get(tid, {})
        pl = pl_tasks.get(tid, {})
        
        rows.append({
            "Task ID": tid,
            "Prompt": pl.get("task_text", bl.get("task_text", "")),
            "Baseline Correct": "✅" if bl.get("correct") else "❌",
            "Learning Correct": "✅" if pl.get("correct") else "❌",
            "Baseline Quality": bl.get("quality", "N/A"),
            "Learning Quality": pl.get("quality", "N/A"),
            "Baseline Strategy": bl.get("selected_strategy", "N/A"),
            "Learning Strategy": pl.get("selected_strategy", "N/A"),
            "Delta Latency (ms)": pl.get("duration_ms", 0) - bl.get("duration_ms", 0)
        })
    
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("You need at least one baseline and one post-learning report to compare.")
