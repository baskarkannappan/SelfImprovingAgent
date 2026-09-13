import pytest
import sqlite3
from unittest.mock import patch, MagicMock
from self_improving_agent.strategy.selector import recalculate_strategy_preferences
from self_improving_agent.memory.database import get_connection, clear_all_data

def test_recalculate_strategy_preferences_scoring():
    """Test that the deterministic score is calculated correctly."""
    
    # Mock get_strategy_stats to return known values
    with patch('self_improving_agent.memory.database.get_strategy_stats') as mock_stats:
        mock_stats.return_value = {
            "sample_count": 5,
            "success_rate": 0.8,  # 80% success
            "avg_quality_score": 0.5, # 50% quality
            "avg_confidence_score": 1.0 # 100% confidence
        }
        
        # Expected score = (0.8 * 0.6) + (0.5 * 0.3) + (1.0 * 0.1) = 0.48 + 0.15 + 0.10 = 0.73
        
        # Mock the DB update to catch the score
        with patch('self_improving_agent.memory.memory.update_strategy_preference') as mock_update:
            recalculate_strategy_preferences("calculation", "strat_1")
            
            mock_update.assert_called_once()
            args, kwargs = mock_update.call_args
            assert kwargs["score"] == pytest.approx(0.73)
            assert kwargs["confidence"] == "high" # Because sample_count >= 5 (assuming config=5)
