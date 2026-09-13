import json
from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import datetime
import uuid
import os

@dataclass
class TaskResult:
    task_id: str
    task_text: str
    correct: bool
    quality: str
    selected_strategy: Optional[str]
    selected_workflow: Optional[str]
    duration_ms: int

@dataclass
class BenchmarkReport:
    run_id: str
    timestamp: str
    phase: str
    total_tasks: int
    success_rate: float
    average_quality: float
    average_latency_ms: int
    lessons_retrieved: int
    lessons_reused: int
    critic_invocations: int
    improvement_invocations: int
    task_results: List[TaskResult]

    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(asdict(self), f, indent=2)

    @classmethod
    def load(cls, filepath: str) -> "BenchmarkReport":
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Reconstruct TaskResult objects
        task_results = [TaskResult(**tr) for tr in data.pop("task_results", [])]
        return cls(**data, task_results=task_results)
