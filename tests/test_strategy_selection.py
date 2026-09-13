import pytest
from unittest.mock import patch
from self_improving_agent.strategy.selector import select_strategy
from self_improving_agent.config import config

@patch('self_improving_agent.strategy.selector.get_best_strategy_from_history')
@patch('self_improving_agent.strategy.selector.random.random')
def test_select_strategy_exploration(mock_random, mock_get_best):
    """Test that it explores if random < exploration rate."""
    mock_random.return_value = 0.01  # Less than STRATEGY_EXPLORATION_RATE (0.1)
    mock_get_best.return_value = {"strategy_id": "direct_calculation"}
    
    # Even if there is a best strategy, exploration should trigger
    strat, is_exploration = select_strategy("calculation")
    
    assert is_exploration is True

@patch('self_improving_agent.strategy.selector.get_best_strategy_from_history')
@patch('self_improving_agent.strategy.selector.random.random')
def test_select_strategy_exploitation(mock_random, mock_get_best):
    """Test that it exploits if random > exploration rate and preference exists."""
    mock_random.return_value = 0.99  # Greater than STRATEGY_EXPLORATION_RATE
    mock_get_best.return_value = {"strategy_id": "verify_calculation"}
    
    strat, is_exploration = select_strategy("calculation")
    
    assert is_exploration is False
    assert strat["id"] == "verify_calculation"
