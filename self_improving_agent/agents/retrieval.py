import logging
from .base import BaseAgent, WorkflowState

logger = logging.getLogger(__name__)

class RetrievalAgent(BaseAgent):
    def __init__(self):
        super().__init__("retrieval", "Fetches relevant context and experiences from persistent memory.")

    def execute(self, state: WorkflowState) -> WorkflowState:
        logger.info("RetrievalAgent executing...")
        
        try:
            from ..memory.retrieval import retrieve_similar_experiences, build_memory_context, search_lessons, build_lesson_context
            
            exps = retrieve_similar_experiences(state.task)
            ctx = build_memory_context(exps)
            
            lessons = search_lessons(state.task)
            lesson_ctx = build_lesson_context(lessons)
            
            state.retrieved_context = {
                "experiences_text": ctx,
                "lessons_text": lesson_ctx
            }
            
        except Exception as e:
            logger.error(f"RetrievalAgent failed: {e}")
            state.retrieved_context = {"error": str(e)}
            
        return state
