from CoderAgent import coder_agent
from Tools import execute_python_sandbox
from ErrorRecovery import analyze_error

task = input('Task: ')

answer = coder_agent(task)

print("\nExplanation:")
print(answer.explanation)

print("\nGenerated code:")
print(answer.code)

confirmation = input("\nExecute this code? (yes/no): ")

if confirmation != "yes":
    print("Execution cancelled.")
    raise SystemExit

result = execute_python_sandbox(answer.code, 5)

if result['cleanup_success'] is False:
    print("Clean up failed.")
    raise SystemExit
elif result['success'] is True:
    print("Success!!")
    print(f'Result (stdout): {result['stdout']}')
elif result['error_source'] == 'python':
    print('Python code Error')
    res = analyze_error(answer.code, result)
    print(f'Explanation:\n{res.explanation}')
    print(f'Corrected code:\n{res.corrected_code}')
elif result['error_source'] == 'infrastructure' or result['error_source'] == 'timeout':
    print(f'Error Source:\n{result["error_source"]}')
    print(f'Error (stderr):\n{result["stderr"]}')