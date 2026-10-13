from groq import Groq
from StructuredData import CoderSchema

def coder_agent(task: str) -> CoderSchema:
    if not isinstance(task, str):
        raise TypeError("Task must be a string")
    if not task.strip():
        raise ValueError("Task must not be empty")

    system_prompt = (
        "You are an expert Python programmer. "
        "Generate complete, runnable Python 3.12 code "
        "that solves the user's task. "
        "Use only the Python standard library. "
        "Print the final result to stdout. "
        "Do not use network requests, subprocesses, or file operations. "
        "Return a short explanation and the complete Python code."
    )

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "CoderSchema",
            "strict": True,
            "schema": CoderSchema.model_json_schema()
        }
    }

    messages = [{'role': 'system','content': system_prompt},
                {'role': 'user', 'content': task}]

    client = Groq()

    response = client.chat.completions.create(
        model = 'openai/gpt-oss-20b',
        messages = messages,
        response_format = response_format
    )

    answer = CoderSchema.model_validate_json(response.choices[0].message.content)

    return answer
