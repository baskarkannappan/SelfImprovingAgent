import json
import logging
import litellm
from .config import config

logger = logging.getLogger(__name__)

LEARNER_PROMPT = """
You are an expert self-improvement learner for an AI agent.
You will receive a task, the agent's response, and an evaluation of that response.
If the evaluation reveals a mistake or an opportunity for a reusable lesson (e.g. error prevention, formatting rule), extract a concise, generalized lesson.
If the response was trivial and perfectly fine without a meaningful lesson, output an empty string for the lesson.

Output a JSON object with exactly these fields:
- "lesson_text": string, the concise generalized lesson, or empty string if no lesson applies.
- "lesson_type": string, one of "error_prevention", "formatting", "verification", or "other"
- "confidence": string, one of "high", "medium", or "low"

Only output valid JSON, nothing else.
"""

class Learner:
    def __init__(self):
        self.model = f"ollama/{config.LLM_MODEL}"
        self.api_base = config.LLM_BASE_URL
        
    def extract_lesson(self, task: str, response: str, evaluation: dict) -> dict:
        """Extract a lesson based on the task, response, and its evaluation."""
        user_prompt = f"Task: {task}\nResponse: {response}\nEvaluation: {json.dumps(evaluation)}\n\nExtract a generic lesson if applicable."
        
        try:
            res = litellm.completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": LEARNER_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                api_base=self.api_base,
                response_format={"type": "json_object"}
            )
            
            content = res.choices[0].message.content
            # Remove any markdown formatting if present
            content = content.replace("```json", "").replace("```", "").strip()
            result = json.loads(content)
            
            lesson_text = result.get("lesson_text", "").strip()
            if not lesson_text:
                return None
                
            return {
                "lesson_text": lesson_text,
                "lesson_type": result.get("lesson_type", "other"),
                "confidence": result.get("confidence", "medium")
            }
        except Exception as e:
            logger.warning(f"Learner failed: {e}")
            return None
