import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from self_improving_agent.memory.database import get_connection
from self_improving_agent.memory.retrieval import search_lessons

st.set_page_config(page_title="Lessons", layout="wide")
st.title("Extracted Lessons")

conn = get_connection()

st.header("Recent Lessons")
try:
    df = pd.read_sql_query("""
        SELECT l.id, l.lesson_text, l.lesson_type, l.confidence, l.source_experience_id, l.source_evaluation_id, l.created_at
        FROM lessons l
        ORDER BY l.created_at DESC
    """, conn)
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.metric("Total Lessons", len(df))
        
        st.header("Graph View")
        selected_lesson_id = st.selectbox("Select Lesson ID to view source graph", df["id"].tolist())
        
        if selected_lesson_id:
            import graphqlite
            db = graphqlite.wrap(conn)
            
            # Find evaluation that produced this lesson
            res = list(db.cypher(f"MATCH (eval:Evaluation)-[:PRODUCES_LESSON]->(l:Lesson {{id: {selected_lesson_id}}}) RETURN eval.id"))
            
            if res:
                eval_id = res[0]["eval.id"]
                st.success(f"This lesson was produced by Evaluation ID: {eval_id}")
                
                # Fetch evaluation details
                cursor = conn.cursor()
                cursor.execute("SELECT correct, quality, reason FROM evaluations WHERE id = ?", (eval_id,))
                row = cursor.fetchone()
                if row:
                    st.write("**Evaluation Correctness:**", row["correct"])
                    st.write("**Evaluation Quality:**", row["quality"])
                    st.write("**Evaluation Reason:**", row["reason"])
            else:
                st.info("No evaluations linked to this lesson.")
                
    else:
        st.info("No lessons found.")
except Exception as e:
    st.error(f"Could not load lessons: {e}")
finally:
    conn.close()

st.header("Semantic Lesson Search")
query = st.text_input("Enter a query to search relevant lessons:")
if st.button("Search Lessons") and query:
    with st.spinner("Searching..."):
        results = search_lessons(query)
        if not results:
            st.info("No relevant lessons found.")
        else:
            st.write(f"Found {len(results)} relevant lessons:")
            for idx, res in enumerate(results):
                st.markdown(f"**{idx+1}. {res.lesson_text}** (Distance: {res.distance:.4f})")
