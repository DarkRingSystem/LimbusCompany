import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

def get_test_pg_sql_tools():
    """测试环境数据库信息"""
    client = MultiServerMCPClient(
        {
            "postgres_server": {
                "command": "npx",
                "args": ["-y", "mcp-postgres-server"],
                "transport": "stdio",
                "env": {
                    "PG_HOST": "192.168.7.106",
                    "PG_PORT": "5432",
                    "PG_USER": "api",
                    "PG_PASSWORD": "Api@abc123",
                    "PG_DATABASE": "api-gateway"
                }
            }
        }
    )
    tools = asyncio.run(client.get_tools())
    return tools

def get_uat_pg_sql_tools():
    """UAT环境数据库信息"""
    client = MultiServerMCPClient(
        {
            "postgres_server": {
                "command": "npx",
                "args": ["-y", "mcp-postgres-server"],
                "transport": "stdio",
                "env": {
                    "PG_HOST": "10.10.1.207",
                    "PG_PORT": "5432",
                    "PG_USER": "api",
                    "PG_PASSWORD": "Api@abc123",
                    "PG_DATABASE": "api-gateway"
                }
            }
        }
    )
    tools = asyncio.run(client.get_tools())
    return tools