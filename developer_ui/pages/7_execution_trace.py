import streamlit as st
import sqlite3
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from self_improving_agent.memory.database import get_connection

st.set_page_config(page_title="Execution Trace", layout="wide")
st.title("🔍 Execution Trace")

st.markdown("Observe multi-agent workflow executions and individual agent steps.")

conn = get_connection()
try:
    df_wf = pd.read_sql_query("SELECT id, workflow_id, task_type, status, success, quality, duration_ms, created_at FROM workflow_executions ORDER BY created_at DESC", conn)
    
    if df_wf.empty:
        st.info("No executions recorded yet.")
    else:
        st.subheader("Recent Workflow Executions")
        st.dataframe(df_wf, use_container_width=True)
        
        st.subheader("Agent Steps per Execution")
        selected_exec_id = st.selectbox("Select Workflow Execution ID:", df_wf['id'].tolist())
        
        if selected_exec_id:
            df_agents = pd.read_sql_query("SELECT agent_id, status, duration_ms, confidence, created_at FROM agent_executions WHERE workflow_execution_id = ? ORDER BY created_at ASC", conn, params=(selected_exec_id,))
            st.table(df_agents)
            
except Exception as e:
    st.error(f"Failed to load execution trace: {e}")
finally:
    conn.close()
