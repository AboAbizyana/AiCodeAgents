from Tools import execute_python_sandbox
from ErrorRecovery import analyze_error

def recovery_loop(code: str, max_retries: int = 3) -> dict:

    current_code = code
    history = []
    retries_used = 0

    for attempt in range(max_retries):
        ...