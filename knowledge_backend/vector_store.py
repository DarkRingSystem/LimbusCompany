"""
Vector store management using Milvus and LangChain
"""
import logging
from typing import List, Optional
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from config import settings

logger = logging.getLogger(__name__)


class VectorStoreManager:
    """Manager for vector store operations"""
    
    def __init__(self):
        """Initialize vector store manager"""
        # Use Ollama embeddings for local models
        if settings.embedding_model_provider.lower() == "qwen":
            self.embeddings = OllamaEmbeddings(
                model=settings.embedding_model_name,
                base_url=settings.openai_api_base
            )
        else:
            # Fallback to OpenAI embeddings for other providers
            self.embeddings = OpenAIEmbeddings(
                model=settings.embedding_model_name,
                api_key=settings.openai_api_key,
                base_url=settings.openai_api_base
            )
        # Use URI format for Milvus connection
        self.milvus_connection_args = {
            "uri": f"http://{settings.milvus_host}:{settings.milvus_port}",
        }
    
    def create_collection(self, collection_name: str) -> Milvus:
        """Create a new Milvus collection for a knowledge base"""
        try:
            vector_store = Milvus(
                embedding_function=self.embeddings,
                collection_name=collection_name,
                connection_args=self.milvus_connection_args,
                drop_old=False,
            )
            logger.info(f"Created collection: {collection_name}")
            return vector_store
        except Exception as e:
            logger.error(f"Error creating collection {collection_name}: {str(e)}")
            raise
    
    def add_documents(
        self,
        collection_name: str,
        documents: List[Document],
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """Add documents to a collection"""
        try:
            vector_store = Milvus(
                embedding_function=self.embeddings,
                collection_name=collection_name,
                connection_args=self.milvus_connection_args,
            )
            
            # Add documents with IDs
            if ids:
                result_ids = vector_store.add_documents(documents, ids=ids)
            else:
                result_ids = vector_store.add_documents(documents)
            
            logger.info(f"Added {len(result_ids)} documents to {collection_name}")
            return result_ids
        except Exception as e:
            logger.error(f"Error adding documents to {collection_name}: {str(e)}")
            raise
    
    def search(
        self,
        collection_name: str,
        query: str,
        top_k: int = 5
    ) -> List[tuple]:
        """Search for similar documents"""
        try:
            vector_store = Milvus(
                embedding_function=self.embeddings,
                collection_name=collection_name,
                connection_args=self.milvus_connection_args,
            )
            
            results = vector_store.similarity_search_with_score(query, k=top_k)
            logger.info(f"Search completed for query in {collection_name}")
            return results
        except Exception as e:
            logger.error(f"Error searching in {collection_name}: {str(e)}")
            raise
    
    def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection"""
        try:
            from pymilvus import connections
            connections.connect(
                host=settings.milvus_host,
                port=settings.milvus_port
            )
            from pymilvus import utility
            utility.drop_collection(collection_name)
            logger.info(f"Deleted collection: {collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting collection {collection_name}: {str(e)}")
            raise


# Global vector store manager instance
vector_store_manager = VectorStoreManager()

