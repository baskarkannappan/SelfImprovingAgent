import json
import logging
import litellm
from .config import config

logger = logging.getLogger(__name__)

EVALUATOR_PROMPT = """
You are an expert self-evaluator for an AI agent.
Your job is to evaluate the response the agent gave to the user's task.
Output a JSON object with exactly these fields:
- "correct": string, one of "true", "false", or "unknown"
- "quality": string, one of "excellent", "good", "acceptable", or "poor"
- "confidence": string, one of "high", "medium", or "low"
- "reason": string, a brief 1-2 sentence explanation for your judgment.

Only output valid JSON, nothing else.
"""

class Evaluator:
    def __init__(self):
        self.model = f"ollama/{config.LLM_MODEL}"
        self.api_base = config.LLM_BASE_URL
        
    def evaluate(self, task: str, response: str) -> dict:
        """Evaluate a task and response, returning a dictionary of the evaluation."""
        user_prompt = f"Task: {task}\nResponse: {response}\n\nEvaluate the response based on the task."
        
        try:
            res = litellm.completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": EVALUATOR_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                api_base=self.api_base,
                response_format={"type": "json_object"}
            )
            
            content = res.choices[0].message.content
            # Remove any markdown formatting if present
            content = content.replace("```json", "").replace("```", "").strip()
            result = json.loads(content)
            
            # Validate fields
            correct = result.get("correct", "unknown")
            quality = result.get("quality", "acceptable")
            confidence = result.get("confidence", "medium")
            reason = result.get("reason", "No reason provided")
            
            if correct not in ("true", "false", "unknown"):
                correct = "unknown"
            if quality not in ("excellent", "good", "acceptable", "poor"):
                quality = "acceptable"
            if confidence not in ("high", "medium", "low"):
                confidence = "medium"
                
            return {
                "correct": correct,
                "quality": quality,
                "confidence": confidence,
                "reason": reason
            }
        except Exception as e:
            logger.warning(f"Evaluator failed: {e}")
            return {
                "correct": "unknown",
                "quality": "acceptable",
                "confidence": "low",
                "reason": f"Evaluation failed due to error: {e}"
            }
