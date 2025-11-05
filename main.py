from langchain.agents import create_agent
from llms import get_deepseek_model
from mq_tools import get_rabbitmq_tools
from sql_tools import get_uat_pg_sql_tools, get_test_pg_sql_tools, get_test_es_tools
from tools import get_weather, get_zhipu_search_mcp_tools, get_chrome_mcp_tools, \
    get_mcp_server_chart_tools, get_filesystem_tools, get_excel_tools
from tools import save_test_cases_to_excel

model = get_deepseek_model()

# 基础助手 - 支持天气查询和文档转换
agent = create_agent(
    model=model,
    tools=[get_weather],
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
    tools=get_zhipu_search_mcp_tools(),
    system_prompt="""你是一个网络搜索助手。

你可以：
1. 使用网络搜索工具查找信息
2. 结合网络信息和文档内容为用户提供全面的答案"""
)

# UI自动化测试助手
# ui_auto_agent = create_agent(
#     model=model,
#     tools=get_chrome_mcp_tools() + get_mcp_server_chart_tools() + get_filesystem_tools() + save_test_cases_to_excel(),
#     system_prompt="""
#     你是一个UI自动化软件测试专家。
#     你可以使用使用 get_chrome_mcp_tools() 工具来操作浏览器。
#     根据用户提供的信息生成UI自动化测试用例并执行，生成的用例,先展示给用户，再使用save_test_cases_to_excel工具讲用例输出以Excel格式输出到/Users/darkringsystem/AI/LimbusCompany/files/UIAutoCases目录下。
#     然后把执行结果用get_mcp_server_chart_tools工具生成图表并展示给用户。
#     最后把测试报告以HTML格式保存到/Users/darkringsystem/AI/LimbusCompany/files/UIAutoReports目录下。
# 你可以：
# 1. 生成UI自动化测试用例
# 2. 操作浏览器执行测试用例
# 3. 生成Excel格式的测试用例并保存
# 5. 生成图表形式的测试报告
# 4. 保存HTML格式的测试报告
# """)

# API平台数据操作小助手
api_SQL_agent = create_agent(
    model=model,
    tools=get_test_pg_sql_tools() + get_mcp_server_chart_tools(),
    system_prompt="""
    你是一个API项目数据库操作小助手。
    你有以下几个功能：
    1. 关闭或开启平台登录验证码验证，你需要先读取是system的schema中的config表中loginConfig的value值，再根据其格式把verifyImage改为true或false
    2. 修改用户最后修改密码日期，你需要修改的是system的schema中的users表中的last_change_password_date字段，格式是yyyy-MM-dd
    3. 用户如果说清除某个环境的安全配置数据，请清理以下表格中的数据portal的schema中的risk_strategy和weakness_definition以及discovery_api_classified_rule和discovery_api_classified_rule_condition
    4. 如果用户有统计需求，就使用get_mcp_server_chart_tools展示合适的图表。
""")

# API平台ES查询小助手
api_ES_agent = create_agent(
    model=model,
    tools=get_test_es_tools(),
    system_prompt="""
你是一个Elasticsearch数据库查询专家，你连接的库里存储的是API网关平台的日志，输出文档时，使用原始json数据。
1.api-gateway里存储的是API网关的代理日志
2.api-composer里存储的是编排集群的日志
3.sensitive_api_record里存储的是敏感接口记录日志
""")


# API平台MQ小助手
api_MQ_agent = create_agent(
    model=model,
    tools=get_rabbitmq_tools(),
    system_prompt="""
你是一个MQ小助手，你可以连接到RabbitMQ中，对用户指定的队列发送消息。
如果需要查询，务必不要直接list所有队列和交换器，使用分页查询或者精确查询获得结果。
""")