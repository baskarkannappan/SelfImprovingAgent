import logging
import sqlite3
import json
import uuid
from ..memory.database import get_connection

logger = logging.getLogger(__name__)

def record_workflow_execution(state, experience_id: int = None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # 1. Determine or Register Workflow
        task_type = state.task_type
        # In a real app we'd have a formal registry. For now, generate a workflow ID based on the trace
        trace = state.metadata.get("execution_trace", [])
        agent_names = [step["agent"] for step in trace]
        agents_sequence = json.dumps(agent_names)
        workflow_id = f"wf_{task_type}_{len(agent_names)}_steps"
        
        cursor.execute(
            "INSERT OR IGNORE INTO workflows (id, name, task_type, agents_sequence) VALUES (?, ?, ?, ?)",
            (workflow_id, workflow_id, task_type, agents_sequence)
        )
        
        # 2. Record Workflow Execution
        wf_exec_id = str(uuid.uuid4())
        status = state.metadata.get("status", "success")
        is_success = (status == "success" and state.critic_evaluation.get("correct", False))
        quality = state.critic_evaluation.get("quality", "unknown")
        duration_ms = sum(step["duration_ms"] for step in trace)
        
        cursor.execute(
            """INSERT INTO workflow_executions 
               (id, workflow_id, task_type, experience_id, status, success, quality, duration_ms) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (wf_exec_id, workflow_id, task_type, experience_id, status, is_success, quality, duration_ms)
        )
        
        # 3. Record Agent Executions
        for step in trace:
            agent_exec_id = str(uuid.uuid4())
            cursor.execute(
                """INSERT INTO agent_executions 
                   (id, workflow_execution_id, agent_id, status, duration_ms, confidence) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (agent_exec_id, wf_exec_id, step["agent"], status, step["duration_ms"], "high")
            )
            
        conn.commit()
        
        # 4. Update Workflow Preferences
        _recalculate_workflow_preferences(task_type)
        
    except Exception as e:
        logger.error(f"Failed to record workflow execution: {e}")

def _recalculate_workflow_preferences(task_type: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get all workflows for this task type
        cursor.execute("SELECT id FROM workflows WHERE task_type = ?", (task_type,))
        workflows = cursor.fetchall()
        
        best_wf = None
        best_score = -1.0
        
        for (wf_id,) in workflows:
            cursor.execute(
                "SELECT success, quality, duration_ms FROM workflow_executions WHERE workflow_id = ?",
                (wf_id,)
            )
            executions = cursor.fetchall()
            
            if not executions:
                continue
                
            sample_count = len(executions)
            successes = sum(1 for e in executions if e[0])
            success_rate = successes / sample_count
            
            # Simple heuristic
            score = (success_rate * 0.7) + (min(10000, max(0, 10000 - sum(e[2] for e in executions)/sample_count))/10000 * 0.3)
            
            cursor.execute(
                """INSERT INTO workflow_preferences (task_type, workflow_id, score, sample_count)
                   VALUES (?, ?, ?, ?)
                   ON CONFLICT(task_type) DO UPDATE SET workflow_id=excluded.workflow_id, score=excluded.score, sample_count=excluded.sample_count, updated_at=CURRENT_TIMESTAMP""",
                (task_type, wf_id, score, sample_count)
            )
            
            if score > best_score:
                best_score = score
                best_wf = wf_id
                
        conn.commit()
        
    except Exception as e:
        logger.error(f"Failed to recalculate workflow preferences: {e}")
