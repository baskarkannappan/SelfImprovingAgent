import logging
import litellm
from .base import BaseAgent, WorkflowState
from ..config import config

logger = logging.getLogger(__name__)

class SolverAgent(BaseAgent):
    def __init__(self):
        super().__init__("solver", "Generates the main answer using the planned steps and retrieved context.")

    def execute(self, state: WorkflowState) -> WorkflowState:
        logger.info("SolverAgent executing...")
        
        # Build prompt using retrieved context and strategy
        prompt_parts = []
        
        if state.retrieved_context.get("experiences_text"):
            prompt_parts.append(state.retrieved_context["experiences_text"])
            
        if state.retrieved_context.get("lessons_text"):
            prompt_parts.append(state.retrieved_context["lessons_text"])
            
        if state.plan:
            plan_str = "Follow these planned steps:\n"
            for step in state.plan:
                plan_str += f"- {step.get('description', '')}\n"
            prompt_parts.append(plan_str)
            
        if state.improvement_feedback:
            prompt_parts.append(f"PREVIOUS ATTEMPT FEEDBACK:\n{state.improvement_feedback}")
            
        prompt_parts.append(f"User Request: {state.task}")
        full_prompt = "\n\n".join(prompt_parts)
        
        # Apply strategy if present
        if state.strategy.get("id") and state.strategy.get("id") != "default_general":
            from ..strategy.executor import format_strategy_prompt
            full_prompt = format_strategy_prompt(full_prompt, state.strategy)
            
        try:
            response = litellm.completion(
                model=f"ollama/{config.LLM_MODEL}",
                messages=[{"role": "user", "content": full_prompt}],
                api_base=config.LLM_BASE_URL
            )
            state.solver_result = response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"SolverAgent failed: {e}")
            state.metadata["status"] = "failed"
            state.solver_result = f"Error generating answer: {str(e)}"
            
        return state
