"""
管理大模型客户端
"""
import os
from langchain_deepseek import ChatDeepSeek
import dotenv

os.environ["DEEPSEEK_API_KEY"] = dotenv.get_key(".env", "DEEPSEEK_API_KEY")

def get_deepseek_model():
    return ChatDeepSeek(model="deepseek-chat")