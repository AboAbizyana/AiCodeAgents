from CoderAgent import coder_agent
from Tools import execute_python_sandbox
from RecoveryLoop import recovery_loop

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

result = recovery_loop(answer.code, max_retries=3)

print("Status:", result["status"])
print("Success:", result["success"])
print("Final code:", result["final_code"])

confirmation = input("\nExecute this code? (yes/no): ")

if confirmation != "yes":
    print("Execution cancelled.")
    raise SystemExit

ans = execute_python_sandbox(result["final_code"], 20)

print("Success:", ans["success"])
print('Result (stdout): ', ans["stdout"])
print('Result (stderr): ', ans["stderr"])
