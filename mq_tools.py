import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

def get_rabbitmq_tools():
    """获取rabbitmq工具"""
    client = MultiServerMCPClient(
        {
            "rabbitmq_mcp_server": {
                "command": "node",
                "args": ["/Users/darkringsystem/AI/rabbitmq-mcp-server/rabbitmq-mcp-server/build"],
                "transport": "stdio",
                "env": {
                    "RABBITMQ_HOST": "10.10.2.236",
                    "RABBITMQ_PORT": "30621",
                    "RABBITMQ_USER": "admin",
                    "RABBITMQ_PASS": "Parav1ew!",
                    "RABBITMQ_VHOST": "/"
                    }
                }
            }
    )
    tools = asyncio.run(client.get_tools())
    return tools

