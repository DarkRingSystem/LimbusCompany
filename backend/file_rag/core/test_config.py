"""
配置测试脚本
用于验证配置系统是否正常工作
"""

import sys
from pathlib import Path

# 确保可以导入 config 模块
sys.path.insert(0, str(Path(__file__).parent))

def test_config_import():
    """测试配置导入"""
    print("=" * 60)
    print("测试 1: 配置导入")
    print("=" * 60)
    try:
        from config import settings
        print("✓ 配置导入成功")
        return True
    except Exception as e:
        print(f"✗ 配置导入失败: {e}")
        return False


def test_basic_config():
    """测试基本配置"""
    print("\n" + "=" * 60)
    print("测试 2: 基本配置访问")
    print("=" * 60)
    try:
        from config import settings
        
        # 测试 LLM 配置
        assert settings.llm_model is not None, "llm_model 不能为空"
        assert settings.llm_api_key is not None, "llm_api_key 不能为空"
        assert settings.llm_temperature >= 0, "llm_temperature 必须 >= 0"
        print(f"✓ LLM 模型: {settings.llm_model}")
        print(f"✓ LLM API Key: {settings.llm_api_key[:10]}...")
        print(f"✓ LLM 温度: {settings.llm_temperature}")
        
        # 测试 Embedding 配置
        assert settings.embedding_model is not None, "embedding_model 不能为空"
        assert settings.embedding_base_url is not None, "embedding_base_url 不能为空"
        print(f"✓ Embedding 模型: {settings.embedding_model}")
        print(f"✓ Embedding URL: {settings.embedding_base_url}")
        
        # 测试 Milvus 配置
        assert settings.milvus_uri is not None, "milvus_uri 不能为空"
        print(f"✓ Milvus URI: {settings.milvus_uri}")
        
        # 测试 RAG 配置
        assert isinstance(settings.rag_enable_grading, bool), "rag_enable_grading 必须是布尔值"
        assert isinstance(settings.rag_enable_rewrite, bool), "rag_enable_rewrite 必须是布尔值"
        assert settings.rag_max_iterations > 0, "rag_max_iterations 必须 > 0"
        print(f"✓ RAG 评分启用: {settings.rag_enable_grading}")
        print(f"✓ RAG 重写启用: {settings.rag_enable_rewrite}")
        print(f"✓ RAG 最大迭代: {settings.rag_max_iterations}")
        
        print("\n✓ 所有基本配置测试通过")
        return True
    except AssertionError as e:
        print(f"✗ 配置验证失败: {e}")
        return False
    except Exception as e:
        print(f"✗ 配置访问失败: {e}")
        return False


def test_config_properties():
    """测试配置属性方法"""
    print("\n" + "=" * 60)
    print("测试 3: 配置属性方法")
    print("=" * 60)
    try:
        from config import settings
        
        # 测试 llm_config
        llm_config = settings.llm_config
        assert isinstance(llm_config, dict), "llm_config 必须是字典"
        assert "model" in llm_config, "llm_config 必须包含 model"
        assert "api_key" in llm_config, "llm_config 必须包含 api_key"
        print(f"✓ LLM 配置字典: {list(llm_config.keys())}")
        
        # 测试 embedding_config
        embedding_config = settings.embedding_config
        assert isinstance(embedding_config, dict), "embedding_config 必须是字典"
        assert "model" in embedding_config, "embedding_config 必须包含 model"
        print(f"✓ Embedding 配置字典: {list(embedding_config.keys())}")
        
        # 测试 milvus_config
        milvus_config = settings.milvus_config
        assert isinstance(milvus_config, dict), "milvus_config 必须是字典"
        assert "uri" in milvus_config, "milvus_config 必须包含 uri"
        print(f"✓ Milvus 配置字典: {list(milvus_config.keys())}")
        
        # 测试 rag_config
        rag_config = settings.rag_config
        assert isinstance(rag_config, dict), "rag_config 必须是字典"
        assert "enable_grading" in rag_config, "rag_config 必须包含 enable_grading"
        print(f"✓ RAG 配置字典: {list(rag_config.keys())}")
        
        print("\n✓ 所有配置属性方法测试通过")
        return True
    except AssertionError as e:
        print(f"✗ 配置属性验证失败: {e}")
        return False
    except Exception as e:
        print(f"✗ 配置属性访问失败: {e}")
        return False


def test_env_file_loading():
    """测试 .env 文件加载"""
    print("\n" + "=" * 60)
    print("测试 4: .env 文件加载")
    print("=" * 60)
    try:
        from config import settings
        import os
        
        # 检查项目根目录的 .env 文件
        project_root = Path(__file__).parent.parent.parent.parent
        env_file = project_root / ".env"
        
        if env_file.exists():
            print(f"✓ 找到 .env 文件: {env_file}")
            
            # 检查一些关键环境变量是否被加载
            if settings.deepseek_api_key:
                print(f"✓ DEEPSEEK_API_KEY 已加载")
            if settings.llm_api_key:
                print(f"✓ LLM_API_KEY 已加载")
            if settings.milvus_uri:
                print(f"✓ MILVUS_URI 已加载")
                
            print("\n✓ .env 文件加载测试通过")
            return True
        else:
            print(f"⚠ 未找到 .env 文件: {env_file}")
            print("  使用默认配置值")
            return True
    except Exception as e:
        print(f"✗ .env 文件加载测试失败: {e}")
        return False


def test_config_types():
    """测试配置类型"""
    print("\n" + "=" * 60)
    print("测试 5: 配置类型验证")
    print("=" * 60)
    try:
        from config import settings
        
        # 字符串类型
        assert isinstance(settings.llm_model, str), "llm_model 必须是字符串"
        assert isinstance(settings.milvus_uri, str), "milvus_uri 必须是字符串"
        print("✓ 字符串类型配置正确")
        
        # 数字类型
        assert isinstance(settings.llm_temperature, (int, float)), "llm_temperature 必须是数字"
        assert isinstance(settings.llm_max_tokens, int), "llm_max_tokens 必须是整数"
        assert isinstance(settings.rag_max_iterations, int), "rag_max_iterations 必须是整数"
        print("✓ 数字类型配置正确")
        
        # 布尔类型
        assert isinstance(settings.rag_enable_grading, bool), "rag_enable_grading 必须是布尔值"
        assert isinstance(settings.rag_enable_rewrite, bool), "rag_enable_rewrite 必须是布尔值"
        assert isinstance(settings.verbose_logging, bool), "verbose_logging 必须是布尔值"
        print("✓ 布尔类型配置正确")
        
        print("\n✓ 所有配置类型验证通过")
        return True
    except AssertionError as e:
        print(f"✗ 配置类型验证失败: {e}")
        return False
    except Exception as e:
        print(f"✗ 配置类型测试失败: {e}")
        return False


def test_config_values():
    """测试配置值的合理性"""
    print("\n" + "=" * 60)
    print("测试 6: 配置值合理性验证")
    print("=" * 60)
    try:
        from config import settings
        
        # 温度值应该在合理范围内
        assert 0 <= settings.llm_temperature <= 2, "llm_temperature 应该在 0-2 之间"
        assert 0 <= settings.embedding_temperature <= 2, "embedding_temperature 应该在 0-2 之间"
        print("✓ 温度值在合理范围内")
        
        # Token 数应该是正数
        assert settings.llm_max_tokens > 0, "llm_max_tokens 必须 > 0"
        print("✓ Token 数配置合理")
        
        # 迭代次数应该是正数
        assert settings.rag_max_iterations > 0, "rag_max_iterations 必须 > 0"
        assert settings.rag_retrieval_k > 0, "rag_retrieval_k 必须 > 0"
        print("✓ 迭代次数配置合理")
        
        # 相似度阈值应该在 0-1 之间
        assert 0 <= settings.rag_similarity_threshold <= 1, "rag_similarity_threshold 应该在 0-1 之间"
        print("✓ 相似度阈值配置合理")
        
        # 文件大小限制应该是正数
        assert settings.max_file_size_mb > 0, "max_file_size_mb 必须 > 0"
        assert settings.max_batch_files > 0, "max_batch_files 必须 > 0"
        assert settings.max_concurrent > 0, "max_concurrent 必须 > 0"
        print("✓ 文件处理配置合理")
        
        print("\n✓ 所有配置值合理性验证通过")
        return True
    except AssertionError as e:
        print(f"✗ 配置值验证失败: {e}")
        return False
    except Exception as e:
        print(f"✗ 配置值测试失败: {e}")
        return False


def print_summary(results):
    """打印测试摘要"""
    print("\n" + "=" * 60)
    print("测试摘要")
    print("=" * 60)
    
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    print(f"总测试数: {total}")
    print(f"通过: {passed} ✓")
    print(f"失败: {failed} ✗")
    print(f"通过率: {passed/total*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 所有测试通过！配置系统工作正常。")
    else:
        print(f"\n⚠️  有 {failed} 个测试失败，请检查配置。")
    
    print("=" * 60)


def main():
    """运行所有测试"""
    print("\n🚀 开始配置系统测试...\n")
    
    results = []
    
    # 运行所有测试
    results.append(test_config_import())
    results.append(test_basic_config())
    results.append(test_config_properties())
    results.append(test_env_file_loading())
    results.append(test_config_types())
    results.append(test_config_values())
    
    # 打印摘要
    print_summary(results)
    
    # 返回退出码
    return 0 if all(results) else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

