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

def get_deepseek_model_with_t0():
    return ChatDeepSeek(model="deepseek-chat",
                        temperature=0)

def get_doubao_seed1_6_model():
    return ChatOpenAI(model="doubao-seed-1-6-251015",
                base_url= "https://ark.cn-beijing.volces.com/api/v3",
               api_key=dotenv.get_key(".env", "DOUBAO_API_KEY"))

def get_qwen_vl_model():
    return ChatOpenAI(model="qwen-vl-max-latest",base_url= "https://dashscope.aliyuncs.com/compatible-mode/v1",
               api_key=dotenv.get_key(".env", "VISION_API_KEY"))