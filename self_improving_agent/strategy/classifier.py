import re

def classify_task(task_text: str) -> str:
    """
    Deterministically classifies the task type based on keywords.
    For Phase 4, we primarily care about 'calculation'.
    """
    text_lower = task_text.lower()
    
    # Simple heuristics for calculation
    calc_keywords = ["calculate", "math", "add", "subtract", "multiply", "divide", "what is", "sum", "%", "percent"]
    # Also check if it contains a math expression like "15% of 200" or "2 + 2"
    has_math_symbols = bool(re.search(r'[\d\+\-\*\/\%]', text_lower))
    
    if has_math_symbols and any(kw in text_lower for kw in calc_keywords):
        return "calculation"
        
    return "general"
