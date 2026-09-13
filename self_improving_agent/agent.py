import os
import logging
from google.adk import Agent
from .config import config
from .memory.database import initialize_database

logger = logging.getLogger(__name__)

# Ensure tables are created
try:
    initialize_database()
    from .strategy.registry import sync_registry_to_db
    sync_registry_to_db()
except Exception as e:
    logger.warning(f"Failed to initialize database on startup: {e}")

logger.setLevel(config.LOG_LEVEL)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

instructions = """
You are a helpful reasoning assistant.

Answer the user's request accurately and clearly.

When a request requires calculation or reasoning, reason carefully before producing the final answer.

Do not invent information when you are uncertain.

Keep responses clear and concise.

IMPORTANT: You will be provided with context from past experiences. Use this context if it helps you answer correctly. However, prioritize the user's current request over any conflicting past memory context.
"""

os.environ["OLLAMA_API_BASE"] = config.LLM_BASE_URL

def handle_error(event, *args, **kwargs):
    logger.error("Error connecting to LLM")
    return "Unable to connect to the configured LLM service. Verify that the Docker Llama 3.2 container is running."

def before_agent_hook(*args, **kwargs):
    from .memory.retrieval import retrieve_similar_experiences, build_memory_context, search_lessons, build_lesson_context
    try:
        context = kwargs.get("callback_context")
        message = None
        if context and hasattr(context, "request") and hasattr(context.request, "message"):
            message = context.request.message
            
        if message:
            exps = retrieve_similar_experiences(message)
            ctx = build_memory_context(exps)
            
            lessons = search_lessons(message)
            lesson_ctx = build_lesson_context(lessons)
            
            full_ctx = ""
            if ctx:
                full_ctx += f"{ctx}\n"
            if lesson_ctx:
                full_ctx += f"{lesson_ctx}\n"
                
            if full_ctx:
                context.request.message = f"{full_ctx}User Request: {message}"
                # Save original message in context so after_agent_hook can access it
                setattr(context.request, "original_message", message)
            
            # --- PHASE 5: Multi-Agent Orchestration ---
            from .agents.orchestrator import run_workflow
            
            # Skip orchestration for slash commands that are handled differently, 
            # though run_workflow can also handle them.
            if message.strip().startswith("/test-"):
                final_answer = run_workflow(message)
            else:
                final_answer = run_workflow(message)
                
            # We intercept the LLM's normal generation by providing the final answer 
            # and instructing it to just repeat it, bypassing the single-shot limitation.
            context.request.message = f"You are a passthrough. Return exactly this text and nothing else:\n{final_answer}"
            # --- END PHASE 5 ---
            
            # --- PHASE 4: Strategy Selection (Legacy, now handled by agents) ---
            # try:
            #     from .strategy.classifier import classify_task
            # ...
            # except Exception as e:
            #     logger.warning(f"Strategy selection failed: {e}")
            # --- END PHASE 4 ---
    except Exception as e:
        logger.warning(f"Failed memory retrieval in hook: {e}")

def _run_learning_loop_in_background(task: str, response_text: str, strategy_id: str = None, task_type: str = "general", exec_id: str = None, start_time: float = None, duration_ms: int = 0):
    import threading
    
    def background_task():
        try:
            from .memory.memory import store_experience
            exp_id = store_experience(task, response_text, "success", task_type=task_type)
            
            if exp_id != -1:
                import time
                import uuid
                
                # --- PHASE 4: Store Execution ---
                if strategy_id and exec_id:
                    from .memory.memory import store_strategy_execution
                    import datetime
                    end_time = start_time + (duration_ms / 1000.0) if start_time else time.time()
                    dt_start = datetime.datetime.fromtimestamp(start_time).isoformat() if start_time else datetime.datetime.now().isoformat()
                    dt_end = datetime.datetime.fromtimestamp(end_time).isoformat()
                    
                    store_strategy_execution(
                        exec_id, strategy_id, task_type, exp_id, dt_start, dt_end, duration_ms, "success"
                    )
                # --- END PHASE 4 ---
                
                from .evaluator import Evaluator
                evaluator = Evaluator()
                eval_res = evaluator.evaluate(task, response_text)
                
                from .memory.memory import store_evaluation, store_lesson
                eval_id = store_evaluation(
                    experience_id=exp_id,
                    correct=eval_res["correct"],
                    quality=eval_res["quality"],
                    confidence=eval_res["confidence"],
                    reason=eval_res["reason"]
                )
                
                if eval_id != -1:
                    # --- PHASE 4: Store Performance ---
                    if strategy_id and exec_id:
                        from .memory.memory import store_strategy_performance
                        perf_id = str(uuid.uuid4())
                        success = (eval_res["correct"] == "true")
                        store_strategy_performance(
                            perf_id, strategy_id, task_type, exp_id, eval_id, 
                            success, eval_res["quality"], eval_res["confidence"], duration_ms
                        )
                        
                        from .strategy.selector import recalculate_strategy_preferences
                        recalculate_strategy_preferences(task_type, strategy_id)
                    # --- END PHASE 4 ---
                    
                    from .graph import link_experience_to_evaluation, link_evaluation_to_lesson
                    link_experience_to_evaluation(exp_id, eval_id)
                    
                    from .learner import Learner
                    learner = Learner()
                    lesson_res = learner.extract_lesson(task, response_text, eval_res)
                    
                    if lesson_res:
                        lesson_id = store_lesson(
                            lesson_text=lesson_res["lesson_text"],
                            lesson_type=lesson_res["lesson_type"],
                            experience_id=exp_id,
                            evaluation_id=eval_id,
                            confidence=lesson_res["confidence"]
                        )
                        if lesson_id != -1:
                            link_evaluation_to_lesson(eval_id, lesson_id)
        except Exception as e:
            logger.error(f"Error in background learning loop: {e}")

    thread = threading.Thread(target=background_task)
    thread.daemon = True
    thread.start()

def after_agent_hook(*args, **kwargs):
    try:
        context = args[0] if args else kwargs.get("callback_context")
        if not context:
            return
            
        task = None
        response_text = None
        
        # Extract task
        if hasattr(context, "user_content") and context.user_content:
            if hasattr(context.user_content, "parts") and context.user_content.parts:
                task = context.user_content.parts[0].text
            else:
                task = str(context.user_content)
                
        # Extract response from the last event in the session
        if hasattr(context, 'session') and hasattr(context.session, 'events') and context.session.events:
            # The last event contains the model's final response content
            last_event = context.session.events[-1]
            if hasattr(last_event, 'content') and last_event.content:
                if hasattr(last_event.content, 'parts') and last_event.content.parts:
                    response_text = last_event.content.parts[0].text
                else:
                    response_text = str(last_event.content)
                    
        if task and response_text:
            target = context.session if hasattr(context, "session") else context
            target = target if hasattr(target, "strategy_id") else getattr(context, "request", context)
            
            strategy_id = getattr(target, "strategy_id", None)
            task_type = getattr(target, "strategy_task_type", "general")
            exec_id = getattr(target, "strategy_exec_id", None)
            start_time = getattr(target, "strategy_start_time", None)
            
            duration_ms = 0
            if start_time:
                import time
                duration_ms = int((time.time() - start_time) * 1000)
                
            logger.info(f"Triggering background learning loop for task: {task[:50]}...")
            _run_learning_loop_in_background(
                str(task), str(response_text), 
                strategy_id=strategy_id, 
                task_type=task_type, 
                exec_id=exec_id, 
                start_time=start_time, 
                duration_ms=duration_ms
            )
        else:
            logger.warning(f"Could not extract task or response. Task: {task}, Response length: {len(response_text) if response_text else 'None'}")
    except Exception as e:
        logger.warning(f"Failed to trigger learning loop: {e}")

self_improving_agent = Agent(
    name="self_improving_agent",
    instruction=instructions,
    model=f"ollama/{config.LLM_MODEL}",
    on_model_error_callback=handle_error,
    before_agent_callback=before_agent_hook,
    after_agent_callback=after_agent_hook
)

def handle_user_message(message: str) -> str:
    # --- PHASE 4: Intercept testing command ---
    if message.strip().startswith("/test-strategy comparison"):
        from .strategy.tester import run_strategy_comparison_test
        return run_strategy_comparison_test()
    # --- END PHASE 4 ---

    # This is just a stub for the test to pass if the test calls it directly
    # In a real ADK flow, ADK handles the interaction.
    from .memory.retrieval import retrieve_similar_experiences, build_memory_context
    from .memory.memory import store_experience
    
    try:
        exps = retrieve_similar_experiences(message)
        context = build_memory_context(exps)
    except Exception as e:
        logger.warning(f"Memory retrieval failed: {e}")
        context = ""
        
    full_prompt = message
    if context:
        full_prompt = f"{context}\nUser Request: {message}"
        
    try:
        import litellm
        response = litellm.completion(
            model=f"ollama/{config.LLM_MODEL}",
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": full_prompt}
            ],
            api_base=config.LLM_BASE_URL
        )
        answer = response.choices[0].message.content
        
        try:
            store_experience(message, answer, "success")
        except Exception as e:
            logger.warning(f"Memory storage failed: {e}")
            
        return answer
    except Exception as e:
        logger.error(f"Error in handle_user_message: {e}")
        return handle_error(None)

root_agent = self_improving_agent
