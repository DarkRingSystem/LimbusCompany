from langchain.agents import create_agent
from llms import get_deepseek_model
from tools import get_weather, get_zhipu_search_mcp_tools, convert_document

model = get_deepseek_model()

# 基础助手 - 支持天气查询和文档转换
agent = create_agent(
    model=model,
    tools=[get_weather, convert_document],
    system_prompt="""你是一个有用的AI助手。

当用户上传文档时，使用 convert_document 工具来解析文档内容。
你可以帮助用户：
1. 转换各种格式的文档为 Markdown
2. 分析文档内容
3. 回答关于文档的问题
4. 提取文档中的关键信息"""
)


# 网络搜索助手 - 支持网络搜索和文档转换
web_agent = create_agent(
    model=model,
    tools=get_zhipu_search_mcp_tools() + [convert_document],
    system_prompt="""你是一个网络搜索助手。

你可以：
1. 使用网络搜索工具查找信息
2. 使用 convert_document 工具解析用户上传的文档
3. 结合网络信息和文档内容为用户提供全面的答案"""
)

# 测试用例生成助手 - 支持文档转换
test_case_generate = create_agent(
    model=model,
    tools=[convert_document],
    system_prompt="""你是一个软件测试专家。

当用户上传文档时，使用 convert_document 工具来解析文档内容。
根据用户提供的信息和上传的文档，生成专业且完整的测试用例。

你可以：
1. 解析需求文档
2. 分析功能规格
3. 生成详细的测试用例
4. 提供测试覆盖率建议"""
)

