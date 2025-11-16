"""
Data models for Knowledge Base Management System
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class KnowledgeBaseCreate(BaseModel):
    """Model for creating a knowledge base"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)


class KnowledgeBaseUpdate(BaseModel):
    """Model for updating a knowledge base"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)


class KnowledgeBaseResponse(BaseModel):
    """Model for knowledge base response"""
    id: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    document_count: int = 0


class DocumentCreate(BaseModel):
    """Model for creating a document"""
    name: str = Field(..., min_length=1, max_length=255)
    file_type: str
    file_size: int
    chunk_size: int = 1024
    chunk_overlap: int = 200


class DocumentUpdate(BaseModel):
    """Model for updating a document"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)


class DocumentResponse(BaseModel):
    """Model for document response"""
    id: str
    knowledge_base_id: str
    name: str
    file_type: str
    file_size: int
    character_count: int
    chunk_count: int
    recall_count: int = 0
    status: str  # processing, completed, failed
    created_at: datetime
    updated_at: datetime


class ChunkResponse(BaseModel):
    """Model for chunk response"""
    id: str
    document_id: str
    content: str
    chunk_index: int


class RetrievalRequest(BaseModel):
    """Model for retrieval request"""
    query: str = Field(..., min_length=1)
    knowledge_base_id: str
    top_k: int = Field(default=5, ge=1, le=100)
    retrieval_type: str = Field(default="vector", pattern="^(vector|hybrid)$")


class RetrievalResult(BaseModel):
    """Model for retrieval result"""
    chunk_id: str
    document_id: str
    document_name: str
    content: str
    similarity_score: float
    chunk_index: int


class RetrievalResponse(BaseModel):
    """Model for retrieval response"""
    query: str
    results: List[RetrievalResult]
    total_count: int

