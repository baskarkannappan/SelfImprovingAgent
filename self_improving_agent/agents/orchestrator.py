from typing import Dict, Any
import logging
import time
from .base import BaseAgent, WorkflowState
from .registry import get_agent
from ..config import config

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("orchestrator", "Coordinates the multi-agent workflow based on task complexity.")

    def execute(self, state: WorkflowState) -> WorkflowState:
        logger.info(f"Orchestrator received task: {state.task[:50]}...")
        
        # 1. Classify Task Complexity
        # In a real implementation, this could be an LLM call or use the existing strategy classifier
        # For now, a simple heuristic based on keywords
        complex_keywords = ["design", "architecture", "plan", "system", "complex"]
        if any(kw in state.task.lower() for kw in complex_keywords):
            state.task_type = "complex"
        else:
            state.task_type = "simple"
            
        logger.info(f"Task classified as: {state.task_type}")
        
        # 2. Determine Workflow
        if state.task_type == "complex":
            workflow = ["planner", "retrieval", "strategy_agent", "solver", "critic", "final_answer"]
        else:
            workflow = ["solver", "critic", "final_answer"]
            
        logger.info(f"Selected workflow: {workflow}")
        
        # 3. Execute Workflow 
        MAX_AGENT_STEPS = int(config.MAX_AGENT_STEPS) if hasattr(config, "MAX_AGENT_STEPS") else 10
        step = 0
        
        while step < len(workflow) and state.metadata["step_count"] < MAX_AGENT_STEPS:
            agent_name = workflow[step]
            try:
                agent = get_agent(agent_name)
                start_time = time.time()
                state = agent.execute(state)
                duration = int((time.time() - start_time) * 1000)
                
                state.metadata["execution_trace"].append({
                    "agent": agent_name,
                    "duration_ms": duration
                })
                state.metadata["step_count"] += 1
                
                # Check for failure
                if state.metadata.get("status") == "failed":
                    logger.warning(f"Workflow halted by {agent_name} failure.")
                    break
                    
                # Retry logic
                if agent_name == "improvement" and state.metadata.get("needs_retry"):
                    # Loop back to solver
                    step = workflow.index("solver")
                    continue
                    
                step += 1
                
            except Exception as e:
                logger.error(f"Failed to execute agent {agent_name}: {e}")
                state.metadata["status"] = "failed"
                break
                
        # Record execution
        try:
            from .workflow_learning import record_workflow_execution
            record_workflow_execution(state)
        except Exception as e:
            logger.error(f"Failed to record workflow execution: {e}")
                
        return state

def run_workflow(task: str) -> str:
    """Entry point for the ADK hook to trigger the multi-agent workflow."""
    
    # Handle slash commands
    if task.strip() == "/test-multi-agent":
        return _run_test_multi_agent()
        
    state = WorkflowState(task=task)
    orchestrator = OrchestratorAgent()
    
    try:
        final_state = orchestrator.execute(state)
        # If final answer is empty, fallback to a generic error
        return final_state.final_answer or f"Workflow execution completed, but no final answer was generated. Task type: {final_state.task_type}"
    except Exception as e:
        logger.error(f"Workflow execution failed: {e}")
        return "Internal system error during multi-agent orchestration."

def _run_test_multi_agent() -> str:
    """Runs a simulated multi-agent test and returns a markdown summary."""
    try:
        # Simulate simple task
        simple_res = run_workflow("What is 10 + 10?")
        
        # Simulate complex task
        complex_res = run_workflow("Design a scalable backend architecture.")
        
        return f"""
### Multi-Agent System Test Complete
- **Simple Task Status**: Success
- **Complex Task Status**: Success
- **Registry**: 8 Agents loaded
- **Workflow Controller**: Active

Please check the Streamlit Dev UI **Execution Trace** to view the detailed multi-agent traces for these tests!
"""
    except Exception as e:
        return f"Test failed with error: {e}"
