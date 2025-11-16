"""
Main FastAPI application for Knowledge Base Management System
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import knowledge_base, documents, retrieval

# Configure logging
logging.basicConfig(level=settings.kb_log_level)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Knowledge Base Management System",
    description="API for managing knowledge bases with vector storage",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(knowledge_base.router, prefix="/api/knowledge-bases", tags=["Knowledge Bases"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(retrieval.router, prefix="/api/retrieval", tags=["Retrieval"])


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("Knowledge Base Management System starting up...")
    logger.info(f"Milvus connection: {settings.milvus_host}:{settings.milvus_port}")
    logger.info(f"Embedding model: {settings.embedding_model_name}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Knowledge Base Management System shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.fastapi_host,
        port=settings.fastapi_port,
        reload=settings.fastapi_reload
    )

