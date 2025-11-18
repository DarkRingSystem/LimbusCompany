# 配置系统快速参考卡片

## [object Object] 分钟快速开始

### 1. 安装依赖
```bash
pip install pydantic pydantic-settings python-dotenv
```

### 2. 导入配置
```python
from backend.file_rag.core.config import settings
```

### 3. 使用配置
```python
# 访问单个配置
print(settings.llm_model)
print(settings.milvus_uri)

# 使用配置字典
llm_config = settings.llm_config
```

---

## 📋 常用配置速查

### LLM 配置
```python
settings.llm_model          # "deepseek-chat"
settings.llm_api_key        # API 密钥
settings.llm_api_base       # API 基础 URL
settings.llm_temperature    # 0.0
settings.llm_max_tokens     # 4096
```

### Embedding 配置
```python
settings.embedding_model       # "qwen3-embedding:0.6b"
settings.embedding_base_url    # Ollama 服务地址
settings.embedding_temperature # 0.0
```

### Milvus 配置
```python
settings.milvus_uri            # Milvus 服务 URI
settings.milvus_index_type     # "FLAT"
settings.milvus_metric_type    # "L2"
settings.milvus_collection_name # 集合名称
```

### RAG 配置
```python
settings.rag_enable_grading    # True/False
settings.rag_enable_rewrite    # True/False
settings.rag_max_iterations    # 3
settings.rag_retrieval_k       # 5
```

---

## 🔧 修改配置

### 方法 1: 修改 .env 文件
```bash
# 编辑项目根目录的 .env 文件
LLM_TEMPERATURE=0.5
RAG_MAX_ITERATIONS=5
```

### 方法 2: 设置环境变量
```bash
export LLM_TEMPERATURE=0.5
export RAG_MAX_ITERATIONS=5
```

---

## 📦 配置字典

### 获取完整配置
```python
llm_config = settings.llm_config
# {'model': 'deepseek-chat', 'api_key': '...', ...}

embedding_config = settings.embedding_config
# {'model': 'qwen3-embedding:0.6b', 'base_url': '...', ...}

milvus_config = settings.milvus_config
# {'uri': '...', 'index_type': 'FLAT', ...}

rag_config = settings.rag_config
# {'enable_grading': True, 'enable_rewrite': True, ...}
```

---

## 🧪 测试配置

```bash
# 运行测试
python3 backend/file_rag/core/test_config.py

# 查看示例
python3 backend/file_rag/core/config_example.py
```

---

## 📚 文档导航

| 需求 | 查看文档 |
|------|----------|
| 快速开始 | `QUICK_REFERENCE.md` (本文件) |
| 详细设置 | `SETUP_GUIDE.md` |
| 配置说明 | `CONFIG_README.md` |
| 工作总结 | `SUMMARY.md` |
| 代码示例 | `config_example.py` |

---

## ⚡ 常用代码片段

### 创建 Embedding
```python
from langchain_ollama import OllamaEmbeddings
from backend.file_rag.core.config import settings

embedding = OllamaEmbeddings(
    model=settings.embedding_model,
    base_url=settings.embedding_base_url,
    temperature=settings.embedding_temperature
)
```

### 创建 LLM
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

### 创建 Milvus 向量存储
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

### 使用 RAG 配置
```python
from backend.file_rag.core.config import settings

if settings.rag_enable_grading:
    # 执行文档评分
    pass

if settings.rag_enable_rewrite:
    # 执行问题重写
    pass

max_iterations = settings.rag_max_iterations
```

---

## 🔍 故障排除

### 问题: ModuleNotFoundError
```bash
# 解决方案
pip install pydantic-settings
```

### 问题: 配置不生效
```bash
# 检查 .env 文件位置
ls -la /Users/darkringsystem/AI/LimbusCompany/.env

# 检查环境变量
echo $LLM_MODEL
```

### 问题: 导入错误
```python
# 确保使用正确的导入路径
from backend.file_rag.core.config import settings
```

---

## 📞 获取帮助

1. **查看详细文档**: `CONFIG_README.md`
2. **查看设置指南**: `SETUP_GUIDE.md`
3. **运行测试**: `python3 test_config.py`
4. **查看示例**: `python3 config_example.py`

---

## ✅ 检查清单

- [ ] 安装了 `pydantic-settings`
- [ ] 能够导入 `settings`
- [ ] 测试通过
- [ ] 了解如何修改配置
- [ ] 知道如何使用配置字典

---

**配置系统已就绪！开始使用吧！** [object Object]
