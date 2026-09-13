import json
import logging
from self_improving_agent.memory.database import get_connection, serialize_f32
from self_improving_agent.memory.embeddings import generate_embedding

logger = logging.getLogger(__name__)

def store_experience(task_text: str, response_text: str, status: str = "success", task_type: str = "general", metadata: dict = None):
    """Store an experience and its semantic vector in the database."""
    try:
        embedding = generate_embedding(task_text)
    except Exception as e:
        logger.warning(f"Could not generate embedding, skipping memory storage: {e}")
        return

    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Insert into experiences
        cursor.execute("""
            INSERT INTO experiences (task_text, task_type, response_text, status, metadata_json)
            VALUES (?, ?, ?, ?, ?)
        """, (task_text, task_type, response_text, status, json.dumps(metadata) if metadata else None))
        
        experience_id = cursor.lastrowid
        
        # Insert into experience_vectors
        embedding_bytes = serialize_f32(embedding)
        cursor.execute("""
            INSERT INTO experience_vectors (experience_id, embedding)
            VALUES (?, ?)
        """, (experience_id, embedding_bytes))
        
        conn.commit()
        return experience_id
    except Exception as e:
        logger.error(f"Error storing experience: {e}")
        conn.rollback()
        return -1
    finally:
        conn.close()

def store_evaluation(experience_id: int, correct: str, quality: str, confidence: str, reason: str) -> int:
    """Store an evaluation of an experience.
    
    Args:
        correct: 'true', 'false', or 'unknown'
        quality: 'excellent', 'good', 'acceptable', or 'poor'
        confidence: 'high', 'medium', or 'low'
    """
    if correct not in ("true", "false", "unknown"):
        correct = "unknown"
        
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO evaluations (experience_id, correct, quality, confidence, reason)
            VALUES (?, ?, ?, ?, ?)
        """, (experience_id, correct, quality, confidence, reason))
        
        evaluation_id = cursor.lastrowid
        conn.commit()
        return evaluation_id
    except Exception as e:
        logger.error(f"Error storing evaluation: {e}")
        conn.rollback()
        return -1
    finally:
        conn.close()

def store_lesson(lesson_text: str, lesson_type: str, experience_id: int, evaluation_id: int, confidence: str) -> int:
    """Store an extracted lesson and its semantic vector."""
    try:
        embedding = generate_embedding(lesson_text)
    except Exception as e:
        logger.warning(f"Could not generate embedding for lesson, skipping: {e}")
        return -1
        
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO lessons (lesson_text, lesson_type, source_experience_id, source_evaluation_id, confidence)
            VALUES (?, ?, ?, ?, ?)
        """, (lesson_text, lesson_type, experience_id, evaluation_id, confidence))
        
        lesson_id = cursor.lastrowid
        
        embedding_bytes = serialize_f32(embedding)
        cursor.execute("""
            INSERT INTO lesson_vectors (lesson_id, embedding)
            VALUES (?, ?)
        """, (lesson_id, embedding_bytes))
        
        conn.commit()
        return lesson_id
    except Exception as e:
        logger.error(f"Error storing lesson: {e}")
        conn.rollback()
        return -1
    finally:
        conn.close()

def store_strategy_execution(exec_id: str, strategy_id: str, task_type: str, experience_id: int, start: str, end: str, duration_ms: int, status: str):
    """Store strategy execution."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO strategy_executions (id, strategy_id, task_type, experience_id, execution_start, execution_end, duration_ms, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (exec_id, strategy_id, task_type, experience_id, start, end, duration_ms, status))
        conn.commit()
    except Exception as e:
        logger.error(f"Error storing strategy execution: {e}")
        conn.rollback()
    finally:
        conn.close()

def store_strategy_performance(perf_id: str, strategy_id: str, task_type: str, experience_id: int, evaluation_id: int, success: bool, quality: str, confidence: str, duration_ms: int):
    """Store strategy performance evaluation."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO strategy_performance (id, strategy_id, task_type, experience_id, evaluation_id, success, quality, confidence, duration_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (perf_id, strategy_id, task_type, experience_id, evaluation_id, success, quality, confidence, duration_ms))
        conn.commit()
    except Exception as e:
        logger.error(f"Error storing strategy performance: {e}")
        conn.rollback()
    finally:
        conn.close()

def update_strategy_preference(pref_id: str, task_type: str, strategy_id: str, score: float, rank: int, confidence: str, sample_count: int, reason: str):
    """Update or insert strategy preference."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO strategy_preferences (id, task_type, strategy_id, score, rank, confidence, sample_count, reason, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (pref_id, task_type, strategy_id, score, rank, confidence, sample_count, reason))
        conn.commit()
    except Exception as e:
        logger.error(f"Error updating strategy preference: {e}")
        conn.rollback()
    finally:
        conn.close()

