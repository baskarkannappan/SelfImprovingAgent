import sqlite3
import sqlite_vec
import struct
from pathlib import Path
from ..config import config

def get_connection() -> sqlite3.Connection:
    """Get a connection to the SQLite database with sqlite-vec loaded."""
    db_path = Path(config.DATABASE_PATH)
    
    # Ensure parent directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    
    import graphqlite
    graphqlite.load(conn)
    
    conn.enable_load_extension(False)
    return conn

def serialize_f32(vector: list[float]) -> bytes:
    """serializes a list of floats into a compact format expected by sqlite-vec"""
    return struct.pack("%sf" % len(vector), *vector)

def initialize_database():
    """Create the experiences and experience_vectors tables if they don't exist."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Create experiences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS experiences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_text TEXT NOT NULL,
                task_type TEXT DEFAULT 'general',
                response_text TEXT NOT NULL,
                status TEXT NOT NULL,
                metadata_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create experience_vectors virtual table
        # nomic-embed-text generates 768-dimensional vectors
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS experience_vectors USING vec0(
                experience_id INTEGER PRIMARY KEY,
                embedding float[768]
            )
        """)
        # Create evaluations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experience_id INTEGER,
                correct TEXT CHECK(correct IN ('true', 'false', 'unknown')),
                quality TEXT CHECK(quality IN ('excellent', 'good', 'acceptable', 'poor')),
                confidence TEXT CHECK(confidence IN ('high', 'medium', 'low')),
                reason TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(experience_id) REFERENCES experiences(id)
            )
        """)
        
        # Create lessons table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lesson_text TEXT NOT NULL,
                lesson_type TEXT,
                source_experience_id INTEGER,
                source_evaluation_id INTEGER,
                confidence TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(source_experience_id) REFERENCES experiences(id),
                FOREIGN KEY(source_evaluation_id) REFERENCES evaluations(id)
            )
        """)
        
        # Create lesson_vectors virtual table
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS lesson_vectors USING vec0(
                lesson_id INTEGER PRIMARY KEY,
                embedding float[768]
            )
        """)
        
        # Create strategies table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS strategies (
                id TEXT PRIMARY KEY,
                description TEXT NOT NULL,
                prompt TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS strategy_executions (
                id TEXT PRIMARY KEY,
                strategy_id TEXT,
                task_type TEXT,
                experience_id INTEGER,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                duration_ms INTEGER,
                status TEXT,
                FOREIGN KEY (strategy_id) REFERENCES strategies (id),
                FOREIGN KEY (experience_id) REFERENCES experiences (id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS strategy_preferences (
                task_type TEXT,
                strategy_id TEXT,
                score REAL,
                sample_count INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (task_type, strategy_id),
                FOREIGN KEY (strategy_id) REFERENCES strategies (id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workflows (
                id TEXT PRIMARY KEY,
                name TEXT,
                task_type TEXT,
                agents_sequence TEXT,
                enabled BOOLEAN DEFAULT 1
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workflow_executions (
                id TEXT PRIMARY KEY,
                workflow_id TEXT,
                task_type TEXT,
                experience_id INTEGER,
                status TEXT,
                success BOOLEAN,
                quality TEXT,
                duration_ms INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(workflow_id) REFERENCES workflows(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_executions (
                id TEXT PRIMARY KEY,
                workflow_execution_id TEXT,
                agent_id TEXT,
                status TEXT,
                duration_ms INTEGER,
                confidence TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(workflow_execution_id) REFERENCES workflow_executions(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workflow_preferences (
                task_type TEXT PRIMARY KEY,
                workflow_id TEXT,
                score REAL,
                sample_count INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(workflow_id) REFERENCES workflows(id)
            )
        """)
        
        conn.commit()
    finally:
        conn.close()

def clear_all_data():
    """Clear all data from the database and graph."""
    conn = get_connection()
    try:
        # Clear graph nodes and edges
        import graphqlite
        db = graphqlite.wrap(conn)
        db.cypher("MATCH (n) DETACH DELETE n")
        
        # Clear relational tables and vector tables
        cursor = conn.cursor()
        cursor.execute("DELETE FROM strategy_preferences")
        cursor.execute("DELETE FROM strategy_performance")
        cursor.execute("DELETE FROM strategy_executions")
        cursor.execute("DELETE FROM strategies")
        cursor.execute("DELETE FROM lessons")
        cursor.execute("DELETE FROM lesson_vectors")
        cursor.execute("DELETE FROM evaluations")
        cursor.execute("DELETE FROM experiences")
        cursor.execute("DELETE FROM experience_vectors")
        
        conn.commit()
    except Exception as e:
        print(f"Error clearing data: {e}")
    finally:
        conn.close()

def get_strategy_stats(task_type: str, strategy_id: str) -> dict:
    """Aggregate performance data for a strategy."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as sample_count,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success_count,
                SUM(CASE WHEN quality = 'excellent' THEN 3
                         WHEN quality = 'good' THEN 2
                         WHEN quality = 'acceptable' THEN 1
                         ELSE 0 END) as quality_sum,
                SUM(CASE WHEN confidence = 'high' THEN 3
                         WHEN confidence = 'medium' THEN 2
                         WHEN confidence = 'low' THEN 1
                         ELSE 0 END) as confidence_sum,
                AVG(duration_ms) as avg_duration_ms
            FROM strategy_performance
            WHERE task_type = ? AND strategy_id = ?
        """, (task_type, strategy_id))
        
        row = cursor.fetchone()
        if not row or row["sample_count"] == 0:
            return None
            
        stats = dict(row)
        sample_count = stats["sample_count"]
        
        # Calculate rates
        stats["success_rate"] = stats["success_count"] / sample_count
        stats["avg_quality_score"] = stats["quality_sum"] / (sample_count * 3) # normalized 0-1
        stats["avg_confidence_score"] = stats["confidence_sum"] / (sample_count * 3) # normalized 0-1
        
        return stats
    except Exception as e:
        print(f"Error getting strategy stats: {e}")
        return None
    finally:
        conn.close()

if __name__ == "__main__":
    initialize_database()
