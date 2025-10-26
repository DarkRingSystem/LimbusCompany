import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
import dotenv

zhipu_api_key = dotenv.get_key(".env", "ZHIPU_API_KEY")

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"{city}，今天是晴天，温度为 25 摄氏度。!"

def get_zhipu_search_mcp_tools():
    client = MultiServerMCPClient(
        {
            "search": {
                "url": "https://open.bigmodel.cn/api/mcp/web_search/sse?Authorization="+zhipu_api_key,
                "transport": "sse",
            }
        }
    )
    tools = asyncio.run(client.get_tools())
    return tools

