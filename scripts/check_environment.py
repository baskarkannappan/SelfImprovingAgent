import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def load_configuration():
    """Loads environment variables, falling back to .env.example if .env is missing."""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    elif env_example_path.exists():
        load_dotenv(dotenv_path=env_example_path)
    else:
        print("Error: Neither .env nor .env.example found.", file=sys.stderr)
        sys.exit(1)

def run_check(name, command, success_text=None):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode == 0 and (success_text is None or success_text in result.stdout.lower() or success_text in result.stderr.lower()):
            print(f"[PASS] {name}")
            return True
        else:
            print(f"[FAIL] {name}")
            return False
    except FileNotFoundError:
        print(f"[FAIL] {name} (executable not found)")
        return False
    except Exception as e:
        print(f"[FAIL] {name} (error: {e})")
        return False

def check_python():
    if sys.version_info >= (3, 11):
        print("[PASS] Python 3.11+")
        return True
    print(f"[FAIL] Python 3.11+ (Found {sys.version.split()[0]})")
    return False

def check_sqlite_vec():
    try:
        import sqlite3
        import sqlite_vec
        db = sqlite3.connect(":memory:")
        db.enable_load_extension(True)
        sqlite_vec.load(db)
        print("[PASS] sqlite-vec extension")
        return True
    except Exception as e:
        print(f"[FAIL] sqlite-vec extension (error: {e})")
        return False

def check_graphqlite():
    try:
        import graphqlite
        print("[PASS] GraphQLite extension")
        return True
    except ImportError as e:
        print(f"[FAIL] GraphQLite extension (error: {e})")
        return False

def check_adk():
    try:
        import google.adk
        print("[PASS] Google ADK 2 imported")
        return True
    except ImportError as e:
        print(f"[FAIL] Google ADK 2 imported (error: {e})")
        return False

def check_litellm():
    try:
        import litellm
        print("[PASS] LiteLLM imported")
        return True
    except ImportError as e:
        print(f"[FAIL] LiteLLM imported (error: {e})")
        return False

def check_llm_connection():
    try:
        import litellm
        import os
        base_url = os.getenv("LLM_BASE_URL", "http://localhost:11434")
        model = os.getenv("LLM_MODEL", "llama3.2")
        print(f"[INFO] Testing connection to {base_url} with model {model}...")
        response = litellm.completion(
            model=f"ollama/{model}",
            messages=[{"role": "user", "content": "Calculate 15% of 200. Just output the number."}],
            api_base=base_url,
            max_tokens=10
        )
        if response and response.choices:
            print(f"[PASS] Local LLM endpoint ({base_url})")
            print(f"[PASS] {model} model available")
            return True
        else:
            print(f"[FAIL] Local LLM endpoint ({base_url}) returned empty response")
            return False
    except Exception as e:
        print(f"[FAIL] Local LLM endpoint (error: {e})")
        return False

def check_embedding():
    try:
        import litellm
        import os
        base_url = os.getenv("EMBEDDING_BASE_URL", "http://localhost:11434")
        model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
        print(f"[INFO] Testing embedding generation to {base_url} with model {model}...")
        response = litellm.embedding(
            model=f"ollama/{model}",
            input=["Calculate 15% of 200."],
            api_base=base_url
        )
        if response and response.data and len(response.data[0]['embedding']) > 0:
            print(f"[PASS] {model} embedding model available")
            return True
        else:
            print(f"[FAIL] {model} embedding model returned empty response")
            return False
    except Exception as e:
        print(f"[FAIL] {model} embedding model (error: {e})")
        return False

def main():
    load_configuration()
    
    print("=============================================")
    print("Self-Improving Agent - Environment Check")
    print("=============================================\n")
    
    all_passed = True
    
    # User Story 1: Basic tools
    all_passed &= check_python()
    all_passed &= run_check("uv", ["uv", "--version"], "uv")
    all_passed &= run_check("Git", ["git", "--version"], "git version")
    all_passed &= run_check("Docker Desktop", ["docker", "--version"], "docker version")
    
    # User Story 2: Database Setup
    all_passed &= run_check("SQLite", ["python", "-c", "import sqlite3"], "")
    all_passed &= check_sqlite_vec()
    all_passed &= check_graphqlite()
    
    # User Story 3: LLM Connectivity
    all_passed &= check_adk()
    all_passed &= check_litellm()
    all_passed &= check_llm_connection()
    all_passed &= check_embedding()
    
    print("\n=============================================")
    if all_passed:
        print("Environment is ready.")
        print("=============================================")
        sys.exit(0)
    else:
        print("Environment check failed. Please resolve the issues above.")
        print("=============================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
