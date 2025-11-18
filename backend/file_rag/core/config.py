"""
Configuration module for File RAG System
配置模块 - 文件检索增强生成系统
"""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

    # ============================================
    # LLM 配置 (DeepSeek)
    # ============================================
    # DeepSeek API 密钥
    deepseek_api_key: str = "sk-7440f86596d341f7b02c1f9ab6aee136"
    # DeepSeek 模型名称
    deepseek_model_name: str = "deepseek-chat"
    # DeepSeek API 基础 URL
    deepseek_base_url: str = "https://api.deepseek.com/v1"

    # LLM 通用配置（用于 RAG 引擎）
    llm_model: str = "deepseek-chat"
    llm_api_key: str = "sk-7440f86596d341f7b02c1f9ab6aee136"
    llm_api_base: str = "https://api.deepseek.com/v1"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 4096

    # ============================================
    # Embedding 配置 (Ollama)
    # ============================================
    # Ollama Embedding 模型名称
    embedding_model: str = "qwen3-embedding:0.6b"
    # Ollama 服务地址
    embedding_base_url: str = "http://35.235.113.151:11434"
    # Embedding 温度参数
    embedding_temperature: float = 0.0
    # Embedding 维度（根据模型而定）
    embedding_dimension: int = 1024

    # ============================================
    # Milvus 向量数据库配置
    # ============================================
    # Milvus 服务 URI
    milvus_uri: str = "http://127.0.0.1:19530"
    # Milvus 索引类型 (FLAT, IVF_FLAT, IVF_SQ8, IVF_PQ, HNSW, ANNOY)
    milvus_index_type: str = "FLAT"
    # Milvus 距离度量类型 (L2, IP, COSINE)
    milvus_metric_type: str = "L2"
    # Milvus 默认集合名称
    milvus_collection_name: str = "file_rag_collection"
    # Milvus 数据库名称
    milvus_db_name: str = "file_rag_db"

    # ============================================
    # RAG 配置
    # ============================================
    # 是否启用文档相关性评分
    rag_enable_grading: bool = True
    # 是否启用问题重写
    rag_enable_rewrite: bool = True
    # 最大迭代次数（问题重写的最大次数）
    rag_max_iterations: int = 3
    # 默认知识库名称
    default_knowledge_base: str = "default"
    # 检索文档数量
    rag_retrieval_k: int = 5
    # 相似度阈值（0-1之间）
    rag_similarity_threshold: float = 0.7

    # ============================================
    # 文档处理配置
    # ============================================
    # 文本分块大小
    chunk_size: int = 1024
    # 文本分块重叠大小
    chunk_overlap: int = 200
    # 最大文件大小（MB）
    max_file_size_mb: int = 100
    # 最大批处理文件数
    max_batch_files: int = 10
    # 最大并发数
    max_concurrent: int = 3

    # ============================================
    # 视觉模型配置（用于文档图片分析）
    # ============================================
    # 视觉模型名称
    vision_model: str = "qwen-vl-max-latest"
    # 视觉模型 API 密钥
    vision_api_key: str = "sk-65417eb6629a4102858a35f3484878e5"
    # 视觉模型 API 基础 URL
    vision_base_url: str = ""

    # ============================================
    # 豆包视觉模型配置
    # ============================================
    # 豆包 API 密钥
    doubao_api_key: str = "0e58effd-fe97-4809-91ee-a631585d0ac2"

    # ============================================
    # UI-TARS 模型配置（用于 UI 分析）
    # ============================================
    # UI-TARS 模型名称
    uitars_model: str = "doubao-1-5-ui-tars-250428"
    # UI-TARS API 密钥
    uitars_api_key: str = "0e58effd-fe97-4809-91ee-a631585d0ac2"
    # UI-TARS API 基础 URL
    uitars_base_url: str = "https://ark.cn-beijing.volces.com/api/v3"

    # ============================================
    # Markdown 转换配置
    # ============================================
    # 是否使用 LLM 提升转换精度
    markdown_use_llm: bool = True
    # 是否强制 OCR
    markdown_force_ocr: bool = False
    # 是否禁用图片提取
    markdown_disable_image_extraction: bool = False
    # 输出格式
    markdown_output_format: str = "markdown"
    # 最大文件大小（MB）
    markdown_max_file_size_mb: int = 100
    # 最大批处理文件数
    markdown_max_batch_files: int = 10
    # 最大并发数
    markdown_max_concurrent: int = 3

    # ============================================
    # Markdown LLM 配置
    # ============================================
    # LLM 服务类路径
    markdown_llm_service: str = "marker.services.openai.OpenAIService"
    # LLM API 密钥
    markdown_llm_api_key: str = "sk-65417eb6629a4102858a35f3484878e5"
    # LLM API 基础 URL
    markdown_llm_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    # LLM 模型名称
    markdown_llm_model: str = "qwen-vl-max-latest"

    # ============================================
    # 搜索工具配置
    # ============================================
    # 智谱 API 密钥
    zhipu_api_key: str = "f5651b653cc94ec6a11d339f59fc8b8e.T6kpVxF5jHmmdMV5"
    # Tavily API 密钥
    tavily_api_key: str = "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"

    # ============================================
    # 日志配置
    # ============================================
    # 日志级别
    log_level: str = "INFO"
    # 是否启用详细日志
    verbose_logging: bool = False

    # ============================================
    # 服务配置
    # ============================================
    # FastAPI 服务地址
    fastapi_host: str = "0.0.0.0"
    # FastAPI 服务端口
    fastapi_port: int = 8000
    # 是否启用热重载
    fastapi_reload: bool = True

    # ============================================
    # 属性方法
    # ============================================
    @property
    def llm_config(self) -> dict:
        """获取 LLM 配置字典"""
        return {
            "model": self.llm_model,
            "api_key": self.llm_api_key,
            "base_url": self.llm_api_base,
            "temperature": self.llm_temperature,
            "max_tokens": self.llm_max_tokens,
        }

    @property
    def embedding_config(self) -> dict:
        """获取 Embedding 配置字典"""
        return {
            "model": self.embedding_model,
            "base_url": self.embedding_base_url,
            "temperature": self.embedding_temperature,
        }

    @property
    def milvus_config(self) -> dict:
        """获取 Milvus 配置字典"""
        return {
            "uri": self.milvus_uri,
            "index_type": self.milvus_index_type,
            "metric_type": self.milvus_metric_type,
            "collection_name": self.milvus_collection_name,
            "db_name": self.milvus_db_name,
        }

    @property
    def rag_config(self) -> dict:
        """获取 RAG 配置字典"""
        return {
            "enable_grading": self.rag_enable_grading,
            "enable_rewrite": self.rag_enable_rewrite,
            "max_iterations": self.rag_max_iterations,
            "retrieval_k": self.rag_retrieval_k,
            "similarity_threshold": self.rag_similarity_threshold,
        }


# 创建全局配置实例
settings = Settings()

