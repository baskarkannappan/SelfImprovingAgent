import streamlit as st
import pandas as pd
from self_improving_agent.memory.database import get_connection

st.set_page_config(page_title="Strategy Preferences", layout="wide")
st.title("Strategy Preferences (Exploitation)")
st.write("The calculated best strategies for each task type based on historical success, quality, and confidence.")

conn = get_connection()
try:
    df_pref = pd.read_sql_query("""
        SELECT sp.task_type, sp.strategy_id, s.name as strategy_name, 
               sp.score, sp.sample_count, sp.confidence, sp.reason, sp.updated_at
        FROM strategy_preferences sp
        JOIN strategies s ON sp.strategy_id = s.id
        ORDER BY sp.score DESC
    """, conn)
    
    if not df_pref.empty:
        st.dataframe(df_pref, use_container_width=True)
    else:
        st.info("No strategy preferences calculated yet. The agent is still exploring.")
except Exception as e:
    st.error(f"Error loading preferences: {e}")
finally:
    conn.close()
