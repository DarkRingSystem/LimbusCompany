"""
Document API routes
"""
import logging
import gc
import os
import uuid
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
from models import DocumentResponse
from database import DocumentDB, KnowledgeBaseDB
from document_processor import document_processor
from vector_store import vector_store_manager
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/{kb_id}/upload")
async def upload_documents(
    kb_id: str,
    files: List[UploadFile] = File(...),
    chunk_size: int = Form(default=1024),
    chunk_overlap: int = Form(default=200)
):
    """Upload documents to a knowledge base"""
    try:
        # Validate knowledge base exists
        kb = KnowledgeBaseDB.get(kb_id)
        if not kb:
            raise HTTPException(status_code=404, detail="Knowledge base not found")

        # Validate file count
        if len(files) > settings.max_files_per_batch:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum {settings.max_files_per_batch} files allowed per batch"
            )

        uploaded_docs = []

        for file in files:
            # Validate file type
            file_ext = os.path.splitext(file.filename)[1].lstrip('.').lower()
            if file_ext not in settings.allowed_file_types_list:
                raise HTTPException(
                    status_code=400,
                    detail=f"File type {file_ext} not allowed"
                )

            # Save uploaded file
            file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
            with open(file_path, 'wb') as f:
                content = await file.read()
                f.write(content)

            # Validate file size
            file_size = os.path.getsize(file_path)
            if file_size > settings.max_file_size_mb * 1024 * 1024:
                os.remove(file_path)
                raise HTTPException(
                    status_code=400,
                    detail=f"File size exceeds {settings.max_file_size_mb}MB limit"
                )

            # Create document record
            doc_data = DocumentDB.create(kb_id, file.filename, file_ext, file_size)

            # Process document
            try:
                chunks, char_count = document_processor.process_file(
                    file_path,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )

                # Ensure all required Milvus fields have a default value
                for chunk in chunks:
                    # Fields we manage
                    chunk.metadata['document_id'] = doc_data['id']
                    chunk.metadata['producer'] = "user_upload"
                    chunk.metadata['creator'] = "admin"

                    # Set defaults for other schema fields if they don't exist
                    chunk.metadata.setdefault('creationdate', '')
                    chunk.metadata.setdefault('source', doc_data.get('name', 'unknown'))
                    chunk.metadata.setdefault('file_path', '')
                    chunk.metadata.setdefault('total_pages', 1)
                    chunk.metadata.setdefault('format', '')
                    chunk.metadata.setdefault('title', '')
                    chunk.metadata.setdefault('author', '')
                    chunk.metadata.setdefault('subject', '')
                    chunk.metadata.setdefault('keywords', '')
                    chunk.metadata.setdefault('moddate', '')
                    chunk.metadata.setdefault('trapped', '')
                    chunk.metadata.setdefault('modDate', '')
                    chunk.metadata.setdefault('creationDate', '')

                # Add to vector store (replace hyphens with underscores for Milvus compatibility)
                collection_name = f"kb_{kb_id.replace('-', '_')}"
                doc_ids = [f"{doc_data['id'].replace('-', '_')}_{i}" for i in range(len(chunks))]
                vector_store_manager.add_documents(collection_name, chunks, ids=doc_ids)

                # Update document record
                DocumentDB.update(
                    doc_data['id'],
                    character_count=char_count,
                    chunk_count=len(chunks),
                    status="completed"
                )

                uploaded_docs.append(DocumentResponse(**DocumentDB.get(doc_data['id'])))

            except Exception as e:
                logger.error(f"Error processing document: {str(e)}")
                DocumentDB.update(doc_data['id'], status="failed")
                raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
            finally:
                # Clean up uploaded file
                if os.path.exists(file_path):
                    # Force garbage collection to release file handles
                    gc.collect()
                    os.remove(file_path)

        return {"documents": uploaded_docs, "count": len(uploaded_docs)}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{kb_id}", response_model=List[DocumentResponse])
async def list_documents(kb_id: str):
    """List documents in a knowledge base"""
    try:
        kb = KnowledgeBaseDB.get(kb_id)
        if not kb:
            raise HTTPException(status_code=404, detail="Knowledge base not found")

        docs = DocumentDB.list_by_kb(kb_id)
        return [DocumentResponse(**doc) for doc in docs]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document"""
    try:
        doc = DocumentDB.get(doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        DocumentDB.delete(doc_id)
        return {"message": "Document deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

