import logging
import graphqlite
from self_improving_agent.memory.database import get_connection

logger = logging.getLogger(__name__)

def link_experience_to_evaluation(experience_id: int, evaluation_id: int):
    """Link an Experience to an Evaluation using GraphQLite."""
    conn = get_connection()
    try:
        # Wrap connection for Cypher support
        db = graphqlite.wrap(conn)
        
        # Create nodes and edge
        query = f"""
        MERGE (exp {{id: {experience_id}}}) SET exp:Experience
        MERGE (eval {{id: {evaluation_id}}}) SET eval:Evaluation
        MERGE (exp)-[:EVALUATED_BY]->(eval)
        """
        db.cypher(query)
        conn.commit()
    except Exception as e:
        logger.error(f"Error linking experience to evaluation: {e}")
    finally:
        conn.close()

def link_evaluation_to_lesson(evaluation_id: int, lesson_id: int):
    """Link an Evaluation to a Lesson using GraphQLite."""
    conn = get_connection()
    try:
        db = graphqlite.wrap(conn)
        
        query = f"""
        MERGE (eval {{id: {evaluation_id}}}) SET eval:Evaluation
        MERGE (lesson {{id: {lesson_id}}}) SET lesson:Lesson
        MERGE (eval)-[:PRODUCES_LESSON]->(lesson)
        """
        db.cypher(query)
        conn.commit()
    except Exception as e:
        logger.error(f"Error linking evaluation to lesson: {e}")
    finally:
        conn.close()

def link_strategy_to_workflow(strategy_id: int, workflow_id: int):
    """Link a Strategy to a Workflow execution using GraphQLite."""
    conn = get_connection()
    try:
        db = graphqlite.wrap(conn)
        query = f"""
        MERGE (strat {{id: {strategy_id}}}) SET strat:StrategyPreference
        MERGE (wf {{id: {workflow_id}}}) SET wf:WorkflowExecution
        MERGE (strat)-[:DRIVES_WORKFLOW]->(wf)
        """
        db.cypher(query)
        conn.commit()
    except Exception as e:
        logger.error(f"Error linking strategy to workflow: {e}")
    finally:
        conn.close()

def link_workflow_to_experience(workflow_id: int, experience_id: int):
    """Link a Workflow Execution to an Experience using GraphQLite."""
    conn = get_connection()
    try:
        db = graphqlite.wrap(conn)
        query = f"""
        MERGE (wf {{id: {workflow_id}}}) SET wf:WorkflowExecution
        MERGE (exp {{id: {experience_id}}}) SET exp:Experience
        MERGE (wf)-[:GENERATES_EXPERIENCE]->(exp)
        """
        db.cypher(query)
        conn.commit()
    except Exception as e:
        logger.error(f"Error linking workflow to experience: {e}")
    finally:
        conn.close()
