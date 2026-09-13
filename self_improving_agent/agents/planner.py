import logging
import litellm
import json
from .base import BaseAgent, WorkflowState
from ..config import config

logger = logging.getLogger(__name__)

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("planner", "Breaks down complex tasks into a structured plan.")

    def execute(self, state: WorkflowState) -> WorkflowState:
        logger.info("PlannerAgent executing...")
        
        prompt = f"""
        You are the Planner Agent. Your job is to break down the following complex task into 3-5 logical steps.
        Return the result as a raw JSON array of objects, where each object has 'id' and 'description' fields.
        DO NOT return markdown formatting. Just the raw JSON array.
        
        Task: {state.task}
        """
        
        try:
            response = litellm.completion(
                model=f"ollama/{config.LLM_MODEL}",
                messages=[{"role": "user", "content": prompt}],
                api_base=config.LLM_BASE_URL,
                temperature=0.0
            )
            
            content = response.choices[0].message.content.strip()
            # Try to parse the json
            # Handle potential markdown code blocks returned by the LLM
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
                
            plan_json = json.loads(content.strip())
            state.plan = plan_json
            
        except Exception as e:
            logger.error(f"PlannerAgent failed: {e}")
            state.metadata["status"] = "failed"
            
        return state
