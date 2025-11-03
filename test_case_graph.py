import os
from typing import TypedDict, Annotated

from langchain.agents import create_agent
from langchain_core.messages import SystemMessage
import dotenv
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph, add_messages
from langgraph.prebuilt import ToolNode
from tools import save_test_cases_to_excel

os.environ["DEEPSEEK_API_KEY"] = dotenv.get_key(".env", "DEEPSEEK_API_KEY")

model = init_chat_model(
    "deepseek:deepseek-chat",
    temperature=0
)

# Augment the LLM with tools
tools = [save_test_cases_to_excel]

# 将工具绑定到大模型对象
# 结果：应该调用哪个工具，以及工具参数是什么？
# 执行工具
# -------------------------------------
# 定义传输数据的状态

class State(TypedDict):
    # 定义状态数据类型信息和当前对话轮次
    messages: Annotated[list[AnyMessage], add_messages]
    current_turn : int

def call_llm_test_case_generation_node(state: State):
    """调用llm生成测试用例"""
    model_with_tools = model.bind_tools(tools)
    # 获取当前轮次
    current_turn = state.get("current_turn", 0)

    # 生成节点的系统提示词
    system_prompt = SystemMessage(content="""# 核心任务 (Core Task)

请基于用户的需求信息，为用户提供的需求设计一套完整的功能测试用例。

---

# 用例设计要求 (Test Case Design Requirements)

- **[测试维度]**: 你的设计必须至少覆盖以下维度：
    - **正向功能测试 (Happy Path):** 验证功能在正常、理想情况下的表现。
    - **边界值分析 (Boundary Value):** 针对有长度或数值限制的输入（如密码长度、验证码次数），测试其临界点。
    - **等价类划分 (Equivalence Partitioning):** 针对输入数据，划分为有效等价类和无效等价类进行测试。
    - **异常与错误场景测试 (Exception & Error Handling):** 模拟各种异常情况，如输入格式错误、网络中断、服务器无响应、权限不足等，验证系统的处理能力和提示信息。
    - **UI/UX 交互测试:** 验证界面布局、文案、控件状态（如按钮的可用/禁用）、跳转逻辑是否符合设计。

- **[优先级划分]**: 请为每一条用例标注优先级（例如：P0-核心、P1-重要、P2-次要），以体现其重要程度。

- **[输出格式]**: 请严格按照以下Markdown表格格式输出你的测试用例，确保每一列都填写完整：

| 用例ID  | 测试模块    | 用例标题                     | 前置条件                | 操作步骤                                                     | 预期结果                                                   | 优先级 |
| :------ | :---------- | :--------------------------- | :---------------------- | :----------------------------------------------------------- | :--------------------------------------------------------- | :----- |
| TC-FUNC-001 | [模块名]    | [一个清晰概括的标题]         | [执行测试前系统所需的状态]  | [1. ...<br>2. ...<br>3. ...]                                 | [与操作步骤对应的、清晰可验证的结果]                       | [P0/P1/P2] |

---""")


    # 将大模型绑定的工具进行及用户问题一起发送给大模型，由大模型觉得调用哪些工具，同时生成工具的参数
    messages = state["messages"]
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [system_prompt] + messages
    result = model.invoke(messages)
    return {"messages": result,
            "current_turn" : current_turn + 1
            }

def call_llm_test_case_review_node(state: State):
    """调用llm评审测试用例"""
    current_turn = state.get("current_turn", 0)

    system_prompt = SystemMessage(content="""你是一个专业的测试用例评审专家。
请仔细评审已生成的测试用例，检查：
1. 测试用例是否完整
2. 测试步骤是否清晰
3. 预期结果是否明确
4. 是否覆盖了关键场景
5. 测试数据是否合理

如果用例完美，请直接输出“用例通过”。
如果发现问题，请输出“用例不通过”，并提出具体的改进建议。""")
    # 过滤消息，只保留用户消息和AI消息的内容，排除工具调用
    messages = state["messages"]
    filtered_messages = []

    for msg in messages:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            # 跳过包含工具调用的消息
            continue
        elif hasattr(msg, 'tool_call_id'):
            # 跳过工具响应消息
            continue
        else:
            filtered_messages.append(msg)

    # 添加系统提示词
    final_messages = [system_prompt] + filtered_messages

    result = model.invoke(final_messages)
    return {"messages": result, "current_turn": current_turn + 0}

def call_tool_excel_agent_node(state: State):
    excel_agent = create_agent(
        model=model,
        tools=tools,
        system_prompt="""根据用例信息，生成Excel文件。"""
    )
    messages = state["messages"]
    result = excel_agent.invoke({"messages": messages})
    return {
        "messages": result["messages"],
        "current_turn": state.get("current_turn", 0)
    }

def condition_edge(state: State):
    """根据当前轮次决定是否继续对话"""
    current_turn = state.get("current_turn", 0)

    # 获取最后一条消息（评审结果）
    last_message = state["messages"][-1] if state["messages"] else None
    
    # 如果评审通过，调用工具生成Excel
    if last_message and hasattr(last_message, 'content'):
        content = str(last_message.content).lower()
        if "用例通过" in content:
            return "call_tool_excel_agent_node"
    
    # 如果达到最大轮次，也调用工具
    if current_turn >= 3:
        return "call_tool_excel_agent_node"
    else:
        return "call_llm_test_case_generation_node"

tool_node = ToolNode(tools)

# 创建工作流
agent_builder = StateGraph(State)

# 添加节点
agent_builder.add_node("call_llm_test_case_generation_node", call_llm_test_case_generation_node)
agent_builder.add_node("call_llm_test_case_review_node", call_llm_test_case_review_node)
agent_builder.add_node("call_tool_excel_agent_node", call_tool_excel_agent_node)
agent_builder.add_node("condition_edge", condition_edge)
agent_builder.add_node("tool_node", tool_node)

#编排节点
agent_builder.add_edge(START, "call_llm_test_case_generation_node")
agent_builder.add_edge("call_llm_test_case_generation_node", "call_llm_test_case_review_node")
agent_builder.add_conditional_edges(
    "call_llm_test_case_review_node",  # 源节点
    condition_edge,                    # 条件判断函数
    {
        "call_tool_excel_agent_node": "call_tool_excel_agent_node",  # 使用工具生成excel
        "call_llm_test_case_generation_node": "call_llm_test_case_generation_node" # 评审不通过,继续优化用例
    }
)
agent_builder.add_edge("call_tool_excel_agent_node", END)
# 编译graph
graph = agent_builder.compile()

# Invoke
# from langchain.messages import HumanMessage
# messages = [HumanMessage(content="生成1正向个登录用例")]
# messages = graph.invoke({"messages": messages})
# for m in messages["messages"]:
#     m.pretty_print()