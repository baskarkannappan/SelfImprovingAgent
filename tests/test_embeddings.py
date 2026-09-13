import pytest
from unittest.mock import patch, MagicMock
from self_improving_agent.memory.embeddings import generate_embedding
import litellm

@patch("self_improving_agent.memory.embeddings.embedding")
def test_generate_embedding_success(mock_embedding):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.data = [{"embedding": [0.1, 0.2, 0.3]}]
    mock_embedding.return_value = mock_response

    # Test
    result = generate_embedding("test text")
    
    assert result == [0.1, 0.2, 0.3]
    mock_embedding.assert_called_once()
    kwargs = mock_embedding.call_args.kwargs
    assert kwargs["input"] == ["test text"]
    assert "ollama/nomic-embed-text" in kwargs["model"]

@patch("self_improving_agent.memory.embeddings.embedding")
def test_generate_embedding_failure(mock_embedding):
    mock_embedding.side_effect = Exception("API error")
    
    with pytest.raises(Exception, match="API error"):
        generate_embedding("test text")
