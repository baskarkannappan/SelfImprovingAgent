from .registry import register_agent
from .orchestrator import OrchestratorAgent
from .planner import PlannerAgent
from .retrieval import RetrievalAgent
from .strategy_agent import StrategyAgent
from .solver import SolverAgent
from .critic import CriticAgent
from .improvement import ImprovementAgent
from .final_answer import FinalAnswerAgent

# Auto-register all core agents
register_agent(OrchestratorAgent())
register_agent(PlannerAgent())
register_agent(RetrievalAgent())
register_agent(StrategyAgent())
register_agent(SolverAgent())
register_agent(CriticAgent())
register_agent(ImprovementAgent())
register_agent(FinalAnswerAgent())
