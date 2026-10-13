from groq import Groq
import json
from StructuredData import ErrorRecoverySchema

client = Groq()

def analyze_error(code: str, result: dict) -> ErrorRecoverySchema:

    if not isinstance(code, str):
        raise TypeError("The code should be a string")
    if not isinstance(result, dict):
        raise TypeError("The result should be a dict")
    if result["success"]:
        raise ValueError("No execution error to fix")

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "ErrorRecoverySchema",
            "strict": True,
            "schema": ErrorRecoverySchema.model_json_schema()
        }
    }

    messages = [
        {
            "role": "system",
            "content": (
                "You are a Python debugging assistant. "
                "Analyze execution errors, explain their causes, "
                "and propose corrected Python code. "
                "Do not claim that your corrections were executed."
                "Distinguish Python exceptions from execution timeouts. "
                "Return the complete corrected Python code, not just a fragment. "
            )
        },
        {
            "role": "user",
            "content": (
                f"Original code:\n{code}\n\n"
                f"Execution result:\n{json.dumps(result)}\n\n"
                "Find the error and propose a correction."
            )
        }
    ]

    response = client.chat.completions.create(
        model='openai/gpt-oss-20b',
        messages=messages,
        response_format=response_format
    )

    ans = response.choices[0].message.content #json str
    ans = ErrorRecoverySchema.model_validate_json(ans)

    return ans