from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent
from llms import get_deepseek_model
from tools import get_weather, get_zhipu_search_mcp_tools

model = get_deepseek_model()

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant"
)


web_agent = create_agent(
    model=model,
    tools=get_zhipu_search_mcp_tools(),
    system_prompt="You are a helpful assistant"
)

test_case_generate = create_agent(
    model=model,
    tools=[],
    system_prompt="You are a helpful assistant"
)

