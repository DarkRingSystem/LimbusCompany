import os
from langchain.chat_models import init_chat_model
from langchain_deepseek import ChatDeepSeek
os.environ["DEEPSEEK_API_KEY"] = "sk-73f715ab4a8b41ac85fd1ffd925a46f4"

# 非流式
llm = init_chat_model("deepseek:deepseek-chat")
response = llm.invoke("你好")
print(response)

# 流式输出
for text in llm.stream("你好"):
    print(text, end="", flush=True)


