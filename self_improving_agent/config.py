import os
from pathlib import Path
from dotenv import load_dotenv

# Load from .env if it exists, otherwise fallback to .env.example
env_path = Path(".env")
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv(dotenv_path=Path(".env.example"))

class Config:
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")
    EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", "http://localhost:11434")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "data/agent.db")
    MEMORY_TOP_K = int(os.getenv("MEMORY_TOP_K", "3"))
    MEMORY_SIMILARITY_THRESHOLD = float(os.getenv("MEMORY_SIMILARITY_THRESHOLD", "0.7"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    STRATEGY_MIN_SAMPLES = int(os.getenv("STRATEGY_MIN_SAMPLES", "5"))
    STRATEGY_EXPLORATION_RATE = float(os.getenv("STRATEGY_EXPLORATION_RATE", "0.1"))

config = Config()
