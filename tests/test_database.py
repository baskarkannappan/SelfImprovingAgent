import pytest
import sqlite3
import os
from unittest.mock import patch
from self_improving_agent.memory.database import get_connection, initialize_database, serialize_f32

@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test.db"
    
    # We patch the database path to use the temp file
    with patch("self_improving_agent.memory.database.config.DATABASE_PATH", str(db_file)):
        yield str(db_file)
        
def test_initialize_database(temp_db):
    initialize_database()
    
    # Check if tables were created
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='experiences'")
    assert cursor.fetchone() is not None
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='experience_vectors'")
    assert cursor.fetchone() is not None
    
    conn.close()

def test_serialize_f32():
    vector = [0.1, 0.2, 0.3]
    serialized = serialize_f32(vector)
    assert isinstance(serialized, bytes)
    assert len(serialized) == 12 # 3 floats * 4 bytes
