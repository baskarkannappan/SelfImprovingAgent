# Contract: Environment Validation Output

The `scripts/check_environment.py` script acts as the primary interface for Phase 0 validation. It produces a standard console output indicating the status of all required infrastructure components.

## Output Format

The script outputs to `stdout` in a human-readable format. Each checked dependency is listed with a `[PASS]` or `[FAIL]` prefix.

### Success Example
```text
=============================================
Self-Improving Agent - Environment Check
=============================================

[PASS] Python 3.11+
[PASS] uv
[PASS] Git
[PASS] Docker Desktop
[PASS] SQLite
[PASS] sqlite-vec extension
[PASS] GraphQLite extension

[PASS] Local LLM endpoint (http://localhost:11434)
[PASS] llama3.2 model available
[PASS] nomic-embed-text embedding model available

[PASS] Google ADK 2 imported
[PASS] LiteLLM imported

=============================================
Environment is ready.
=============================================
```

### Failure Example
```text
=============================================
Self-Improving Agent - Environment Check
=============================================

[PASS] Python 3.11+
[PASS] uv
[PASS] Git
[FAIL] Docker Desktop (Ensure Docker Desktop is running)

...

[FAIL] Local LLM endpoint (Unable to connect to http://localhost:11434)

=============================================
Environment check failed. Please resolve the issues above.
=============================================
```

## Expected Exit Codes
- `0`: All checks passed.
- `1`: One or more checks failed.
