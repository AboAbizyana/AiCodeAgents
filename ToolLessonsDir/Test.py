from RecoveryLoop import recovery_loop

code = """
a = 10
b = 20
print(a + c)
"""

result = recovery_loop(code, max_retries=3)

print("Status:", result["status"])
print("Success:", result["success"])
print("Retries:", result["retries_used"])
print("History length:", len(result["history"]))