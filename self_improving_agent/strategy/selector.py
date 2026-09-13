import random
import logging
from typing import Dict, Any, Tuple
from self_improving_agent.config import config
from self_improving_agent.strategy.registry import get_strategies_by_task_type
from self_improving_agent.memory.database import get_connection

logger = logging.getLogger(__name__)

def select_strategy(task_type: str) -> Tuple[Dict[str, Any], bool]:
    """
    Selects a strategy for the given task type.
    Returns:
        Tuple of (selected_strategy_dict, is_exploration)
    """
    available_strategies = get_strategies_by_task_type(task_type)
    
    if not available_strategies:
        logger.warning(f"No strategies found for task type '{task_type}'. Falling back to default_general.")
        from self_improving_agent.strategy.registry import get_strategy
        return get_strategy("default_general"), True

    # Check if we should explore
    if random.random() < config.STRATEGY_EXPLORATION_RATE:
        logger.info("Exploration triggered.")
        return random.choice(available_strategies), True

    # Attempt exploitation (get the preferred strategy)
    preferred = get_best_strategy_from_history(task_type)
    if preferred:
        # Check if the preferred strategy is still valid/enabled
        for s in available_strategies:
            if s["id"] == preferred["strategy_id"]:
                logger.info(f"Exploitation: Selected preferred strategy {s['id']}")
                return s, False
    
    # If no preference yet or not enough samples, randomly explore
    logger.info("No valid preferred strategy found. Defaulting to exploration.")
    return random.choice(available_strategies), True

def get_best_strategy_from_history(task_type: str) -> Dict[str, Any]:
    """
    Queries the strategy_preferences table to find the best strategy for the task type.
    Returns the preference record dict, or None if STRATEGY_MIN_SAMPLES is not met for any.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # Find the rank 1 strategy that meets the sample count
        cursor.execute("""
            SELECT strategy_id, score, sample_count 
            FROM strategy_preferences 
            WHERE task_type = ? AND sample_count >= ?
            ORDER BY rank ASC, score DESC
            LIMIT 1
        """, (task_type, config.STRATEGY_MIN_SAMPLES))
        
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    except Exception as e:
        logger.error(f"Error querying strategy preferences: {e}")
        return None
    finally:
        conn.close()

def recalculate_strategy_preferences(task_type: str, strategy_id: str):
    """
    Recalculates the strategy score based on recent performance data
    and updates the strategy_preferences table.
    """
    from self_improving_agent.memory.database import get_strategy_stats
    from self_improving_agent.memory.memory import update_strategy_preference
    import uuid
    
    stats = get_strategy_stats(task_type, strategy_id)
    if not stats:
        return
        
    # Deterministic scoring formula:
    # 60% success rate + 30% quality + 10% confidence
    score = (stats["success_rate"] * 0.6) + (stats["avg_quality_score"] * 0.3) + (stats["avg_confidence_score"] * 0.1)
    
    # Simple rank approximation (could be refined with a real window function, but here we just store the score)
    # We will compute rank dynamically in the read query or set it to 1 for now
    update_strategy_preference(
        pref_id=str(uuid.uuid4()),
        task_type=task_type,
        strategy_id=strategy_id,
        score=score,
        rank=1, # simplified
        confidence="high" if stats["sample_count"] >= config.STRATEGY_MIN_SAMPLES else "low",
        sample_count=stats["sample_count"],
        reason=f"Calculated from {stats['sample_count']} samples."
    )
    logger.info(f"Updated preference for {strategy_id} on {task_type}: Score {score:.2f}")

