"""
配置使用示例
演示如何使用 config.py 中的配置
"""

from config import settings

# ============================================
# 示例 1: 访问基本配置
# ============================================
print("=== 基本配置 ===")
print(f"LLM 模型: {settings.llm_model}")
print(f"LLM API Key: {settings.llm_api_key[:10]}...")
print(f"LLM 温度: {settings.llm_temperature}")
print(f"Milvus URI: {settings.milvus_uri}")
print(f"Embedding 模型: {settings.embedding_model}")

# ============================================
# 示例 2: 使用配置字典
# ============================================
print("\n=== 配置字典 ===")
llm_config = settings.llm_config
print(f"LLM 配置: {llm_config}")

embedding_config = settings.embedding_config
print(f"Embedding 配置: {embedding_config}")

milvus_config = settings.milvus_config
print(f"Milvus 配置: {milvus_config}")

rag_config = settings.rag_config
print(f"RAG 配置: {rag_config}")

# ============================================
# 示例 3: 在代码中使用配置
# ============================================
print("\n=== 在代码中使用配置 ===")

# 创建 Embedding 实例
from langchain_ollama import OllamaEmbeddings

embedding = OllamaEmbeddings(
    model=settings.embedding_model,
    base_url=settings.embedding_base_url,
    temperature=settings.embedding_temperature
)
print(f"创建了 Embedding 实例: {embedding}")

# 创建 Milvus 连接配置
milvus_connection_args = {
    "uri": settings.milvus_uri,
}
print(f"Milvus 连接参数: {milvus_connection_args}")

# 创建 LLM 实例
from langchain.chat_models import init_chat_model

llm = init_chat_model(
    f"deepseek:{settings.llm_model}",
    temperature=settings.llm_temperature,
    max_tokens=settings.llm_max_tokens,
    api_key=settings.llm_api_key,
    base_url=settings.llm_api_base
)
print(f"创建了 LLM 实例: {llm}")

# ============================================
# 示例 4: RAG 配置使用
# ============================================
print("\n=== RAG 配置使用 ===")

if settings.rag_enable_grading:
    print("✓ 文档相关性评分已启用")
else:
    print("✗ 文档相关性评分已禁用")

if settings.rag_enable_rewrite:
    print(f"✓ 问题重写已启用 (最大迭代次数: {settings.rag_max_iterations})")
else:
    print("✗ 问题重写已禁用")

print(f"检索文档数量: {settings.rag_retrieval_k}")
print(f"相似度阈值: {settings.rag_similarity_threshold}")

# ============================================
# 示例 5: 环境变量覆盖
# ============================================
print("\n=== 环境变量覆盖示例 ===")
print("你可以通过设置环境变量来覆盖配置:")
print("export LLM_TEMPERATURE=0.5")
print("export RAG_MAX_ITERATIONS=5")
print("export MILVUS_URI=http://localhost:19530")
print("\n或者在 .env 文件中修改:")
print("LLM_TEMPERATURE=0.5")
print("RAG_MAX_ITERATIONS=5")
print("MILVUS_URI=http://localhost:19530")

# ============================================
# 示例 6: 日志配置
# ============================================
print("\n=== 日志配置 ===")
import logging

# 使用配置中的日志级别
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("日志系统已配置")
logger.debug(f"详细日志: {settings.verbose_logging}")

# ============================================
# 示例 7: 完整的 RAG 引擎初始化示例
# ============================================
print("\n=== 完整的 RAG 引擎初始化示例 ===")

def create_rag_engine():
    """创建完整的 RAG 引擎"""
    from langchain_ollama import OllamaEmbeddings
    from langchain_milvus import Milvus
    from langchain.chat_models import init_chat_model
    
    # 1. 创建 Embedding
    embedding = OllamaEmbeddings(
        model=settings.embedding_model,
        base_url=settings.embedding_base_url,
        temperature=settings.embedding_temperature
    )
    
    # 2. 创建向量存储
    vector_store = Milvus(
        embedding_function=embedding,
        connection_args={"uri": settings.milvus_uri},
        index_params={
            "index_type": settings.milvus_index_type,
            "metric_type": settings.milvus_metric_type
        },
        collection_name=settings.milvus_collection_name,
    )
    
    # 3. 创建 LLM
    llm = init_chat_model(
        f"deepseek:{settings.llm_model}",
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
        api_key=settings.llm_api_key,
        base_url=settings.llm_api_base
    )
    
    # 4. 创建检索器
    retriever = vector_store.as_retriever(
        search_kwargs={"k": settings.rag_retrieval_k}
    )
    
    print("✓ RAG 引擎创建成功")
    return {
        "embedding": embedding,
        "vector_store": vector_store,
        "llm": llm,
        "retriever": retriever,
    }

# 注意：这只是示例，实际运行需要确保服务可用
# engine = create_rag_engine()

print("\n配置示例演示完成！")

