"""
Knowledge Base API routes
"""
import logging
from fastapi import APIRouter, HTTPException
from typing import List
from models import KnowledgeBaseCreate, KnowledgeBaseUpdate, KnowledgeBaseResponse
from database import KnowledgeBaseDB, DocumentDB
from vector_store import vector_store_manager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_model=KnowledgeBaseResponse)
async def create_knowledge_base(kb_create: KnowledgeBaseCreate):
    """Create a new knowledge base"""
    try:
        # Create in database
        kb_data = KnowledgeBaseDB.create(kb_create.name, kb_create.description)

        # Create Milvus collection (replace hyphens with underscores for Milvus compatibility)
        collection_name = f"kb_{kb_data['id'].replace('-', '_')}"
        vector_store_manager.create_collection(collection_name)
        
        return KnowledgeBaseResponse(**kb_data)
    except Exception as e:
        logger.error(f"Error creating knowledge base: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{kb_id}", response_model=KnowledgeBaseResponse)
async def get_knowledge_base(kb_id: str):
    """Get knowledge base by ID"""
    try:
        kb = KnowledgeBaseDB.get(kb_id)
        if not kb:
            raise HTTPException(status_code=404, detail="Knowledge base not found")

        # Add document count
        doc_count = len(DocumentDB.list_by_kb(kb_id))
        kb_with_count = {**kb, 'document_count': doc_count}

        return KnowledgeBaseResponse(**kb_with_count)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting knowledge base: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[KnowledgeBaseResponse])
async def list_knowledge_bases():
    """List all knowledge bases"""
    try:
        kbs = KnowledgeBaseDB.list_all()
        response_kbs = []
        for kb in kbs:
            doc_count = len(DocumentDB.list_by_kb(kb['id']))
            kb_with_count = {**kb, 'document_count': doc_count}
            response_kbs.append(KnowledgeBaseResponse(**kb_with_count))
        return response_kbs
    except Exception as e:
        logger.error(f"Error listing knowledge bases: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{kb_id}", response_model=KnowledgeBaseResponse)
async def update_knowledge_base(kb_id: str, kb_update: KnowledgeBaseUpdate):
    """Update knowledge base"""
    try:
        kb = KnowledgeBaseDB.update(
            kb_id,
            name=kb_update.name,
            description=kb_update.description
        )
        if not kb:
            raise HTTPException(status_code=404, detail="Knowledge base not found")
        return KnowledgeBaseResponse(**kb)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating knowledge base: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{kb_id}")
async def delete_knowledge_base(kb_id: str):
    """Delete knowledge base"""
    try:
        # Delete from database
        if not KnowledgeBaseDB.delete(kb_id):
            raise HTTPException(status_code=404, detail="Knowledge base not found")

        # Delete Milvus collection (replace hyphens with underscores for Milvus compatibility)
        collection_name = f"kb_{kb_id.replace('-', '_')}"
        try:
            vector_store_manager.delete_collection(collection_name)
        except Exception as e:
            logger.warning(f"Error deleting collection {collection_name}: {str(e)}")
        
        return {"message": "Knowledge base deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting knowledge base: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

