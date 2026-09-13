import json
from dataclasses import dataclass
from typing import List, Optional
from self_improving_agent.memory.database import get_connection, serialize_f32
from self_improving_agent.memory.embeddings import generate_embedding
from self_improving_agent.config import config
import logging

logger = logging.getLogger(__name__)

@dataclass
class Experience:
    id: int
    task_text: str
    response_text: str
    status: str
    distance: float = 0.0

def retrieve_similar_experiences(query: str, top_k: int = None, threshold: float = None) -> List[Experience]:
    """Retrieve experiences that are semantically similar to the query."""
    if top_k is None:
        top_k = config.MEMORY_TOP_K
    if threshold is None:
        threshold = config.MEMORY_SIMILARITY_THRESHOLD
        
    try:
        query_embedding = generate_embedding(query)
    except Exception as e:
        logger.warning(f"Could not generate embedding for memory retrieval: {e}")
        return []
        
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # SQLite-vec distance query
        # vec_distance_cosine returns cosine distance (1 - cosine_similarity).
        # A smaller distance is better.
        # So we filter by distance <= (1 - threshold)
        
        max_distance = 1.0 - threshold
        
        query_bytes = serialize_f32(query_embedding)
        
        cursor.execute("""
            SELECT e.id, e.task_text, e.response_text, e.status, 
                   vec_distance_cosine(v.embedding, ?) as distance
            FROM experiences e
            JOIN experience_vectors v ON e.id = v.experience_id
            WHERE vec_distance_cosine(v.embedding, ?) <= ?
            ORDER BY distance ASC
            LIMIT ?
        """, (query_bytes, query_bytes, max_distance, top_k))
        
        results = []
        for row in cursor.fetchall():
            results.append(Experience(
                id=row['id'],
                task_text=row['task_text'],
                response_text=row['response_text'],
                status=row['status'],
                distance=row['distance']
            ))
            
        return results
    except Exception as e:
        logger.error(f"Error retrieving similar experiences: {e}")
        return []
    finally:
        conn.close()

def build_memory_context(experiences: List[Experience]) -> str:
    """Format experiences into a context block for the LLM prompt."""
    if not experiences:
        return ""
        
    context_lines = ["\n[Context from past experiences]"]
    for exp in experiences:
        if exp.status == "success":
            context_lines.append(f"Past Request: {exp.task_text}\nPast Response: {exp.response_text}")
    
    context_lines.append("[End of context]\n")
    return "\n".join(context_lines)

@dataclass
class Lesson:
    id: int
    lesson_text: str
    lesson_type: str
    confidence: str
    distance: float = 0.0

def search_lessons(query: str, top_k: int = 3, threshold: float = 0.5) -> List[Lesson]:
    """Retrieve semantically relevant lessons."""
    try:
        query_embedding = generate_embedding(query)
    except Exception as e:
        logger.warning(f"Could not generate embedding for lesson search: {e}")
        return []
        
    conn = get_connection()
    try:
        cursor = conn.cursor()
        max_distance = 1.0 - threshold
        query_bytes = serialize_f32(query_embedding)
        
        cursor.execute("""
            SELECT l.id, l.lesson_text, l.lesson_type, l.confidence, 
                   vec_distance_cosine(v.embedding, ?) as distance
            FROM lessons l
            JOIN lesson_vectors v ON l.id = v.lesson_id
            WHERE vec_distance_cosine(v.embedding, ?) <= ?
            ORDER BY distance ASC
            LIMIT ?
        """, (query_bytes, query_bytes, max_distance, top_k))
        
        results = []
        for row in cursor.fetchall():
            results.append(Lesson(
                id=row['id'],
                lesson_text=row['lesson_text'],
                lesson_type=row['lesson_type'],
                confidence=row['confidence'],
                distance=row['distance']
            ))
            
        return results
    except Exception as e:
        logger.error(f"Error retrieving lessons: {e}")
        return []
    finally:
        conn.close()

def build_lesson_context(lessons: List[Lesson]) -> str:
    """Format lessons into a context block for the LLM prompt."""
    if not lessons:
        return ""
        
    context_lines = ["\n[RELEVANT LESSONS FROM PAST MISTAKES]"]
    for idx, lesson in enumerate(lessons):
        context_lines.append(f"{idx+1}. {lesson.lesson_text}")
    
    context_lines.append("[END RELEVANT LESSONS]\n")
    return "\n".join(context_lines)
