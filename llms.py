"""
管理大模型客户端
"""
import os
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
import dotenv

os.environ["DEEPSEEK_API_KEY"] = dotenv.get_key(".env", "DEEPSEEK_API_KEY")

def get_deepseek_model():
    return ChatDeepSeek(model="deepseek-chat")

def get_doubao_seed_model():
    ChatOpenAI(model="doubao-seed-1-6-251015",
               base_url="https://openaia.com/api/v1/",
               api_key=dotenv.get_key(".env", "DOUBAO_SEED_API_KEY")
               )

def get_doubao_seed1_6_model():
    ChatOpenAI(model="doubao-seed-1-6-251015",
                base_url= "https://ark.cn-beijing.volces.com/api/v3",
               api_key=dotenv.get_key(".env", "DOUBAO_API_KEY"))