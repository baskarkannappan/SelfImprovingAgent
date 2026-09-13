# Agent Interfaces & Contracts

Agents must communicate using a structured `WorkflowState` (or similar dictionary).

## WorkflowState Contract

```python
{
    "task": "Original user prompt",
    "task_type": "complex", # simple, moderate, complex
    
    "plan": [
        # Populated by Planner
        {"id": 1, "description": "Identify requirements"}
    ],
    
    "retrieved_context": {
        # Populated by Retrieval Agent
        "experiences": [...],
        "lessons": [...]
    },
    
    "strategy": {
        # Populated by Strategy Agent
        "id": "structured_analysis",
        "description": "..."
    },
    
    "solver_result": "Raw text output from the Solver agent",
    
    "critic_evaluation": {
        # Populated by Critic Agent
        "correct": True,
        "quality": "good",
        "confidence": "high",
        "reason": "..."
    },
    
    "improvement_feedback": "Specific instructions for the Solver retry",
    
    "final_answer": "The finalized response shown to the user",
    
    "metadata": {
        "step_count": 5,
        "retry_count": 0,
        "execution_trace": [
            {"agent": "orchestrator", "duration_ms": 10},
            {"agent": "planner", "duration_ms": 1500}
        ]
    }
}
```

Each logical agent receives this dictionary (or object), reads the fields it needs, and appends/updates its specific output fields before passing it to the next agent in the sequence.
