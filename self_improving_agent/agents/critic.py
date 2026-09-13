import logging
from .base import BaseAgent, WorkflowState
from ..evaluator import Evaluator

logger = logging.getLogger(__name__)

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__("critic", "Evaluates the Solver's answer.")
        self.evaluator = Evaluator()

    def execute(self, state: WorkflowState) -> WorkflowState:
        logger.info("CriticAgent executing...")
        
        try:
            eval_res = self.evaluator.evaluate(state.task, state.solver_result)
            
            state.critic_evaluation = {
                "correct": eval_res["correct"] == "true",
                "quality": eval_res["quality"],
                "confidence": eval_res["confidence"],
                "reason": eval_res["reason"]
            }
            
        except Exception as e:
            logger.error(f"CriticAgent failed: {e}")
            state.critic_evaluation = {
                "correct": False,
                "reason": f"Evaluation failed: {e}"
            }
            
        return state
