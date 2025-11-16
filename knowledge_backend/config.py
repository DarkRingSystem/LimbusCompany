"""
Configuration module for Knowledge Base Management System
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

    # FastAPI Server Configuration
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    fastapi_reload: bool = True

    # Milvus Vector Database Configuration
    milvus_host: str = "localhost"
    milvus_port: int = 19530
    milvus_db_name: str = "knowledge_base"

    # Embedding Model Configuration
    embedding_model_provider: str = "qwen"
    embedding_model_name: str = "text-embedding-3-small"
    embedding_model_dimension: int = 1024

    # OpenAI Configuration
    openai_api_key: str = ""
    openai_api_base: str = "https://api.openai.com/v1"

    # Rerank Model Configuration (Reserved for future use)
    rerank_model_provider: Optional[str] = None
    rerank_model_name: Optional[str] = None
    rerank_model_api_key: Optional[str] = None

    # File Upload Configuration
    max_file_size_mb: int = 15
    max_files_per_batch: int = 5
    allowed_file_types: str = "pptx,xls,csv,xml,docx,pdf,doc,markdown,xlsx,html,ppt,htm,txt,md"

    # Document Processing Configuration
    default_chunk_size: int = 1024
    default_chunk_overlap: int = 200

    # Logging Configuration
    kb_log_level: str = "INFO"

    @property
    def allowed_file_types_list(self) -> list:
        """Convert comma-separated string to list"""
        return [ft.strip() for ft in self.allowed_file_types.split(",")]


# Create global settings instance
settings = Settings()

