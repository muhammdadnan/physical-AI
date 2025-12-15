from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import asyncio
from ..storage.rag_pipeline import RAGPipeline
from ..config import Config
from .whisper_processing import register_routes as register_whisper_routes
from .planning_service import register_routes as register_planning_routes

# Validate configuration
Config.validate()

app = FastAPI(title="VLA RAG API", version="1.0.0")

# Initialize RAG pipeline
rag_pipeline = RAGPipeline()

# Set up logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL.upper()))
logger = logging.getLogger(__name__)

# Register API routes
register_whisper_routes(app)
register_planning_routes(app)

class EmbedRequest(BaseModel):
    content: str
    title: str
    path: str
    source: str
    chunk_id: str
    metadata: Optional[Dict[str, Any]] = {}

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class QueryResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    context: str

class SelectedTextRequest(BaseModel):
    selected_text: str
    user_query: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the VLA RAG API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/embed")
async def embed_content(request: EmbedRequest):
    """Parse MDX files → clean markdown → generate OpenAI embeddings → store in Qdrant"""
    try:
        # Create a chunk from the request
        chunk = {
            "id": request.chunk_id,
            "content": request.content,
            "title": request.title,
            "path": request.path,
            "source": request.source,
            "chunk_id": request.chunk_id,
            "metadata": request.metadata or {}
        }

        # Store the chunk in the RAG pipeline
        await rag_pipeline.store_document_chunks([chunk])

        return {
            "status": "success",
            "message": f"Successfully embedded content to {request.path}",
            "chunk_id": request.chunk_id
        }
    except Exception as e:
        logger.error(f"Error embedding content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_content(request: QueryRequest) -> QueryResponse:
    """Retrieve vectors from Qdrant → build context window → call OpenAI Agent"""
    try:
        # Retrieve relevant content
        results = await rag_pipeline.retrieve_relevant_content(request.query, request.top_k)

        # Build context window
        context = await rag_pipeline.build_context_window(request.query, request.top_k)

        return QueryResponse(
            query=request.query,
            results=results,
            context=context
        )
    except Exception as e:
        logger.error(f"Error querying content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/answer_from_selected")
async def answer_from_selected(request: SelectedTextRequest):
    """Answer from selected text only - disable RAG and feed only user-provided text"""
    try:
        # This endpoint would typically call OpenAI with just the selected text
        # For now, we'll return the selected text as context to demonstrate the concept
        return {
            "query": request.user_query,
            "selected_text": request.selected_text,
            "answer": f"Based on the selected text: '{request.selected_text}', the answer to '{request.user_query}' would be generated here.",
            "mode": "selected_text_only"
        }
    except Exception as e:
        logger.error(f"Error answering from selected text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Additional API endpoints will be added as we implement the VLA system