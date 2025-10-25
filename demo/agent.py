from langchain.agents import create_agent
from llms import get_deepseek_model

model = get_deepseek_model()

agent = create_agent(
    model,
    tools=[],
    system_prompt="你是个有用的AI助手",
)

# 非流式输出
# response = agent.invoke({"message":[{"role": "user", "content": "你好"}]})
# print(response)


# 流式输出
for item in agent.stream({"message":[{"role": "user", "content": "你好"}]}):
    print(item, end="", flush=True)