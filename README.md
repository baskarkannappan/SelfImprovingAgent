# 🧠 Self-Improving Agents

Welcome to **Self-Improving Agents**, a local-first, multi-agent AI system built on top of the Google ADK (Agent Development Kit). This system is designed to not just answer prompts, but to **learn from its mistakes, adapt to user preferences, and continuously optimize its own strategies** over time.

Instead of a generic LLM wrapper, this project implements a highly orchestrated assembly line of specialized agents (Planner, Retrieval, Strategy, Solver, Critic) that read and write their experiences to a local graph database (SQLite + sqlite-vec).

---

## 🌟 Key Features

* **Self-Improving Memory Loop**: The Critic agent grades every generated answer and writes out a "Lesson Learned". Future prompts automatically retrieve these lessons via vector embeddings, ensuring the system never makes the exact same mistake twice.
* **Epsilon-Greedy Strategy Optimization**: A dedicated Strategy Agent evaluates whether to use a "Fast" workflow or a "Complex/Deep Thinking" workflow based on historical success rates, actively exploring new strategies 10% of the time to break out of local optimums.
* **100% Local Execution**: Everything runs strictly on your machine. We use LiteLLM to interface with a local `llama3.2` container and `nomic-embed-text` for vector generation. Your data never leaves your computer.
* **Graph Traceability**: Execution traces, strategy decisions, experiences, evaluations, and lessons are all linked via GraphQLite, creating an analyzable graph of the AI's learning journey.
* **Continuous Improvement Benchmark**: Includes a built-in automated testing suite to mathematically prove the AI has gotten smarter by comparing a "baseline" run (empty memory) against a "post-learning" run (populated memory).

---

## 📖 Deep Dives & Documentation

To understand the system in depth, please read our accompanying documentation:
- **[TUTORIAL.md](./TUTORIAL.md)**: A simple, non-technical explanation of how the different AI agents work together as a team.
- **[ARCHITECTURE.md](./ARCHITECTURE.md)**: High-level technical design, including Mermaid Sequence Diagrams and Component Interactions.

---

## 🛠️ Prerequisites

- **OS:** Windows 10/11 (macOS/Linux compatible with minor tweaks)
- **Python:** 3.11+
- **Dependency Manager:** [uv](https://github.com/astral-sh/uv)
- **Local LLM Engine:** [Ollama](https://ollama.com/) running `llama3.2` and `nomic-embed-text`
- **Docker:** (Optional, but recommended for running the Ollama container)

---

## 🚀 Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/baskarkannappan/SelfImprovingAgent.git
   cd SelfImprovingAgent
   ```

2. **Install dependencies using `uv`:**
   ```bash
   uv sync
   ```

3. **Configure Environment Variables:**
   Copy the example environment file and verify the settings.
   ```bash
   cp .env.example .env
   ```
   *Default `.env` settings:*
   ```env
   LLM_BASE_URL=http://localhost:11434
   LLM_MODEL=llama3.2
   EMBEDDING_BASE_URL=http://localhost:11434
   EMBEDDING_MODEL=nomic-embed-text
   DATABASE_PATH=data/agent.db
   ```

4. **Verify your environment:**
   Run our comprehensive setup script to ensure SQLite, Ollama, and LiteLLM are correctly configured.
   ```bash
   uv run python scripts/check_environment.py
   ```

---

## 🎮 Usage

This project uses two main interfaces: the Chat UI to interact with the agents, and the Developer Dashboard to monitor the AI's "brain".

### 1. The Chat Interface (Google ADK)
To chat with the Self-Improving Agent, start the ADK web server:
```bash
uv run adk web
```
This will spin up a local chat interface (usually at `http://localhost:8000`) where you can send prompts and watch the multi-agent orchestration happen in real time.

### 2. The Developer Dashboard (Streamlit)
To peer into the AI's memory, view strategy leaderboards, or analyze the execution graph, open a new terminal and run:
```bash
uv run streamlit run developer_ui/app.py
```
This opens a beautiful dashboard (usually at `http://localhost:8501`) featuring:
- **Strategy Registry & Performance:** See which workflows are winning.
- **Execution Trace:** A detailed breakdown of every agent's thought process.
- **Memory Browser & Graph View:** Inspect raw database lessons and follow the GraphQLite graph.
- **Continuous Improvement:** Benchmark comparisons to track learning.

---

## 📈 Running the Benchmarks

Want to prove the system actually learns? We've included a Continuous Improvement Benchmark script that runs standard tasks against the AI with an empty database, and then runs them again with its accumulated memory.

Run the provided PowerShell script:
```powershell
.\run_benchmarks.ps1
```
Once complete, open the **Continuous Improvement** page in the Streamlit Developer UI to see the exact percentage increase in success rate and quality!

---

## 🧪 Testing

To run the internal unit tests:
```bash
uv run pytest
```
