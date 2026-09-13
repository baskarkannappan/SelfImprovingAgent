import streamlit as st
import sqlite3
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from self_improving_agent.memory.database import get_connection

st.set_page_config(page_title="Workflow Registry", layout="wide")
st.title("📜 Workflow Registry")

st.markdown("This page displays dynamically generated multi-agent workflows.")

conn = get_connection()
try:
    df = pd.read_sql_query("SELECT id, task_type, agents_sequence, enabled FROM workflows", conn)
    if df.empty:
        st.info("No workflows recorded yet. Send a message to the agent to generate a workflow.")
    else:
        st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"Failed to load workflows: {e}")
finally:
    conn.close()
