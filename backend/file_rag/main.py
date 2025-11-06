from langchain.agents import create_agent
from file_rag.core.llms import get_deepseek_model,get_doubao_seed1_6_model

model = get_deepseek_model()


# 基础助手 - 负责文本类对话
agent = create_agent(
    model=model,
    tools=[],
    system_prompt="""你是一个文档助手"""
)


