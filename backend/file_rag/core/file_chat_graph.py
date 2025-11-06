from typing import TypedDict, Annotated, Any
import base64
import os
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langgraph.graph import add_messages, StateGraph, START, END
from langgraph.runtime import Runtime
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_community.document_loaders.parsers import LLMImageBlobParser

from file_rag.core.llms import get_deepseek_model, get_doubao_seed1_6_model

chat_model = get_deepseek_model()
pic_model = get_doubao_seed1_6_model()

# 创建中间件
@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """
    在模型调用前处理消息，特别是处理 PDF 文件
    1. 提取 PDF 内容并作为系统消息添加到上下文中
    2. 从原始消息中移除 file 类型的字段（因为 DeepSeek 等模型不支持 file 类型）
    3. 只保留 text 类型的字段传递给模型
    """
    print("Before model logs")
    print(state["messages"])

    messages = state.get("messages", [])
    if not messages:
        return None

    # 存储提取的 PDF 内容
    pdf_contents = []
    # 标记是否需要更新消息
    need_update = False

    # 遍历消息，查找包含 PDF 文件的消息
    for i, message in enumerate(messages):
        if not isinstance(message, HumanMessage):
            continue

        # 检查消息内容是否为列表（多模态消息格式）
        if not isinstance(message.content, list):
            continue

        # 遍历消息内容，查找 PDF 文件并过滤掉 file 类型
        new_content = []
        has_pdf = False

        for content_item in message.content:
            if isinstance(content_item, dict):
                content_type = content_item.get('type', '')
                mime_type = content_item.get('mime_type', '')

                # 检查是否为 PDF 文件
                # 支持格式: {'type': 'file', 'mime_type': 'application/pdf', 'source_type': 'base64', 'data': '...'}
                is_pdf = (content_type == 'file' and
                         (mime_type == 'application/pdf' or 'pdf' in mime_type.lower()) and
                         content_item.get('source_type') == 'base64')

                if is_pdf:
                    has_pdf = True
                    # 提取 base64 数据和文件名
                    base64_data = content_item.get('data', '')
                    filename = content_item.get('metadata', {}).get('filename', 'temp.pdf')

                    print(f"检测到PDF文件: {filename}, mime_type: {mime_type}")

                    try:
                        # 解码 base64 数据
                        pdf_bytes = base64.b64decode(base64_data)

                        # 确保缓存目录存在
                        cache_dir = "backend/cache_data"
                        os.makedirs(cache_dir, exist_ok=True)

                        # 创建临时 PDF 文件
                        temp_pdf_path = os.path.join(cache_dir, f"temp_{filename}")
                        with open(temp_pdf_path, 'wb') as f:
                            f.write(pdf_bytes)

                        # 使用 PyMuPDF4LLMLoader 提取 PDF 内容
                        loader = PyMuPDF4LLMLoader(
                            temp_pdf_path,
                            mode="page",
                            extract_images=True,
                            images_parser=LLMImageBlobParser(
                                model=pic_model
                            ),
                        )
                        docs = loader.load()

                        # 将提取的文档内容合并
                        extracted_text = "\n\n".join([doc.page_content for doc in docs])

                        # 将提取的内容添加到列表中，稍后作为系统消息插入
                        pdf_contents.append({
                            'filename': filename,
                            'content': extracted_text,
                            'pages': len(docs)
                        })

                        print(f"成功提取 PDF 文件 '{filename}' 的内容，共 {len(docs)} 页")

                        # 清理临时文件（可选）
                        # os.remove(temp_pdf_path)

                    except Exception as e:
                        print(f"处理 PDF 文件时出错: {e}")
                        # 如果处理失败，记录错误
                        pdf_contents.append({
                            'filename': filename,
                            'content': f"[错误: 无法处理此PDF文件 - {str(e)}]",
                            'pages': 0
                        })

                    # 不将 PDF 文件添加到 new_content（过滤掉 file 类型）
                    # 因为 DeepSeek 等模型不支持 file 类型，只支持 text 和 image_url
                    print(f"已从消息中移除 PDF 文件字段: {filename}")

                elif content_type == 'file':
                    # 其他类型的 file 也需要过滤掉
                    print(f"警告: 检测到不支持的 file 类型: {mime_type}，已从消息中移除")
                    need_update = True
                else:
                    # 保留 text 和 image_url 等其他类型
                    new_content.append(content_item)
            else:
                new_content.append(content_item)

        # 如果有 PDF 文件，更新消息内容（移除 file 类型字段）
        if has_pdf and new_content != message.content:
            messages[i] = HumanMessage(
                content=new_content,
                additional_kwargs=message.additional_kwargs,
                response_metadata=message.response_metadata,
                id=message.id
            )
            need_update = True

    # 如果提取到了 PDF 内容，将其作为系统消息插入到消息列表中
    if pdf_contents:
        # 构建系统消息内容
        system_content_parts = []
        for pdf_info in pdf_contents:
            system_content_parts.append(
                f"## PDF文件: {pdf_info['filename']}\n"
                f"（共 {pdf_info['pages']} 页）\n\n"
                f"{pdf_info['content']}"
            )

        system_message_content = (
            "以下是用户上传的PDF文件内容，请基于这些内容回答用户的问题：\n\n" +
            "\n\n---\n\n".join(system_content_parts)
        )

        # 创建系统消息
        system_message = SystemMessage(content=system_message_content)

        # 在最后一条消息之前插入系统消息
        # 这样的顺序是: [...历史消息, 系统消息(PDF内容), 最新用户消息(已移除file字段)]
        updated_messages = messages[:-1] + [system_message, messages[-1]]

        print(f"已将 {len(pdf_contents)} 个PDF文件的内容作为系统消息添加到上下文中")
        print(f"已从用户消息中移除 file 类型字段，只保留 text 和 image_url 类型")

        # 返回更新后的消息列表
        return {"messages": updated_messages}

    # 如果没有 PDF 文件但有其他 file 类型需要过滤
    if need_update:
        print("已从消息中移除不支持的 file 类型字段")
        return {"messages": messages}

    # 如果没有任何需要处理的内容，返回 None（不修改消息）
    return None

# 构建PDF加载器，使用多模态大模型解析PDF中的图片
# loader = PyMuPDF4LLMLoader(
#     "./cache_data/layout-parser-paper.pdf",
#     mode="page",
#     extract_images=True,
#     images_parser=LLMImageBlobParser(
#         model=pic_model
#     ),
# )
# docs = loader.load()

# print(docs[5].page_content[1863:])


# 基础助手 - 负责文本类对话
chat_agent = create_agent(
    model=chat_model,
    middleware=[log_before_model],
    tools=[],
    system_prompt="""你是一个专业的AI对话助手，具备以下能力：

## 核心职责
- 提供准确、有帮助的信息和建议
- 进行自然流畅的多轮对话
- 理解用户意图并给出针对性的回答

## 交互原则
1. **清晰准确**：回答要简洁明了，避免冗长和模糊
2. **友好专业**：保持礼貌和专业的语气
3. **主动引导**：当用户问题不明确时，主动询问细节
4. **结构化输出**：对于复杂问题，使用列表、分点等方式组织答案

## 回答格式
- 对于简单问题：直接给出答案
- 对于复杂问题：先总结要点，再详细说明
- 对于需要步骤的问题：使用编号列表清晰展示

请始终以用户需求为中心，提供最有价值的帮助。"""
)

# 图片分析助手 - 负责图片类对话，用户上传图片时进行分析和对话
pic_agent = create_agent(
    model=pic_model,
    middleware=[log_before_model],
    tools=[],
    system_prompt="""你是一个专业的图像分析助手，擅长理解和分析各类视觉内容。

## 核心能力
- **图像识别**：准确识别图片中的物体、场景、人物、文字等元素
- **细节观察**：注意图片中的细节、颜色、构图、光线等特征
- **内容理解**：理解图片的主题、情感、意图和上下文
- **文字提取**：识别并提取图片中的文字内容（OCR）

## 分析流程
1. **整体概览**：先描述图片的整体内容和主题
2. **关键元素**：识别并说明图片中的主要元素
3. **细节分析**：根据用户需求，深入分析特定细节
4. **回答问题**：针对用户的具体问题给出准确答案

## 输出原则
- **客观描述**：基于图片实际内容，避免过度推测
- **结构清晰**：使用分点、分段等方式组织答案
- **重点突出**：优先说明用户关心的内容
- **准确性优先**：如果某些内容不确定，明确说明

## 特殊场景处理
- 图表/数据可视化：提取关键数据和趋势
- 文档/截图：识别文字并理解文档结构
- 产品图片：描述产品特征和细节
- 场景照片：分析场景、氛围和构图

请根据用户上传的图片内容和提问，提供专业、准确的分析和回答。"""
)

# 文档类助手 - 负责文档类对话，用户上传PDF文档时进行分析和对话
pdf_agent = create_agent(
    model=chat_model,
    middleware=[log_before_model],
    tools=[],
    system_prompt="""你是一个专业的文档分析助手，擅长理解、总结和分析各类PDF文档。

## 核心能力
- **文档理解**：快速理解文档的主题、结构和核心内容
- **信息提取**：准确提取文档中的关键信息、数据和观点
- **内容总结**：生成简洁准确的文档摘要
- **深度分析**：对文档内容进行深入分析和解读
- **问答交互**：基于文档内容回答用户的具体问题

## 分析方法
1. **快速浏览**：先了解文档的整体结构和主要章节
2. **关键信息**：识别标题、摘要、结论等关键部分
3. **内容梳理**：理清文档的逻辑脉络和论述结构
4. **针对回答**：根据用户问题，定位相关内容并给出答案

## 输出格式
### 文档总结时
- **文档概述**：简要说明文档类型、主题和目的
- **核心内容**：提炼3-5个关键要点
- **重要细节**：补充必要的数据、案例或论据
- **结论建议**：总结文档的主要结论或建议

### 回答问题时
- **直接答案**：先给出简洁的答案
- **依据说明**：引用文档中的相关内容作为依据
- **补充信息**：提供相关的背景或延伸信息
- **页码标注**：如果可能，标注信息来源的页码

## 处理原则
- **忠于原文**：基于文档实际内容，不添加文档中没有的信息
- **结构化呈现**：使用标题、列表、分段等方式清晰组织答案
- **重点突出**：优先展示最重要和最相关的内容
- **准确引用**：引用文档内容时保持准确性

## 特殊文档类型
- **学术论文**：关注研究问题、方法、结果和结论
- **技术文档**：注重技术细节、参数和使用说明
- **商业报告**：提取数据、趋势和商业洞察
- **合同协议**：识别关键条款、权利义务和重要日期

注意：文档内容已经通过中间件提取并添加到上下文中，你可以直接基于这些内容进行分析和回答。"""
)

# 定义数据状态类型
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    file_type: str  # 文件类型: "chat", "pic", "pdf"

# 定义节点
def check_file_type_node(state: State):
    """
    检查用户消息中的文件类型
    返回: "chat" (纯文本), "pic" (包含图片), "pdf" (包含PDF文件)
    """
    messages = state["messages"]
    if not messages:
        return {"file_type": "chat"}

    # 获取最后一条消息（用户的最新输入）
    last_message = messages[-1]

    # 检查消息内容
    if isinstance(last_message, HumanMessage) and isinstance(last_message.content, list):
        # 遍历消息内容，检查是否包含图片或文件
        for content_item in last_message.content:
            if isinstance(content_item, dict):
                content_type = content_item.get('type', '')

                # 检查是否包含图片（支持 image 和 image_url 两种格式）
                if content_type == 'image' or content_type == 'image_url':
                    print(f"检测到图片类型: {content_type}")
                    return {"file_type": "pic"}

                # 检查是否包含 PDF 文件
                # 格式1: {'type': 'file', 'mime_type': 'application/pdf', ...}
                # 格式2: {'type': 'file', 'source_type': 'base64', 'mime_type': 'application/pdf', ...}
                if content_type == 'file':
                    mime_type = content_item.get('mime_type', '')
                    if mime_type == 'application/pdf' or 'pdf' in mime_type.lower():
                        print(f"检测到PDF文件: {mime_type}")
                        return {"file_type": "pdf"}

    # 默认返回纯文本类型
    print("检测到纯文本消息")
    return {"file_type": "chat"}

def call_chat_agent_node(state: State):
    """调用基础助手"""
    messages = state["messages"]
    result = chat_agent.invoke({"messages": messages})
    return {"messages": result["messages"]}

def call_pic_agent_node(state: State):
    """调用图片助手"""
    messages = state["messages"]
    result = pic_agent.invoke({"messages": messages})
    return {"messages": result["messages"]}

def call_pdf_agent_node(state: State):
    """调用文档助手"""
    messages = state["messages"]
    result = pdf_agent.invoke({"messages": messages})
    return {"messages": result["messages"]}

def condition_edge(state: State) -> str:
    """
    条件边函数：根据文件类型决定调用哪个助手
    返回下一个节点的名称
    """
    file_type = state.get("file_type", "chat")

    if file_type == "pic":
        return "call_pic_agent_node"
    elif file_type == "pdf":
        return "call_pdf_agent_node"
    else:
        return "call_chat_agent_node"  # 默认使用聊天助手

# 构建工作流图
agent_builder = StateGraph(State)

# 添加节点
agent_builder.add_node("check_file_type_node", check_file_type_node)  # 检查文件类型节点
agent_builder.add_node("call_chat_agent_node", call_chat_agent_node)  # 文本对话节点
agent_builder.add_node("call_pic_agent_node", call_pic_agent_node)    # 图片分析节点
agent_builder.add_node("call_pdf_agent_node", call_pdf_agent_node)    # PDF文档处理节点

# 设置入口点：从 START 开始，先检查文件类型
agent_builder.add_edge(START, "check_file_type_node")

# 添加条件边：根据文件类型路由到不同的处理节点
agent_builder.add_conditional_edges(
    "check_file_type_node",  # 源节点
    condition_edge,          # 条件函数
    {
        "call_chat_agent_node": "call_chat_agent_node",  # 纯文本 -> 文本助手
        "call_pic_agent_node": "call_pic_agent_node",    # 包含图片 -> 图片助手
        "call_pdf_agent_node": "call_pdf_agent_node",    # 包含PDF -> PDF助手
    }
)

# 所有处理节点完成后都返回到 END
agent_builder.add_edge("call_chat_agent_node", END)
agent_builder.add_edge("call_pic_agent_node", END)
agent_builder.add_edge("call_pdf_agent_node", END)

# 编译工作流图
graph = agent_builder.compile()

# 调试代码（可选）
# 测试纯文本对话
# result = graph.invoke({"messages": [HumanMessage(content="请生成1个正方形")]})
# print(result)








