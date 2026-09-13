import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from self_improving_agent.memory.database import get_connection

st.set_page_config(page_title="Evaluations", layout="wide")
st.title("Evaluations")

conn = get_connection()

st.header("Recent Evaluations")
try:
    df = pd.read_sql_query("""
        SELECT e.id, e.experience_id, e.correct, e.quality, e.confidence, e.reason, e.created_at, exp.task_text, exp.response_text
        FROM evaluations e
        JOIN experiences exp ON e.experience_id = exp.id
        ORDER BY e.created_at DESC
    """, conn)
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.metric("Total Evaluations", len(df))
        
        st.header("Graph View")
        selected_eval_id = st.selectbox("Select Evaluation ID to view graph connections", df["id"].tolist())
        
        if selected_eval_id:
            import graphqlite
            db = graphqlite.wrap(conn)
            
            # Find lesson connected to this evaluation
            res = list(db.cypher(f"MATCH (eval:Evaluation {{id: {selected_eval_id}}})-[:PRODUCES_LESSON]->(l:Lesson) RETURN l.id"))
            
            if res:
                lesson_id = res[0]["l.id"]
                st.success(f"This evaluation produced Lesson ID: {lesson_id}")
                
                # Fetch lesson details
                cursor = conn.cursor()
                cursor.execute("SELECT lesson_text, lesson_type, confidence FROM lessons WHERE id = ?", (lesson_id,))
                row = cursor.fetchone()
                if row:
                    st.write("**Extracted Lesson:**", row["lesson_text"])
                    st.write("**Type:**", row["lesson_type"])
                    st.write("**Confidence:**", row["confidence"])
            else:
                st.info("No lessons produced from this evaluation.")
    else:
        st.info("No evaluations found.")
except Exception as e:
    st.error(f"Could not load evaluations: {e}")
finally:
    conn.close()
