import logging
from .base import BaseAgent, WorkflowState

logger = logging.getLogger(__name__)

class StrategyAgent(BaseAgent):
    def __init__(self):
        super().__init__("strategy_agent", "Selects the optimal execution strategy based on historical performance.")

    def execute(self, state: WorkflowState) -> WorkflowState:
        logger.info("StrategyAgent executing...")
        
        try:
            from ..strategy.selector import select_strategy
            strategy, is_exploration = select_strategy(state.task_type)
            
            state.strategy = {
                "id": strategy["id"],
                "description": strategy.get("description", ""),
                "prompt": strategy.get("prompt", "") or str(strategy.get("steps", [])),
                "is_exploration": is_exploration
            }
            
        except Exception as e:
            logger.error(f"StrategyAgent failed: {e}")
            state.strategy = {"id": "default_general"}
            
        return state
