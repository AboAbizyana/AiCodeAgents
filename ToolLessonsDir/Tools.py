import json
import os
import subprocess
from tempfile import NamedTemporaryFile
import sys
import uuid
from StructuredData import MetricsSchema

def multiply(a: int, b: int) -> int:
    return a * b

def call_infp(tool_call_: list) -> dict:
    tool_call_ = tool_call_[0]

    dd = {'Tool name': tool_call_.function.name,
          'Arguments': json.loads(tool_call_.function.arguments),
          'Tool call ID': tool_call_.id}
    return dd

def execute_tool(tool_call_: list, tools_:dict) -> dict:
    info = call_infp(tool_call_)

    tool_name = info['Tool name']

    if tool_name not in tools_:

        return {'tool_name': tool_name,
                'tool_call_id': info['Tool call ID'],
                'tool_found': False,
                'result': None,
                'success': False}

    func = tools_[tool_name]

    arg = info['Arguments']
    if set(arg.keys()) != {"a", "b"}:
        raise ValueError("Arguments must contain exactly a and b")

    if not all(type(arg[k]) is int for k in ("a", "b")):
        raise TypeError("Both arguments must be integers")

    result = func(**arg)

    return {'tool_name': tool_name,
            'tool_call_id': info['Tool call ID'],
            'tool_found': True,
            'result': result,
            'success': True}


def execute_python_sandbox(code: str, timeout: int) -> dict:

    if not isinstance(code, str):
        raise TypeError("The code should be a string")
    if type(timeout) is not int:
        raise TypeError("timeout must be an integer")

    if timeout <= 0:
        raise ValueError("timeout must be positive")

    container_name = f"python-sandbox-{uuid.uuid4().hex}"
    cleanup_success = True
    result = None

    with NamedTemporaryFile(mode='w', suffix='.py') as f:
        f.write(code)
        f.flush()
        path = f.name
        os.chmod(path, 0o644)
        execute_methode = [
            "podman", "run", "--rm",
            "--name", container_name,
            "--network=none",
            "--read-only",
            "--cap-drop=ALL",
            "--security-opt=no-new-privileges",
            "--memory=256m",
            "--cpus=1",
            "--pids-limit=64",
            "--user=65534:65534",
            "--pull=never",
            "-v", f"{path}:/sandbox/script.py:ro",
            "docker.io/library/python:3.12-slim",
            "python", "-I", "-B", "/sandbox/script.py"
        ]
        try:
            res = subprocess.run(execute_methode, timeout=timeout + 5, capture_output=True, text=True)

            if res.returncode == 0:
                error_source = "none"
            elif res.returncode in (125, 126, 127):
                error_source = "infrastructure"
            else:
                error_source = "python"

            result = {
                "filename": path,
                "exit_code": res.returncode,
                "stdout": res.stdout,
                "stderr": res.stderr,
                "success": res.returncode == 0,
                "error_source": error_source,
                "timed_out": False,
                "cleanup_success": None
            }

        except subprocess.TimeoutExpired as e:
            stdout = e.stdout.decode(errors="replace") if e.stdout else ""

            result = {
                "filename": path,
                "exit_code": None,
                "stdout": stdout,
                "stderr": str(e),
                "success": False,
                'error_source': 'timeout',
                "timed_out": True,
                'cleanup_success': None
            }

        except FileNotFoundError as e:
            result = {
                "filename": path,
                "exit_code": None,
                "stdout": "",
                "stderr": str(e),
                "error_source": "infrastructure",
                "timed_out": False,
                "success": False,
                'cleanup_success': None
            }

        finally:
            try:
                subprocess.run(
                    ["podman", "rm", "-f", "--ignore", container_name],
                    capture_output=True,
                    text=True,
                    timeout=20,
                    check=True
                )


            except (
                    subprocess.TimeoutExpired,
                    subprocess.CalledProcessError,
                    FileNotFoundError
            ):
                cleanup_success = False

        result["cleanup_success"] = cleanup_success

        return result


def parse_metrics(stdout: str) -> MetricsSchema | None:
    if not isinstance(stdout, str):
        raise TypeError("stdout must be a string")

    metrics = None
    lines = stdout.splitlines()

    for line in lines:
        line = line.lstrip()
        if line.startswith("METRICS "):
            json_text = line[len("METRICS "):]
            data = json.loads(json_text)
            metrics = MetricsSchema.model_validate(data)
            break


    return metrics

