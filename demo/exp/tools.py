"""
版权所有 (c) 2023-2026 北京慧测信息技术有限公司(但问智能) 保留所有权利。

本代码版权归北京慧测信息技术有限公司(但问智能)所有，仅用于学习交流目的，未经公司商业授权，
不得用于任何商业用途，包括但不限于商业环境部署、售卖或以任何形式进行商业获利。违者必究。

授权商业应用请联系微信：huice666
"""

import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"{city}，今天是晴天，温度为 25 摄氏度。!"

def get_zhipu_search_mcp_tools():
    client = MultiServerMCPClient(
        {
            "search": {
                "url": "https://open.bigmodel.cn/api/mcp/web_search/sse?Authorization=0d3c7b3d55c84d6682663dbdbdb3d614.cpoJIoZ3NFaqXARQ",
                "transport": "sse",
            }
        }
    )
    tools = asyncio.run(client.get_tools())
    return tools



# tools = get_zhipu_search_mcp_tools()
# print(tools)