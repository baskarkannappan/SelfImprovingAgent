import streamlit as st
import sqlite3
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from self_improving_agent.memory.database import get_connection

st.set_page_config(page_title="Workflow Preferences", layout="wide")
st.title("🧠 Workflow Preferences")

st.markdown("Displays the dynamically learned optimal workflows for each task type.")

conn = get_connection()
try:
    df = pd.read_sql_query("SELECT task_type, workflow_id, score, sample_count, updated_at FROM workflow_preferences ORDER BY score DESC", conn)
    if df.empty:
        st.info("No workflow preferences learned yet. Run more tasks to generate data.")
    else:
        st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"Failed to load workflow preferences: {e}")
finally:
    conn.close()
