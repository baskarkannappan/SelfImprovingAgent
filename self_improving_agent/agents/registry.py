from typing import Dict, Type
from .base import BaseAgent
import logging

logger = logging.getLogger(__name__)

_AGENT_REGISTRY: Dict[str, BaseAgent] = {}

def register_agent(agent: BaseAgent) -> None:
    """Register an instantiated agent."""
    _AGENT_REGISTRY[agent.name] = agent
    logger.info(f"Registered agent: {agent.name}")

def get_agent(name: str) -> BaseAgent:
    if name not in _AGENT_REGISTRY:
        raise ValueError(f"Agent {name} not found in registry")
    return _AGENT_REGISTRY[name]

def get_all_agents() -> Dict[str, BaseAgent]:
    return _AGENT_REGISTRY
