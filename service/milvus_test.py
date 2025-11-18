from pymilvus import connections, utility

# 连接到 Milvus
connections.connect("default", host="localhost", port="19530")

# 检查连接状态
print(f"Milvus 版本: {utility.get_server_version()}")

print(f"Milvus 类型: {utility.get_server_type()}")
