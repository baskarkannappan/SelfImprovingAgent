import pytest
from unittest.mock import patch, MagicMock
from self_improving_agent.learner import Learner

@pytest.fixture
def learner():
    return Learner()

@patch('litellm.completion')
def test_extract_lesson_from_failure(mock_completion, learner):
    # Setup mock response
    mock_res = MagicMock()
    mock_res.choices = [
        MagicMock(message=MagicMock(content='{"lesson_text": "Always verify percentages before returning.", "lesson_type": "error_prevention", "confidence": "high"}'))
    ]
    mock_completion.return_value = mock_res
    
    evaluation = {
        "correct": "false",
        "quality": "poor",
        "confidence": "high",
        "reason": "The percentage calculation is wrong."
    }
    
    # Run learner
    result = learner.extract_lesson("What is 15% of 200?", "35", evaluation)
    
    assert result is not None
    assert result["lesson_text"] == "Always verify percentages before returning."
    assert result["lesson_type"] == "error_prevention"
    assert result["confidence"] == "high"

@patch('litellm.completion')
def test_extract_no_lesson(mock_completion, learner):
    # Setup mock response indicating no lesson
    mock_res = MagicMock()
    mock_res.choices = [
        MagicMock(message=MagicMock(content='{"lesson_text": "", "lesson_type": "other", "confidence": "high"}'))
    ]
    mock_completion.return_value = mock_res
    
    evaluation = {
        "correct": "true",
        "quality": "excellent",
        "confidence": "high",
        "reason": "Accurate."
    }
    
    # Run learner
    result = learner.extract_lesson("What is 2+2?", "4", evaluation)
    
    assert result is None
