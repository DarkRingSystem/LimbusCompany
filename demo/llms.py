"""
管理大模型客户端
"""
import os
from langchain_deepseek import ChatDeepSeek
os.environ["DEEPSEEK_API_KEY"] = "sk-73f715ab4a8b41ac85fd1ffd925a46f4"

def get_deepseek_model():
    return ChatDeepSeek(model="deepseek-chat")



