import time
import uuid
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def format_strategy_prompt(task: str, strategy: Dict[str, Any]) -> str:
    """
    Formats the user task with the specific strategy instructions so the LLM executes them.
    """
    steps_list = "\n".join([f"{i+1}. {step}" for i, step in enumerate(strategy["steps"])])
    
    prompt = f"""You must solve the following task using this specific strategy: '{strategy["name"]}'.

STRATEGY STEPS TO FOLLOW:
{steps_list}

TASK: {task}
"""
    return prompt
