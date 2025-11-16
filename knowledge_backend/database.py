"""
Database management for knowledge bases and documents
"""
import logging
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
import json
import os

logger = logging.getLogger(__name__)

# Simple file-based storage for demo purposes
# In production, use a proper database like PostgreSQL
STORAGE_DIR = "data"
KB_DIR = os.path.join(STORAGE_DIR, "knowledge_bases")
DOCS_DIR = os.path.join(STORAGE_DIR, "documents")


def ensure_dirs():
    """Ensure storage directories exist"""
    os.makedirs(KB_DIR, exist_ok=True)
    os.makedirs(DOCS_DIR, exist_ok=True)


class KnowledgeBaseDB:
    """Database operations for knowledge bases"""
    
    @staticmethod
    def create(name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Create a new knowledge base"""
        ensure_dirs()
        kb_id = str(uuid.uuid4())
        kb_data = {
            "id": kb_id,
            "name": name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "document_count": 0,
        }
        
        kb_file = os.path.join(KB_DIR, f"{kb_id}.json")
        with open(kb_file, 'w', encoding='utf-8') as f:
            json.dump(kb_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Created knowledge base: {kb_id}")
        return kb_data
    
    @staticmethod
    def get(kb_id: str) -> Optional[Dict[str, Any]]:
        """Get knowledge base by ID"""
        ensure_dirs()
        kb_file = os.path.join(KB_DIR, f"{kb_id}.json")
        if os.path.exists(kb_file):
            with open(kb_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    @staticmethod
    def list_all() -> List[Dict[str, Any]]:
        """List all knowledge bases"""
        ensure_dirs()
        kbs = []
        for filename in os.listdir(KB_DIR):
            if filename.endswith('.json'):
                with open(os.path.join(KB_DIR, filename), 'r', encoding='utf-8') as f:
                    kbs.append(json.load(f))
        return kbs
    
    @staticmethod
    def update(kb_id: str, name: Optional[str] = None, description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Update knowledge base"""
        kb = KnowledgeBaseDB.get(kb_id)
        if not kb:
            return None
        
        if name:
            kb["name"] = name
        if description is not None:
            kb["description"] = description
        kb["updated_at"] = datetime.now().isoformat()
        
        kb_file = os.path.join(KB_DIR, f"{kb_id}.json")
        with open(kb_file, 'w', encoding='utf-8') as f:
            json.dump(kb, f, ensure_ascii=False, indent=2)
        
        return kb
    
    @staticmethod
    def delete(kb_id: str) -> bool:
        """Delete knowledge base"""
        kb_file = os.path.join(KB_DIR, f"{kb_id}.json")
        if os.path.exists(kb_file):
            os.remove(kb_file)
            logger.info(f"Deleted knowledge base: {kb_id}")
            return True
        return False


class DocumentDB:
    """Database operations for documents"""
    
    @staticmethod
    def create(kb_id: str, name: str, file_type: str, file_size: int) -> Dict[str, Any]:
        """Create a new document record"""
        ensure_dirs()
        doc_id = str(uuid.uuid4())
        doc_data = {
            "id": doc_id,
            "knowledge_base_id": kb_id,
            "name": name,
            "file_type": file_type,
            "file_size": file_size,
            "character_count": 0,
            "chunk_count": 0,
            "recall_count": 0,
            "status": "processing",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        
        doc_file = os.path.join(DOCS_DIR, f"{doc_id}.json")
        with open(doc_file, 'w', encoding='utf-8') as f:
            json.dump(doc_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Created document: {doc_id}")
        return doc_data
    
    @staticmethod
    def get(doc_id: str) -> Optional[Dict[str, Any]]:
        """Get document by ID"""
        ensure_dirs()
        doc_file = os.path.join(DOCS_DIR, f"{doc_id}.json")
        if os.path.exists(doc_file):
            with open(doc_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    @staticmethod
    def list_by_kb(kb_id: str) -> List[Dict[str, Any]]:
        """List documents in a knowledge base"""
        ensure_dirs()
        docs = []
        for filename in os.listdir(DOCS_DIR):
            if filename.endswith('.json'):
                with open(os.path.join(DOCS_DIR, filename), 'r', encoding='utf-8') as f:
                    doc = json.load(f)
                    if doc["knowledge_base_id"] == kb_id:
                        docs.append(doc)
        return docs
    
    @staticmethod
    def update(doc_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Update document"""
        doc = DocumentDB.get(doc_id)
        if not doc:
            return None
        
        for key, value in kwargs.items():
            if key in doc:
                doc[key] = value
        doc["updated_at"] = datetime.now().isoformat()
        
        doc_file = os.path.join(DOCS_DIR, f"{doc_id}.json")
        with open(doc_file, 'w', encoding='utf-8') as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
        
        return doc
    
    @staticmethod
    def delete(doc_id: str) -> bool:
        """Delete document"""
        doc_file = os.path.join(DOCS_DIR, f"{doc_id}.json")
        if os.path.exists(doc_file):
            os.remove(doc_file)
            logger.info(f"Deleted document: {doc_id}")
            return True
        return False

