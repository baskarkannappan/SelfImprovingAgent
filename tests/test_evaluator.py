import pytest
from unittest.mock import patch, MagicMock
from self_improving_agent.evaluator import Evaluator

@pytest.fixture
def evaluator():
    return Evaluator()

@patch('litellm.completion')
def test_evaluate_subjective_answer(mock_completion, evaluator):
    # Setup mock response
    mock_res = MagicMock()
    mock_res.choices = [
        MagicMock(message=MagicMock(content='{"correct": "true", "quality": "excellent", "confidence": "high", "reason": "Accurate"}'))
    ]
    mock_completion.return_value = mock_res
    
    # Run evaluation
    result = evaluator.evaluate("What is 2+2?", "4")
    
    assert result["correct"] == "true"
    assert result["quality"] == "excellent"
    assert result["confidence"] == "high"
    assert "Accurate" in result["reason"]
