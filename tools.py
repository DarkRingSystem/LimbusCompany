import asyncio
import base64
from typing import Optional, Dict, Any

from langchain_mcp_adapters.client import MultiServerMCPClient
import dotenv
from service.markdown_converter_service import MarkdownConverterService

zhipu_api_key = dotenv.get_key(".env", "ZHIPU_API_KEY")

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"{city}，今天是晴天，温度为 25 摄氏度。!"

def get_zhipu_search_mcp_tools():
    client = MultiServerMCPClient(
        {
            "search": {
                "url": "https://open.bigmodel.cn/api/mcp/web_search/sse?Authorization="+zhipu_api_key,
                "transport": "sse",
            }
        }
    )
    tools = asyncio.run(client.get_tools())
    return tools


def convert_document(
    file_path: Optional[str] = None,
    file_bytes: Optional[bytes] = None,
    filename: Optional[str] = None,
) -> Dict[str, Any]:
    """
    将文档转换为 Markdown 格式

    支持的文件格式:
    - PDF (.pdf)
    - Word (.docx, .doc)
    - Excel (.xlsx, .xls)
    - PowerPoint (.pptx, .ppt)
    - 图片 (.png, .jpg, .jpeg, .gif, .bmp, .tiff)
    - HTML (.html, .htm)
    - EPUB (.epub)

    参数:
        file_path: 本地文件路径 (可选)
        file_bytes: 文件字节流 (可选，用于上传的文件)
        filename: 文件名 (当使用 file_bytes 时需要提供)

    返回:
        包含以下字段的字典:
        - success: 是否转换成功
        - markdown: 转换后的 Markdown 内容
        - images: 提取的图片列表 (base64 编码)
        - metadata: 文件元数据
        - error: 错误信息 (如果失败)

    示例:
        # 从本地文件转换
        result = convert_document(file_path="/path/to/document.pdf")

        # 从上传的文件字节转换
        result = convert_document(
            file_bytes=file_content,
            filename="document.pdf"
        )
    """
    try:
        service = MarkdownConverterService()

        if file_path:
            # 从本地文件转换
            result = asyncio.run(service.convert_file(file_path))
        elif file_bytes and filename:
            # 从字节流转换
            result = asyncio.run(service.convert_file_bytes(file_bytes, filename))
        else:
            return {
                "success": False,
                "error": "必须提供 file_path 或 (file_bytes + filename)"
            }

        if result.get("success"):
            # 格式化响应
            response = {
                "success": True,
                "markdown": result.get("markdown", ""),
                "metadata": {
                    "filename": result.get("filename", filename or "unknown"),
                    "file_size": result.get("file_size", 0),
                    "pages": result.get("pages", 0),
                    "conversion_time": result.get("conversion_time", 0),
                }
            }

            # 处理提取的图片
            if result.get("images"):
                response["images"] = [
                    {
                        "data": base64.b64encode(img.get("data", b"")).decode("utf-8"),
                        "format": img.get("format", "png"),
                        "page": img.get("page", 0),
                    }
                    for img in result.get("images", [])
                ]

            return response
        else:
            return {
                "success": False,
                "error": result.get("error", "转换失败")
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"文档转换错误: {str(e)}"
        }

