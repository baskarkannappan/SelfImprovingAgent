import json
from typing import Dict, Any

# A predefined deterministic registry of strategies
STRATEGY_REGISTRY: Dict[str, Dict[str, Any]] = {
    "direct_calculation": {
        "id": "direct_calculation",
        "name": "Direct Calculation",
        "task_type": "calculation",
        "description": "Directly calculates the answer without extra steps.",
        "steps": ["Extract numbers", "Perform operation", "Format answer"],
        "enabled": True
    },
    "verify_calculation": {
        "id": "verify_calculation",
        "name": "Verify Calculation",
        "task_type": "calculation",
        "description": "Calculates the answer and then performs a verification step.",
        "steps": ["Extract numbers", "Perform operation", "Verify operation", "Format answer"],
        "enabled": True
    },
    "step_by_step_calculation": {
        "id": "step_by_step_calculation",
        "name": "Step by Step Calculation",
        "task_type": "calculation",
        "description": "Calculates the answer explicitly breaking down each intermediate step.",
        "steps": ["Identify problem", "Break down steps", "Calculate each step", "Sum results", "Format answer"],
        "enabled": True
    },
    "default_general": {
        "id": "default_general",
        "name": "Default General",
        "task_type": "general",
        "description": "A standard fallback strategy for non-calculation tasks.",
        "steps": ["Understand task", "Generate response"],
        "enabled": True
    }
}

def get_strategies_by_task_type(task_type: str) -> list[Dict[str, Any]]:
    """Return all enabled strategies for a given task type."""
    return [
        s for s in STRATEGY_REGISTRY.values() 
        if s["task_type"] == task_type and s["enabled"]
    ]

def get_strategy(strategy_id: str) -> Dict[str, Any]:
    """Get a strategy by ID."""
    return STRATEGY_REGISTRY.get(strategy_id)

def sync_registry_to_db():
    """Sync the hardcoded registry to the SQLite database so UI/GraphQLite can query it."""
    from self_improving_agent.memory.database import get_connection
    conn = get_connection()
    try:
        cursor = conn.cursor()
        for s_id, s in STRATEGY_REGISTRY.items():
            cursor.execute("""
                INSERT OR REPLACE INTO strategies (id, name, task_type, description, steps, enabled)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (s["id"], s["name"], s["task_type"], s["description"], json.dumps(s["steps"]), s["enabled"]))
        conn.commit()
    except Exception as e:
        print(f"Failed to sync strategy registry: {e}")
    finally:
        conn.close()
