import streamlit as st
import pandas as pd
from self_improving_agent.memory.database import get_connection

st.set_page_config(page_title="Strategy Performance", layout="wide")
st.title("Strategy Performance")
st.write("Recent strategy executions and their evaluations.")

conn = get_connection()
try:
    df_perf = pd.read_sql_query("""
        SELECT sp.id, sp.task_type, sp.strategy_id, s.name as strategy_name, 
               sp.success, sp.quality, sp.confidence, sp.duration_ms, sp.created_at
        FROM strategy_performance sp
        JOIN strategies s ON sp.strategy_id = s.id
        ORDER BY sp.created_at DESC
        LIMIT 100
    """, conn)
    
    if not df_perf.empty:
        st.dataframe(df_perf, use_container_width=True)
    else:
        st.info("No performance records found yet.")
except Exception as e:
    st.error(f"Error loading performance: {e}")
finally:
    conn.close()
