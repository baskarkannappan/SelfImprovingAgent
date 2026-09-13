import logging
from .base import BaseAgent, WorkflowState

logger = logging.getLogger(__name__)

class FinalAnswerAgent(BaseAgent):
    def __init__(self):
        super().__init__("final_answer", "Produces the final user-facing answer.")

    def execute(self, state: WorkflowState) -> WorkflowState:
        logger.info("FinalAnswerAgent executing...")
        
        # For now, it simply forwards the solver result. 
        # In a more advanced implementation, it could synthesize multiple solver results or rewrite it cleanly.
        if state.metadata.get("status") == "failed":
            state.final_answer = "The system encountered an error while processing the request."
        else:
            state.final_answer = state.solver_result
            
        return state
