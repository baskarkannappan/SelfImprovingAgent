# 🏛️ High-Level Technical Architecture

The **Self-Improving Agents** application is a modular, local-first Python system built on top of an asynchronous execution pipeline, a SQLite-based memory engine, and the Google ADK (Agent Development Kit). 

## 1. Core Components

1. **ADK Integration (`hook.py`)**: 
   - Intercepts user messages from the ADK Web UI.
   - Redirects the prompt into our custom `process_prompt` async workflow instead of passing it to a generic LLM.

2. **The Execution Pipeline (`main.py`)**:
   - The orchestrator. It executes the agents sequentially and passes state between them.
   - It captures the `duration_ms` for each agent and generates a unique `workflow_execution_id` for traceability.

3. **Memory & Vector Database (`memory/database.py`)**:
   - Uses **SQLite** for relational storage (Experiences, Evaluations, Strategies, Workflows).
   - Uses **sqlite-vec** for vector embeddings. The Retrieval agent converts text into vector embeddings using the `nomic-embed-text` model and performs cosine-similarity search to find related past experiences.
   - Uses **GraphQLite** (`graph.py`) to map relational data into graph nodes and edges so that complex paths (e.g., Task -> Workflow -> Experience -> Evaluation -> Lesson) can be visualized.

4. **Agents (`agents/`)**:
   - Each agent (`planner.py`, `retrieval.py`, `solver.py`, `critic.py`) wraps a call to **LiteLLM**. 
   - We use `Llama 3.2` as the local language model. 

5. **Strategy Engine (`strategy/`)**:
   - Maintains a dynamic registry of workflows (e.g., Simple, Complex, Debug).
   - Chooses a strategy based on Epsilon-Greedy logic (90% Exploitation of the best historical score, 10% Exploration of random strategies).

6. **Developer UI (`developer_ui/`)**:
   - A **Streamlit** application that directly queries the local SQLite database to render dashboards (Execution Trace, Memory Browser, Strategy Performance, and Continuous Improvement Benchmarks).

---

## 2. Sequence Diagram

This diagram shows the exact technical flow when a user sends a prompt through the chat interface.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant ADK as ADK Hook
    participant Main as Pipeline
    participant Memory as SQLite + sqlite-vec
    participant Strat as Strategy Engine
    participant LLM as LiteLLM
    participant Critic as Critic Agent

    User->>ADK: Sends Prompt ("Write a script")
    ADK->>Main: Intercept & trigger process_prompt()
    
    rect rgb(240, 248, 255)
        Note over Main, LLM: Phase 1: Planning & Retrieval
        Main->>LLM: PlannerAgent(Prompt)
        LLM-->>Main: Returns Step-by-Step Checklist
        Main->>Memory: RetrievalAgent(Prompt Embedding)
        Memory-->>Main: Returns Top K Past Lessons
    end

    rect rgb(255, 245, 238)
        Note over Main, Strat: Phase 2: Strategy Selection
        Main->>Strat: get_best_strategy(Prompt)
        Strat->>Memory: Query historical success rates
        Memory-->>Strat: Scores for Simple/Complex
        Strat-->>Main: Selected Strategy & Workflow Rules
    end
    
    rect rgb(245, 255, 250)
        Note over Main, LLM: Phase 3: Solving
        Main->>LLM: SolverAgent(Prompt + Checklist + Lessons + Strategy)
        LLM-->>Main: Generated Code/Answer
    end

    rect rgb(255, 240, 245)
        Note over Main, Memory: Phase 4: Evaluation & Learning
        Main->>Critic: CriticAgent(Answer, Original Prompt, Lessons)
        Critic->>LLM: Grade the answer
        LLM-->>Critic: Quality Score + New Lesson text
        Critic->>Memory: Save Experience, Evaluation, and Lesson
        Main->>Memory: Save Workflow Trace & Timings
    end
    
    Main-->>ADK: Return Final Answer String
    ADK-->>User: Display in Chat UI
```

---

## 3. Database Schema Overview

The relational structure that powers the learning loop:

- `workflow_executions`: Logs the execution trace (durations of all agents).
- `strategy_preferences`: The available strategies and their exploration counts.
- `experiences`: The actual user prompt and the Solver's answer. Linked to the workflow.
- `evaluations`: The Critic's grade (`correct` boolean, `quality` string). Linked to the experience.
- `lessons`: The written text explaining what went wrong (or right). Linked to the evaluation. This table contains the `embedding` column powered by `sqlite-vec`.

---

## 4. Component Diagram

This diagram illustrates the high-level structural dependencies and how each component interacts.

```mermaid
graph TD
    UI[ADK Web UI] -->|Prompt| Hook(hook.py)
    DevUI[Streamlit Developer UI] -->|SQL Queries| DB[(SQLite Database)]
    
    Hook --> Main[main.py Pipeline]
    
    subgraph Agents
        Planner[Planner Agent]
        Retrieval[Retrieval Agent]
        Strategy[Strategy Agent]
        Solver[Solver Agent]
        Critic[Critic Agent]
    end
    
    Main --> Planner
    Main --> Retrieval
    Main --> Strategy
    Main --> Solver
    Main --> Critic
    
    Planner --> LLM{LiteLLM}
    Solver --> LLM
    Critic --> LLM
    
    Retrieval -->|Embeddings| Vec[sqlite-vec]
    Vec --> DB
    
    Strategy -->|Query Past Success| DB
    Critic -->|Save Experience & Lessons| DB
    Main -->|Save Workflow Trace| DB
    
    subgraph Memory Engine
        DB
        Vec
        Graph[GraphQLite]
    end
    
    Graph -.->|Maps Relational to Graph| DB
```
