"""
Retrieval API routes
"""
import logging
from fastapi import APIRouter, HTTPException
from models import RetrievalRequest, RetrievalResponse, RetrievalResult
from database import KnowledgeBaseDB, DocumentDB
from vector_store import vector_store_manager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/search", response_model=RetrievalResponse)
async def search_knowledge_base(request: RetrievalRequest):
    """Search in a knowledge base"""
    try:
        # Validate knowledge base exists
        kb = KnowledgeBaseDB.get(request.knowledge_base_id)
        if not kb:
            raise HTTPException(status_code=404, detail="Knowledge base not found")

        # Search in vector store (replace hyphens with underscores for Milvus compatibility)
        collection_name = f"kb_{request.knowledge_base_id.replace('-', '_')}"
        results = vector_store_manager.search(
            collection_name,
            request.query,
            top_k=request.top_k
        )

        # Sort results by similarity score (ascending for L2 distance, lower is better)
        sorted_results = sorted(results, key=lambda x: x[1])

        # Format results
        retrieval_results = []
        for doc, score in sorted_results:
            # Get document ID from metadata (added during document processing)
            doc_id = doc.metadata.get("document_id", "")
            chunk_id = doc.metadata.get("id", "")

            # Get document info
            doc_info = DocumentDB.get(doc_id) if doc_id else None
            
            retrieval_results.append(RetrievalResult(
                chunk_id=chunk_id,
                document_id=doc_id,
                document_name=doc_info["name"] if doc_info else "Unknown",
                content=doc.page_content,
                similarity_score=float(score),
                chunk_index=int(chunk_id.rsplit('_', 1)[1]) if '_' in chunk_id else 0
            ))
            
            # Update recall count
            if doc_info:
                current_count = doc_info.get("recall_count", 0)
                DocumentDB.update(doc_id, recall_count=current_count + 1)
        
        return RetrievalResponse(
            query=request.query,
            results=retrieval_results,
            total_count=len(retrieval_results)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching knowledge base: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/preview-chunks")
async def preview_chunks(
    kb_id: str,
    doc_id: str,
    chunk_size: int = 1024,
    chunk_overlap: int = 200
):
    """Preview document chunks with given settings"""
    try:
        # Validate knowledge base and document exist
        kb = KnowledgeBaseDB.get(kb_id)
        if not kb:
            raise HTTPException(status_code=404, detail="Knowledge base not found")
        
        doc = DocumentDB.get(doc_id)
        if not doc or doc["knowledge_base_id"] != kb_id:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # For preview, we would need to re-process the document
        # This is a placeholder - in production, you'd store the original file
        return {
            "message": "Preview functionality requires storing original files",
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "estimated_chunks": max(1, doc["character_count"] // chunk_size)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error previewing chunks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

