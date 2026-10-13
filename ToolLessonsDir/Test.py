from CoderAgent import coder_agent

answer = coder_agent(
    "Calculate the mean of [10, 20, 30, 40]"
)

print("Explanation:", answer.explanation)
print("Generated code:")
print(answer.code)