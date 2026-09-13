import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch
from self_improving_agent.memory.memory import store_experience
from self_improving_agent.memory.retrieval import retrieve_similar_experiences, build_memory_context
from self_improving_agent.memory.database import initialize_database, get_connection

@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test.db"
    with patch("self_improving_agent.memory.database.config.DATABASE_PATH", str(db_file)):
        initialize_database()
        yield str(db_file)

@pytest.fixture
def mock_embedding():
    # Return a dummy vector generator to avoid hitting Ollama in tests
    with patch("self_improving_agent.memory.embeddings.embedding") as mock_emb:
        def side_effect(*args, **kwargs):
            text = kwargs.get("input", [""])[0]
            # Simple dummy: 768 length array
            # We differentiate "test1" vs "test2"
            vec = [0.1] * 768
            if "hello" in text.lower():
                vec = [0.5] * 768
            class MockResponse:
                data = [{"embedding": vec}]
            return MockResponse()
        mock_emb.side_effect = side_effect
        yield mock_emb

def test_store_and_retrieve(temp_db, mock_embedding):
    store_experience("say hello", "hello there!")
    store_experience("calculate 2+2", "4")
    
    # Retrieve
    results = retrieve_similar_experiences("hello world", top_k=1, threshold=0.0)
    assert len(results) == 1
    assert results[0].task_text == "say hello"
    assert results[0].response_text == "hello there!"
    
def test_fallback_empty_db(temp_db, mock_embedding):
    results = retrieve_similar_experiences("hello world", top_k=1, threshold=0.0)
    assert len(results) == 0
    
def test_build_memory_context():
    from self_improving_agent.memory.retrieval import Experience
    exps = [
        Experience(id=1, task_text="q1", response_text="a1", status="success"),
        Experience(id=2, task_text="q2", response_text="a2", status="error")
    ]
    context = build_memory_context(exps)
    assert "Past Request: q1" in context
    assert "Past Response: a1" in context
    assert "q2" not in context # Errors are skipped
