import os
import logging
from typing import Literal

from langchain_community.document_loaders.parsers import LLMImageBlobParser
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_milvus import Milvus
from langchain_openai import ChatOpenAI
from langchain_pymupdf4llm import PyMuPDF4LLMLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition

# 导入配置
from .config import settings

# 配置日志
logger = logging.getLogger(__name__)

# 创建检索工具供llm使用
def create_retriever_tool(vectorstore: VectorStore):
    from langchain_classic.tools.retriever import create_retriever_tool
    # “VectorStoreRetriever
    # 支持 “相似性”（默认）、“mmr”（最大边际相关性，上文已描述）和 “相似性分数阈值” 这几种搜索类型。我们可以使用最后一种类型，根据相似性分数对检索器输出的文档进行阈值筛选。检索器可以轻松地集成到更复杂的应用程序中，例如检索增强型生成（RAG）应用程序，它将给定的问题与检索到的上下文结合起来，为
    # LLM
    # 构造提示。
    #
    # ### 解释说明
    # - ** VectorStoreRetriever
    # 支持的搜索类型 **：
    # - ** 相似性（similarity） ** ：这是默认的搜索类型，它会根据文档与查询之间的相似性来检索文档。相似性通常是通过计算文档向量和查询向量之间的距离（如余弦相似度）来衡量的。
    # - ** 最大边际相关性（mmr，maximum
    # marginal
    # relevance） ** ：这种搜索类型旨在平衡检索结果的相似性和多样性。它不仅考虑文档与查询的相似性，还会考虑文档之间的差异性，以避免检索到过于相似的文档，从而提高检索结果的多样性。
    # - ** 相似性分数阈值（similarity_score_threshold） ** ：这种搜索类型允许用户设置一个相似性分数的阈值，只有当文档的相似性分数高于这个阈值时，才会被检索出来。这可以用于过滤掉与查询相关性较低的文档，提高检索结果的质量。
    # - ** 检索器的应用 **：
    # - 检索器可以集成到更复杂的应用程序中，例如检索增强型生成（RAG）应用程序。

    retriever = vectorstore.as_retriever()

    retriever_tool = create_retriever_tool(
        retriever,
        "retrieve_api_config",
        "搜索并返回API平台配置信息",
    )
    # retriever_tool.invoke({"query": "API平台测试环境地址是？"})
    return retriever_tool

def retrieve_tool():
    """使用配置创建检索工具"""
    from langchain_ollama import OllamaEmbeddings

    # 使用配置中的 Embedding 设置
    embedding = OllamaEmbeddings(
        model=settings.embedding_model,
        base_url=settings.embedding_base_url,
        temperature=settings.embedding_temperature
    )

    # 使用配置中的 Milvus 设置
    vector_store = Milvus(
        embedding_function=embedding,
        connection_args={"uri": settings.milvus_uri},
        index_params={
            "index_type": settings.milvus_index_type,
            "metric_type": settings.milvus_metric_type
        },
    )
    return create_retriever_tool(vector_store)

# -----------------------------------------------------------------------


def get_deepseek_model():
    """使用配置创建 DeepSeek 模型"""
    os.environ["DEEPSEEK_API_KEY"] = settings.deepseek_api_key
    model = init_chat_model(
        f"deepseek:{settings.deepseek_model_name}",
        temperature=settings.llm_temperature
    )
    return model


# ===== 提示词模板 =====

GRADE_PROMPT = (
    "你是一个文档相关性评估专家，负责评估检索到的文档与用户问题的相关性。\n\n"
    "【检索到的文档】：\n{context}\n\n"
    "【用户问题】：\n{question}\n\n"
    "【评估标准】：\n"
    "- 如果文档包含与用户问题相关的关键词、概念或语义信息，则判定为相关\n"
    "- 如果文档内容能够帮助回答用户问题，则判定为相关\n"
    "- 如果文档与问题完全无关或信息不足，则判定为不相关\n\n"
    "【输出要求】：\n"
    "请给出二元评分：'yes'（相关）或 'no'（不相关）"
)

REWRITE_PROMPT = (
    "你是一个问题优化专家，擅长理解用户问题的深层语义意图并重新表述问题。\n\n"
    "【原始问题】：\n"
    "-------------------\n"
    "{question}\n"
    "-------------------\n\n"
    "【任务要求】：\n"
    "1. 分析问题的核心语义和潜在意图\n"
    "2. 识别问题中的关键概念和隐含需求\n"
    "3. 将问题重新表述得更加清晰、具体和易于检索\n"
    "4. 保持原问题的核心意图不变\n\n"
    "【优化后的问题】："
)

GENERATE_PROMPT = (
    "你是一个专业的问答助手，擅长基于检索到的上下文信息回答用户问题。\n\n"
    "【用户问题】：\n{question}\n\n"
    "【检索到的上下文】：\n{context}\n\n"
    "【回答要求】：\n"
    "1. 仔细阅读上下文信息，基于事实进行回答\n"
    "2. 如果上下文中包含答案，请准确提取并组织成连贯的回答\n"
    '3. 如果上下文信息不足以回答问题，请明确说明"根据现有信息无法回答"\n'
    "4. 回答要简洁明了，控制在3-5句话以内\n"
    "5. 使用专业、友好的语气\n"
    "6. 不要编造或推测上下文中没有的信息\n\n"
    "【你的回答】："
)


class AgenticRAGEngine:
    """Agentic RAG 引擎"""

    def __init__(self,
                 knowledge_base: str = None,
                 vector_service=None,
                 milvus_service=None):
        self.knowledge_base = knowledge_base or settings.default_knowledge_base
        self.vector_service = vector_service
        self.milvus_service = milvus_service
        self.retriever = None
        self.retriever_tool = None
        self.response_model = None
        self.grader_model = None
        self.graph = None
        self.file_processor = None
        self._initialized = False

    async def initialize(self):
        """初始化引擎"""
        if self._initialized:
            return

        try:
            # 初始化向量服务
            if self.vector_service is None:
                self.vector_service = await VectorServiceFactory.get_default_service()

            # 初始化Milvus服务
            if self.milvus_service is None:
                self.milvus_service = await MilvusServiceFactory.create_service(
                    knowledge_base=self.knowledge_base,
                    dimension=self.vector_service.dimension
                )

            # 创建检索工具
            if create_retriever_tool is not None:
                self.retriever_tool = create_retriever_tool(
                    self.retriever,
                    "retrieve_documents",
                    f"Search and return information from {self.knowledge_base} knowledge base."
                )

            # 初始化LLM模型
            if init_chat_model is not None:
                self.response_model = init_chat_model(
                    f"deepseek:{settings.llm_model}",
                    temperature=settings.llm_temperature,
                    max_tokens=settings.llm_max_tokens,
                    api_key=settings.llm_api_key,
                    base_url=settings.llm_api_base
                )
                self.grader_model = self.response_model

            # 构建图
            if StateGraph is not None:
                await self._build_graph()

            self._initialized = True
            logger.info(f"Agentic RAG engine initialized for knowledge base: {self.knowledge_base}")

        except Exception as e:
            logger.error(f"Failed to initialize Agentic RAG engine: {str(e)}")
            raise

    async def _build_graph(self):
        """构建LangGraph工作流"""
        workflow = StateGraph(MessagesState)

        # 添加节点
        workflow.add_node("generate_query_or_respond", self._generate_query_or_respond)
        workflow.add_node("retrieve", ToolNode([self.retriever_tool]))
        workflow.add_node("grade_documents", self._grade_documents)
        workflow.add_node("rewrite_question", self._rewrite_question)
        workflow.add_node("generate_answer", self._generate_answer)

        # 添加边
        workflow.add_edge(START, "generate_query_or_respond")

        # 决定是否检索
        workflow.add_conditional_edges(
            "generate_query_or_respond",
            tools_condition,
            {
                "tools": "retrieve",
                END: END,
            },
        )

        # 检索后的条件边
        workflow.add_conditional_edges(
            "retrieve",
            self._grade_documents,
        )

        workflow.add_edge("generate_answer", END)
        workflow.add_edge("rewrite_question", "generate_query_or_respond")

        # 编译图
        self.graph = workflow.compile()

    def _generate_query_or_respond(self, state):
        """生成查询或直接回答"""
        if self.response_model is None:
            return {"messages": [{"role": "assistant", "content": "LLM model not available"}]}

        try:
            response = (
                self.response_model
                .bind_tools([self.retriever_tool])
                .invoke(state["messages"])
            )
            return {"messages": [response]}
        except Exception as e:
            return {"messages": [{"role": "assistant", "content": f"Error: {str(e)}"}]}

    def _grade_documents(self, state) -> Literal["generate_answer", "rewrite_question"]:
        """评估检索文档的相关性"""
        if not settings.rag_enable_grading:
            return "generate_answer"

        if self.grader_model is None:
            return "generate_answer"

        try:
            question = state["messages"][0].content
            context = state["messages"][-1].content

            prompt = GRADE_PROMPT.format(question=question, context=context)

            # 注意：GradeDocuments 类需要在其他地方定义
            # 这里暂时注释掉结构化输出，使用简单的文本判断
            # response = (
            #     self.grader_model
            #     .with_structured_output(GradeDocuments)
            #     .invoke([{"role": "user", "content": prompt}])
            # )
            # score = response.binary_score

            # 简化版本：直接从模型响应中提取判断
            response = self.grader_model.invoke([{"role": "user", "content": prompt}])
            score = "yes" if "yes" in response.content.lower() else "no"

            if score == "yes":
                return "generate_answer"
            else:
                # 检查迭代次数
                iteration_count = getattr(state, 'iteration_count', 0)
                if iteration_count >= settings.rag_max_iterations:
                    return "generate_answer"
                return "rewrite_question"

        except Exception as e:
            logger.error(f"Error in grade_documents: {str(e)}")
            return "generate_answer"

    def _rewrite_question(self, state):
        """重写问题"""
        if not settings.rag_enable_rewrite:
            return {"messages": state["messages"]}

        if self.response_model is None:
            return {"messages": state["messages"]}

        try:
            messages = state["messages"]
            question = messages[0].content
            prompt = REWRITE_PROMPT.format(question=question)
            response = self.response_model.invoke([{"role": "user", "content": prompt}])

            # 增加迭代计数
            iteration_count = getattr(state, 'iteration_count', 0) + 1

            return {
                "messages": [{"role": "user", "content": response.content}],
                "iteration_count": iteration_count
            }
        except Exception as e:
            logger.error(f"Error in rewrite_question: {str(e)}")
            return {"messages": state["messages"]}

    def _generate_answer(self, state):
        """生成最终答案"""
        if self.response_model is None:
            return {"messages": [{"role": "assistant", "content": "LLM model not available"}]}

        try:
            question = state["messages"][0].content
            context = state["messages"][-1].content
            prompt = GENERATE_PROMPT.format(question=question, context=context)
            response = self.response_model.invoke([{"role": "user", "content": prompt}])
            return {"messages": [response]}
        except Exception as e:
            logger.error(f"Error in generate_answer: {str(e)}")
            return {"messages": [{"role": "assistant", "content": f"Error generating answer: {str(e)}"}]}


class AgenticRAGEngineFactory:
    """Agentic RAG引擎工厂类"""

    _instances = {}

    @classmethod
    async def create_engine(cls, knowledge_base: str = None) -> AgenticRAGEngine:
        """创建或获取引擎实例"""
        knowledge_base = knowledge_base or settings.default_knowledge_base

        if knowledge_base not in cls._instances:
            engine = AgenticRAGEngine(knowledge_base=knowledge_base)
            await engine.initialize()
            cls._instances[knowledge_base] = engine
            logger.info(f"Created new Agentic RAG engine for knowledge base: {knowledge_base}")

        return cls._instances[knowledge_base]

    @classmethod
    async def get_default_engine(cls) -> AgenticRAGEngine:
        """获取默认引擎"""
        return await cls.create_engine()

    @classmethod
    def clear_instances(cls):
        """清理所有实例"""
        cls._instances.clear()
        logger.info("Cleared all Agentic RAG engine instances")