"""
Document processing module for various file formats
"""
import logging
import os
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.parsers import LLMImageBlobParser
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader,
    UnstructuredPowerPointLoader,
    UnstructuredHTMLLoader,
    UnstructuredXMLLoader,
)
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from pathlib import Path
from langchain_openai import ChatOpenAI


logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Process documents from various file formats"""
    
    SUPPORTED_FORMATS = {
        'pdf': 'pdf',
        'txt': 'text',
        'md': 'markdown',
        'markdown': 'markdown',
        'csv': 'csv',
        'docx': 'docx',
        'doc': 'doc',
        'xlsx': 'xlsx',
        'xls': 'xls',
        'pptx': 'pptx',
        'ppt': 'ppt',
        'html': 'html',
        'htm': 'html',
        'xml': 'xml',
    }
    
    @staticmethod
    def load_document(file_path: str) -> List[Document]:
        """Load document based on file type"""
        file_ext = Path(file_path).suffix.lower().lstrip('.')
        
        if file_ext not in DocumentProcessor.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        try:
            if file_ext == 'pdf':
                _PROMPT_IMAGES_TO_DESCRIPTION: str = (
        "您是一名负责为图像检索任务生成摘要的助手。"
        "1. 这些摘要将被嵌入并用于检索原始图像。"
        "请提供简洁的图像摘要，确保其高度优化以利于检索\n"
        "2. 提取图像中的所有文本内容。"
        "不得遗漏页面上的任何信息。\n"
        "3. 不要凭空捏造不存在的信息\n"
        "请使用Markdown格式直接输出答案，"
        "无需解释性文字，且开头不要使用Markdown分隔符```。"
    )
                llm_parser = LLMImageBlobParser(
                    model=ChatOpenAI(
                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                    api_key="sk-abd31c85f3fa41928b16dda0cb54e2df",
                    model="qwen3-vl-plus",
                    max_tokens=8192
                ),
                prompt=_PROMPT_IMAGES_TO_DESCRIPTION
            )

                # Use PyMuPDF4LLMLoader for better PDF processing
                loader = PyMuPDF4LLMLoader(
                    file_path,
                    mode="single",  # Process as single document
                    extract_images=True,
                    table_strategy="lines",  # Extract tables
                    images_parser=llm_parser
                )
                documents = loader.load()
            elif file_ext in ['txt', 'md', 'markdown']:
                loader = TextLoader(file_path, encoding='utf-8')
                documents = loader.load()
            elif file_ext == 'csv':
                loader = CSVLoader(file_path, encoding='utf-8')
                documents = loader.load()
            elif file_ext in ['doc', 'docx']:
                loader = Docx2txtLoader(file_path)
                documents = loader.load()
            elif file_ext in ['xls', 'xlsx']:
                loader = UnstructuredExcelLoader(file_path, mode="elements")
                documents = loader.load()
            elif file_ext in ['ppt', 'pptx']:
                loader = UnstructuredPowerPointLoader(file_path, mode="elements")
                documents = loader.load()
            elif file_ext in ['htm', 'html']:
                loader = UnstructuredHTMLLoader(file_path, mode="elements")
                documents = loader.load()
            elif file_ext == 'xml':
                loader = UnstructuredXMLLoader(file_path, mode="elements")
                documents = loader.load()
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")

            logger.info(f"Loaded {len(documents)} documents from {file_path}")
            return documents
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def split_documents(
        documents: List[Document],
        chunk_size: int = 1024,
        chunk_overlap: int = 200
    ) -> List[Document]:
        """Split documents into chunks using tiktoken encoder"""
        try:
            # Use from_tiktoken_encoder for better token-based splitting
            splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )

            split_docs = splitter.split_documents(documents)
            logger.info(f"Split documents into {len(split_docs)} chunks")
            return split_docs
        except Exception as e:
            logger.error(f"Error splitting documents: {str(e)}")
            raise
    
    @staticmethod
    def process_file(
        file_path: str,
        chunk_size: int = 1024,
        chunk_overlap: int = 200
    ) -> Tuple[List[Document], int]:
        """Process a file: load and split into chunks"""
        try:
            # Load document
            documents = DocumentProcessor.load_document(file_path)
            
            # Calculate character count
            total_chars = sum(len(doc.page_content) for doc in documents)
            
            # Split into chunks
            chunks = DocumentProcessor.split_documents(
                documents,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            
            logger.info(f"Processed file {file_path}: {total_chars} chars, {len(chunks)} chunks")
            return chunks, total_chars
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            raise


# Global document processor instance
document_processor = DocumentProcessor()

