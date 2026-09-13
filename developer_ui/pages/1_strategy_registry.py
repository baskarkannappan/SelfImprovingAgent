import streamlit as st
import pandas as pd
from self_improving_agent.memory.database import get_connection

st.set_page_config(page_title="Strategy Registry", layout="wide")
st.title("Strategy Registry")
st.write("This page shows all predefined strategies in the deterministic registry.")

conn = get_connection()
try:
    df = pd.read_sql_query("SELECT * FROM strategies", conn)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No strategies found in the database. Run a task to trigger initial sync.")
except Exception as e:
    st.error(f"Error loading strategies: {e}")
finally:
    conn.close()
