import pytest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_agent_import():
    import self_improving_agent
    from self_improving_agent.agent import self_improving_agent as agent
    assert agent is not None

def test_config_loading():
    from self_improving_agent.config import config
    assert config.LLM_BASE_URL is not None
    assert config.LLM_MODEL is not None

def test_agent_instantiation():
    from self_improving_agent.agent import self_improving_agent as agent
    assert agent.name == "self_improving_agent"

@patch("litellm.completion")
def test_fallback_on_llm_error(mock_completion):
    mock_completion.side_effect = Exception("Connection refused")
    
    from self_improving_agent.agent import handle_user_message
    
    response = handle_user_message("Hello")
    assert "Unable to connect to the configured LLM service" in response
    assert "Verify that the Docker Llama 3.2 container is" in response
