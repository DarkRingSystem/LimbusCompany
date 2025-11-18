# File RAG 配置系统说明

## 📋 概述

本配置系统使用 `pydantic-settings` 实现，支持从环境变量和 `.env` 文件自动加载配置。所有配置项都有合理的默认值，可以通过环境变量灵活覆盖。

## 🗂️ 文件结构

```
backend/file_rag/core/
├── config.py              # 配置定义文件
├── config_example.py      # 配置使用示例
├── CONFIG_README.md       # 本文档
└── agentic_rag.py        # 使用配置的主要代码
```

## 🚀 快速开始

### 1. 导入配置

```python
from backend.file_rag.core.config import settings

# 访问配置
print(settings.llm_model)
print(settings.milvus_uri)
```

### 2. 使用配置字典

```python
# 获取 LLM 配置
llm_config = settings.llm_config
# 返回: {'model': 'deepseek-chat', 'api_key': '...', ...}

# 获取 Embedding 配置
embedding_config = settings.embedding_config

# 获取 Milvus 配置
milvus_config = settings.milvus_config

# 获取 RAG 配置
rag_config = settings.rag_config
```

## 📝 配置项说明

### LLM 配置

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| `llm_model` | `LLM_MODEL` | `deepseek-chat` | LLM 模型名称 |
| `llm_api_key` | `LLM_API_KEY` | (从.env读取) | LLM API 密钥 |
| `llm_api_base` | `LLM_API_BASE` | `https://api.deepseek.com/v1` | LLM API 基础 URL |
| `llm_temperature` | `LLM_TEMPERATURE` | `0.0` | LLM 温度参数 |
| `llm_max_tokens` | `LLM_MAX_TOKENS` | `4096` | 最大生成 token 数 |

### Embedding 配置

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| `embedding_model` | `EMBEDDING_MODEL` | `qwen3-embedding:0.6b` | Embedding 模型名称 |
| `embedding_base_url` | `EMBEDDING_BASE_URL` | `http://35.235.113.151:11434` | Ollama 服务地址 |
| `embedding_temperature` | `EMBEDDING_TEMPERATURE` | `0.0` | Embedding 温度参数 |
| `embedding_dimension` | `EMBEDDING_DIMENSION` | `1024` | Embedding 维度 |

### Milvus 配置

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| `milvus_uri` | `MILVUS_URI` | `http://207.246.94.177:19530` | Milvus 服务 URI |
| `milvus_index_type` | `MILVUS_INDEX_TYPE` | `FLAT` | 索引类型 |
| `milvus_metric_type` | `MILVUS_METRIC_TYPE` | `L2` | 距离度量类型 |
| `milvus_collection_name` | `MILVUS_COLLECTION_NAME` | `file_rag_collection` | 集合名称 |
| `milvus_db_name` | `MILVUS_DB_NAME` | `file_rag_db` | 数据库名称 |

### RAG 配置

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| `rag_enable_grading` | `RAG_ENABLE_GRADING` | `true` | 是否启用文档评分 |
| `rag_enable_rewrite` | `RAG_ENABLE_REWRITE` | `true` | 是否启用问题重写 |
| `rag_max_iterations` | `RAG_MAX_ITERATIONS` | `3` | 最大迭代次数 |
| `default_knowledge_base` | `DEFAULT_KNOWLEDGE_BASE` | `default` | 默认知识库名称 |
| `rag_retrieval_k` | `RAG_RETRIEVAL_K` | `5` | 检索文档数量 |
| `rag_similarity_threshold` | `RAG_SIMILARITY_THRESHOLD` | `0.7` | 相似度阈值 |

### 文档处理配置

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| `chunk_size` | `CHUNK_SIZE` | `1024` | 文本分块大小 |
| `chunk_overlap` | `CHUNK_OVERLAP` | `200` | 文本分块重叠 |
| `max_file_size_mb` | `MAX_FILE_SIZE_MB` | `100` | 最大文件大小(MB) |
| `max_batch_files` | `MAX_BATCH_FILES` | `10` | 最大批处理文件数 |
| `max_concurrent` | `MAX_CONCURRENT` | `3` | 最大并发数 |

## 🔧 配置方式

### 方式 1: 使用 .env 文件（推荐）

在项目根目录的 `.env` 文件中设置：

```bash
# LLM 配置
LLM_MODEL=deepseek-chat
LLM_API_KEY=sk-your-api-key
LLM_TEMPERATURE=0.0

# Milvus 配置
MILVUS_URI=http://localhost:19530

# RAG 配置
RAG_ENABLE_GRADING=true
RAG_MAX_ITERATIONS=5
```

### 方式 2: 环境变量

```bash
export LLM_MODEL=deepseek-chat
export LLM_TEMPERATURE=0.5
export RAG_MAX_ITERATIONS=5
```

### 方式 3: 代码中直接访问

```python
from backend.file_rag.core.config import settings

# 直接访问（只读）
print(settings.llm_model)
```

## 💡 使用示例

### 示例 1: 创建 Embedding

```python
from langchain_ollama import OllamaEmbeddings
from backend.file_rag.core.config import settings

embedding = OllamaEmbeddings(
    model=settings.embedding_model,
    base_url=settings.embedding_base_url,
    temperature=settings.embedding_temperature
)
```

### 示例 2: 创建 Milvus 向量存储

```python
from langchain_milvus import Milvus
from backend.file_rag.core.config import settings

vector_store = Milvus(
    embedding_function=embedding,
    connection_args={"uri": settings.milvus_uri},
    index_params={
        "index_type": settings.milvus_index_type,
        "metric_type": settings.milvus_metric_type
    },
    collection_name=settings.milvus_collection_name,
)
```

### 示例 3: 创建 LLM

```python
from langchain.chat_models import init_chat_model
from backend.file_rag.core.config import settings

llm = init_chat_model(
    f"deepseek:{settings.llm_model}",
    temperature=settings.llm_temperature,
    max_tokens=settings.llm_max_tokens,
    api_key=settings.llm_api_key,
    base_url=settings.llm_api_base
)
```

### 示例 4: 使用 RAG 配置

```python
from backend.file_rag.core.config import settings

def should_grade_documents():
    return settings.rag_enable_grading

def should_rewrite_question():
    return settings.rag_enable_rewrite

def get_max_iterations():
    return settings.rag_max_iterations
```

## 🎯 最佳实践

### 1. 敏感信息管理

- ✅ 将 API 密钥等敏感信息放在 `.env` 文件中
- ✅ 确保 `.env` 文件在 `.gitignore` 中
- ❌ 不要在代码中硬编码敏感信息

### 2. 环境区分

为不同环境创建不同的 `.env` 文件：

```
.env.development   # 开发环境
.env.staging       # 测试环境
.env.production    # 生产环境
```

### 3. 配置验证

配置会在启动时自动验证，如果缺少必需的配置项会报错。

### 4. 配置文档

- 所有配置项都有中文注释
- 使用 `settings.llm_config` 等属性方法获取配置字典
- 配置项使用小写 snake_case 命名（Python 规范）

## 🔍 调试技巧

### 查看当前配置

```python
from backend.file_rag.core.config import settings

# 查看所有 LLM 配置
print(settings.llm_config)

# 查看所有 RAG 配置
print(settings.rag_config)

# 查看单个配置
print(f"LLM Model: {settings.llm_model}")
print(f"Milvus URI: {settings.milvus_uri}")
```

### 检查配置来源

```python
import os

# 检查环境变量
print(os.getenv('LLM_MODEL'))
print(os.getenv('MILVUS_URI'))
```

## 📚 相关文件

- `config.py` - 配置定义
- `config_example.py` - 使用示例
- `agentic_rag.py` - 实际使用配置的代码
- `../../.env` - 环境变量配置文件

## ❓ 常见问题

### Q: 如何修改配置？
A: 在 `.env` 文件中修改对应的环境变量，或者设置系统环境变量。

### Q: 配置不生效怎么办？
A: 检查环境变量名称是否正确（不区分大小写），确保 `.env` 文件在项目根目录。

### Q: 如何添加新的配置项？
A: 在 `config.py` 的 `Settings` 类中添加新的字段，并在 `.env` 文件中添加对应的环境变量。

### Q: 配置的优先级是什么？
A: 环境变量 > .env 文件 > 代码中的默认值

## 🔄 更新日志

- 2025-11-17: 初始版本，整合 agentic_rag.py 中的所有配置项
- 支持 LLM、Embedding、Milvus、RAG 等全部配置
- 添加配置字典属性方法
- 完善文档和示例

## 📞 支持

如有问题，请查看 `config_example.py` 中的示例代码。

