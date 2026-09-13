import subprocess
import sys

def test_python_environment():
    assert sys.version_info >= (3, 11)

def test_uv_availability():
    result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "uv" in result.stdout.lower()

def test_git_availability():
    result = subprocess.run(["git", "--version"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "git version" in result.stdout.lower()

def test_docker_availability():
    result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "docker version" in result.stdout.lower()

def test_sqlite():
    import sqlite3
    assert sqlite3.sqlite_version_info >= (3, 0)

def test_sqlite_vec():
    import sqlite3
    import sqlite_vec
    
    db = sqlite3.connect(":memory:")
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    
    db.execute("CREATE VIRTUAL TABLE vec_test USING vec0(embedding float[3]);")
    db.execute("INSERT INTO vec_test(rowid, embedding) VALUES (1, '[0.1, 0.2, 0.3]')")
    db.commit()
    
    cursor = db.cursor()
    cursor.execute("SELECT rowid FROM vec_test WHERE embedding MATCH '[0.1, 0.2, 0.3]' ORDER BY distance LIMIT 1")
    assert cursor.fetchone()[0] == 1

def test_graphqlite():
    import graphqlite
    assert graphqlite is not None
def test_adk_import():
    import google.adk
    assert google.adk is not None

def test_litellm_import():
    import litellm
    assert litellm is not None

def test_llm_connection():
    import litellm
    assert callable(litellm.completion)

def test_embedding_model_available():
    import litellm
    assert callable(litellm.embedding)
