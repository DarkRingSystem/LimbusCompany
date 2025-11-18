# File RAG 配置系统设置指南

## 📦 已完成的工作

### 1. 创建的文件

```
backend/file_rag/core/
├── config.py              # ✅ 配置定义文件（主文件）
├── config_example.py      # ✅ 配置使用示例
├── test_config.py         # ✅ 配置测试脚本
├── CONFIG_README.md       # ✅ 配置系统说明文档
└── SETUP_GUIDE.md         # ✅ 本设置指南

backend/file_rag/
└── requirements.txt       # ✅ 依赖包列表

项目根目录/.env           # ✅ 已更新环境变量配置
```

### 2. 更新的文件

- ✅ `agentic_rag.py` - 已更新为使用配置系统
- ✅ `.env` - 已添加所有必需的配置项

## 🚀 快速开始

### 步骤 1: 安装依赖

```bash
# 进入项目目录
cd /Users/darkringsystem/AI/LimbusCompany

# 安装依赖
pip install -r backend/file_rag/requirements.txt

# 或者只安装配置相关的包
pip install pydantic pydantic-settings python-dotenv
```

### 步骤 2: 验证配置

```bash
# 运行配置测试
python3 backend/file_rag/core/test_config.py
```

如果所有测试通过，你会看到：
```
🎉 所有测试通过！配置系统工作正常。
```

### 步骤 3: 使用配置

在你的代码中导入并使用配置：

```python
from backend.file_rag.core.config import settings

# 访问配置
print(settings.llm_model)
print(settings.milvus_uri)

# 使用配置字典
llm_config = settings.llm_config
embedding_config = settings.embedding_config
```

## 📋 配置系统特性

### 1. 自动从 .env 加载

配置系统会自动从项目根目录的 `.env` 文件加载环境变量：

```bash
# .env 文件示例
LLM_MODEL=deepseek-chat
LLM_API_KEY=sk-your-api-key
MILVUS_URI=http://localhost:19530
RAG_ENABLE_GRADING=true
```

### 2. 类型安全

所有配置项都有明确的类型定义，Pydantic 会自动验证：

```python
llm_temperature: float = 0.0      # 必须是浮点数
rag_max_iterations: int = 3       # 必须是整数
rag_enable_grading: bool = True   # 必须是布尔值
```

### 3. 默认值

所有配置项都有合理的默认值，即使不设置环境变量也能正常工作。

### 4. 配置字典

提供了便捷的属性方法获取配置字典：

```python
settings.llm_config        # LLM 配置字典
settings.embedding_config  # Embedding 配置字典
settings.milvus_config     # Milvus 配置字典
settings.rag_config        # RAG 配置字典
```

## 🔧 配置项说明

### 核心配置

| 类别 | 配置项数量 | 说明 |
|------|-----------|------|
| LLM | 5 | DeepSeek 模型配置 |
| Embedding | 4 | Ollama Embedding 配置 |
| Milvus | 5 | 向量数据库配置 |
| RAG | 6 | 检索增强生成配置 |
| 文档处理 | 5 | 文档分块和限制配置 |
| 视觉模型 | 3 | 图片分析模型配置 |
| 其他 | 10+ | 日志、服务等配置 |

详细配置说明请查看 `CONFIG_README.md`。

## 📝 主要改动说明

### agentic_rag.py 的改动

#### 1. 添加了导入

```python
import os
import logging
from typing import Literal

# 导入配置
from .config import settings

# 配置日志
logger = logging.getLogger(__name__)
```

#### 2. 更新了函数

**retrieve_tool()** - 使用配置创建检索工具：
```python
# 之前：硬编码
embedding = OllamaEmbeddings(
    model="qwen3-embedding:0.6b",
    base_url="http://35.235.113.151:11434",
    temperature=0
)

# 现在：使用配置
embedding = OllamaEmbeddings(
    model=settings.embedding_model,
    base_url=settings.embedding_base_url,
    temperature=settings.embedding_temperature
)
```

**get_deepseek_model()** - 使用配置创建模型：
```python
# 之前：硬编码
os.environ["DEEPSEEK_API_KEY"] = "sk-3b351274b99e41679b0c014ae1f6096a"
model = init_chat_model("deepseek:deepseek-chat", temperature=0)

# 现在：使用配置
os.environ["DEEPSEEK_API_KEY"] = settings.deepseek_api_key
model = init_chat_model(
    f"deepseek:{settings.deepseek_model_name}",
    temperature=settings.llm_temperature
)
```

#### 3. 更新了 AgenticRAGEngine 类

所有配置访问都改为小写 snake_case：
```python
# 之前
settings.DEFAULT_KNOWLEDGE_BASE
settings.LLM_MODEL
settings.RAG_ENABLE_GRADING

# 现在
settings.default_knowledge_base
settings.llm_model
settings.rag_enable_grading
```

### .env 文件的改动

添加了以下配置项：

```bash
# Embedding 配置
EMBEDDING_MODEL=qwen3-embedding:0.6b
EMBEDDING_BASE_URL=http://35.235.113.151:11434
EMBEDDING_TEMPERATURE=0.0
EMBEDDING_DIMENSION=1024

# Milvus 配置
MILVUS_URI=http://207.246.94.177:19530
MILVUS_INDEX_TYPE=FLAT
MILVUS_METRIC_TYPE=L2
MILVUS_COLLECTION_NAME=file_rag_collection
MILVUS_DB_NAME=file_rag_db

# RAG 配置
RAG_ENABLE_GRADING=true
RAG_ENABLE_REWRITE=true
RAG_MAX_ITERATIONS=3
DEFAULT_KNOWLEDGE_BASE=default
RAG_RETRIEVAL_K=5
RAG_SIMILARITY_THRESHOLD=0.7

# LLM 通用配置
LLM_MODEL=deepseek-chat
LLM_API_KEY=sk-7440f86596d341f7b02c1f9ab6aee136
LLM_API_BASE=https://api.deepseek.com/v1
LLM_TEMPERATURE=0.0
LLM_MAX_TOKENS=4096

# 文档处理配置
CHUNK_SIZE=1024
CHUNK_OVERLAP=200
MAX_FILE_SIZE_MB=100
MAX_BATCH_FILES=10
MAX_CONCURRENT=3

# 日志配置
LOG_LEVEL=INFO
VERBOSE_LOGGING=false

# 服务配置
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
FASTAPI_RELOAD=true
```

## ⚠️ 注意事项

### 1. GradeDocuments 类

在 `_grade_documents` 方法中，我临时注释掉了 `GradeDocuments` 结构化输出，因为这个类需要单独定义。如果你需要使用它，请创建类似这样的定义：

```python
from pydantic import BaseModel

class GradeDocuments(BaseModel):
    """文档评分输出"""
    binary_score: str  # "yes" 或 "no"
```

### 2. VectorServiceFactory 和 MilvusServiceFactory

这些工厂类在代码中被引用但未定义。如果需要使用，请确保它们在项目的其他地方已经实现。

### 3. 环境变量优先级

配置加载优先级：
1. 系统环境变量（最高）
2. .env 文件
3. config.py 中的默认值（最低）

## 🧪 测试

### 运行完整测试

```bash
python3 backend/file_rag/core/test_config.py
```

### 查看配置示例

```bash
python3 backend/file_rag/core/config_example.py
```

## 📚 文档

- **CONFIG_README.md** - 详细的配置系统说明
- **config_example.py** - 实际使用示例代码
- **test_config.py** - 配置测试脚本

## 🔍 故障排除

### 问题 1: ModuleNotFoundError: No module named 'pydantic_settings'

**解决方案**：
```bash
pip install pydantic-settings
```

### 问题 2: 配置不生效

**检查清单**：
1. ✅ .env 文件在项目根目录
2. ✅ 环境变量名称正确（不区分大小写）
3. ✅ 重启 Python 进程以加载新配置

### 问题 3: 导入错误

**解决方案**：
```python
# 确保使用正确的导入路径
from backend.file_rag.core.config import settings

# 或者在 backend/file_rag/core/ 目录下
from .config import settings
```

## 🎯 下一步

1. **安装依赖**：`pip install -r backend/file_rag/requirements.txt`
2. **运行测试**：`python3 backend/file_rag/core/test_config.py`
3. **查看示例**：阅读 `config_example.py`
4. **开始使用**：在你的代码中导入 `settings`

## 📞 需要帮助？

如果遇到问题：
1. 查看 `CONFIG_README.md` 了解详细配置说明
2. 运行 `test_config.py` 检查配置是否正常
3. 查看 `config_example.py` 了解使用方法

## ✅ 完成清单

- [x] 创建 config.py 配置文件
- [x] 更新 agentic_rag.py 使用配置
- [x] 更新 .env 文件添加所有配置项
- [x] 创建配置文档和示例
- [x] 创建测试脚本
- [x] 创建依赖列表
- [ ] 安装依赖包（需要你执行）
- [ ] 运行测试验证（需要你执行）

---

**配置系统已经准备就绪！** 🎉

现在你可以：
1. 安装依赖包
2. 运行测试验证
3. 在项目中使用新的配置系统

