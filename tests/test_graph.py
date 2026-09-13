import pytest
from self_improving_agent.graph import link_experience_to_evaluation, link_evaluation_to_lesson
from self_improving_agent.memory.database import get_connection
import graphqlite

def test_graph_relationships():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO experiences (id, task_text, response_text, status) VALUES (1001, 'Task', 'Resp', 'success')")
        cursor.execute("INSERT INTO evaluations (id, experience_id, correct) VALUES (2001, 1001, 'true')")
        cursor.execute("INSERT INTO lessons (id, lesson_text) VALUES (3001, 'Lesson')")
        conn.commit()
    except:
        pass # Might already exist
        
    link_experience_to_evaluation(1001, 2001)
    link_evaluation_to_lesson(2001, 3001)
    
    try:
        db = graphqlite.wrap(conn)
        
        # Verify edge 1
        res = list(db.cypher("MATCH (e:Experience {id: 1001})-[:EVALUATED_BY]->(eval:Evaluation) RETURN eval.id"))
        assert len(res) == 1
        assert res[0]["eval.id"] == 2001
        
        # Verify edge 2
        res2 = list(db.cypher("MATCH (eval:Evaluation {id: 2001})-[:PRODUCES_LESSON]->(l:Lesson) RETURN l.id"))
        assert len(res2) == 1
        assert res2[0]["l.id"] == 3001
    finally:
        conn.close()
