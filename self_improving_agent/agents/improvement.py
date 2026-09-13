import logging
from .base import BaseAgent, WorkflowState
from ..config import config

logger = logging.getLogger(__name__)

class ImprovementAgent(BaseAgent):
    def __init__(self):
        super().__init__("improvement", "Determines if a retry is needed based on the Critic's evaluation.")

    def execute(self, state: WorkflowState) -> WorkflowState:
        logger.info("ImprovementAgent executing...")
        
        # Check if the critic marked it as incorrect or if we want to improve it
        is_correct = state.critic_evaluation.get("correct", False)
        quality = state.critic_evaluation.get("quality", "poor")
        
        if not is_correct or quality == "poor":
            if state.metadata["retry_count"] < int(config.MAX_RETRIES):
                logger.info(f"Triggering retry {state.metadata['retry_count'] + 1}/{config.MAX_RETRIES}")
                state.metadata["retry_count"] += 1
                state.improvement_feedback = f"Your previous answer was evaluated as incorrect/poor. Reason: {state.critic_evaluation.get('reason')}. Please fix these issues."
                # Signal the orchestrator to retry the solver
                state.metadata["needs_retry"] = True
            else:
                logger.warning("Max retries reached. Accepting partial/failed result.")
                state.metadata["needs_retry"] = False
        else:
            state.metadata["needs_retry"] = False
            
        return state
