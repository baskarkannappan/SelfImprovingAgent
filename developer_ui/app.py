import streamlit as st
import sqlite3
import pandas as pd
import sys
import os

# Ensure we can import the agent packages
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from self_improving_agent.memory.database import get_connection, initialize_database
from self_improving_agent.memory.retrieval import retrieve_similar_experiences

st.set_page_config(page_title="Semantic Memory Viewer", layout="wide")
st.title("Semantic Memory Developer UI")

# Initialize database to ensure tables exist
try:
    initialize_database()
except Exception as e:
    st.sidebar.error(f"Failed to initialize database: {e}")

# Check database connection
try:
    conn = get_connection()
    st.sidebar.success("Connected to Memory Database")
except Exception as e:
    st.sidebar.error(f"Failed to connect to database: {e}")
    st.stop()

st.sidebar.markdown("---")

st.sidebar.markdown("---")
st.sidebar.markdown("### Phase 4: Strategy Optimization")
st.sidebar.page_link("pages/1_strategy_registry.py", label="Strategy Registry", icon="📚")
st.sidebar.page_link("pages/2_strategy_performance.py", label="Strategy Performance", icon="📊")
st.sidebar.page_link("pages/3_strategy_preferences.py", label="Strategy Preferences", icon="🎯")

st.sidebar.markdown("---")
st.sidebar.markdown("### Phase 5: Multi-Agent")
st.sidebar.page_link("pages/5_agent_registry.py", label="Agent Registry", icon="🤖")
st.sidebar.page_link("pages/6_workflow_registry.py", label="Workflow Registry", icon="📜")
st.sidebar.page_link("pages/7_execution_trace.py", label="Execution Trace", icon="🔍")
st.sidebar.page_link("pages/8_workflow_preferences.py", label="Workflow Preferences", icon="🧠")

st.sidebar.markdown("---")
if st.sidebar.button("Clear All Data"):
    from self_improving_agent.memory.database import clear_all_data
    with st.spinner("Clearing all data (relational, vectors, graph)..."):
        clear_all_data()
        st.sidebar.success("Database cleared!")
        st.rerun()

st.sidebar.markdown("---")

view_mode = st.sidebar.radio("Navigation", ["Database Overview & Experiences", "Vector Data", "Semantic Search"])

if view_mode == "Database Overview & Experiences":
    st.header("Experiences")
    try:
        df = pd.read_sql_query("SELECT id, task_text, task_type, response_text, status, created_at FROM experiences ORDER BY created_at DESC", conn)
        st.dataframe(df, use_container_width=True)
        st.metric("Total Experiences", len(df))
    except Exception as e:
        st.error(f"Could not load experiences: {e}")

elif view_mode == "Vector Data":
    st.header("Vector Embeddings")
    try:
        # We don't want to load thousands of 768-d floats into pandas directly if it's large, but for POC it's fine
        # We can just show the experience_id and a preview of the embedding
        cursor = conn.cursor()
        cursor.execute("SELECT experience_id, vec_to_json(embedding) as embedding_preview FROM experience_vectors LIMIT 100")
        rows = cursor.fetchall()
        data = []
        for r in rows:
            data.append({"Experience ID": r['experience_id'], "Embedding (JSON)": r['embedding_preview'][:200] + "..."})
            
        df_vec = pd.DataFrame(data)
        st.dataframe(df_vec, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load vector data: {e}")

elif view_mode == "Semantic Search":
    st.header("Test Semantic Search")
    query = st.text_input("Enter a test query to find similar experiences:")
    top_k = st.slider("Top K", min_value=1, max_value=10, value=3)
    threshold = st.slider("Similarity Threshold (1.0 = exact match)", min_value=0.0, max_value=1.0, value=0.0, step=0.05)
    
    if st.button("Search Similar Memories") and query:
        with st.spinner("Generating embedding and searching..."):
            try:
                results = retrieve_similar_experiences(query, top_k=top_k, threshold=threshold)
                if not results:
                    st.info("No experiences found matching the criteria.")
                else:
                    st.write(f"Found {len(results)} matching experiences:")
                    for idx, res in enumerate(results):
                        with st.expander(f"Match #{idx+1} (Distance: {res.distance:.4f})"):
                            st.markdown(f"**Task**: {res.task_text}")
                            st.markdown(f"**Response**: {res.response_text}")
            except Exception as e:
                st.error(f"Search failed: {e}")

conn.close()
