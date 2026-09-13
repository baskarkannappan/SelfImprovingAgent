from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class AgentResult(BaseModel):
    status: str = "success" # success, failed, partial
    result: Any = None
    confidence: str = "high"
    reason: Optional[str] = None
    duration_ms: int = 0
    created_at: Optional[str] = None

class WorkflowState(BaseModel):
    task: str = ""
    task_type: str = "general" # simple, moderate, complex
    
    plan: List[Dict[str, Any]] = Field(default_factory=list)
    retrieved_context: Dict[str, Any] = Field(default_factory=dict)
    strategy: Dict[str, Any] = Field(default_factory=dict)
    
    solver_result: str = ""
    critic_evaluation: Dict[str, Any] = Field(default_factory=dict)
    improvement_feedback: str = ""
    final_answer: str = ""
    
    metadata: Dict[str, Any] = Field(default_factory=lambda: {
        "step_count": 0,
        "retry_count": 0,
        "execution_trace": []
    })

class BaseAgent:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        
    def execute(self, state: WorkflowState) -> WorkflowState:
        raise NotImplementedError("Subclasses must implement execute()")
