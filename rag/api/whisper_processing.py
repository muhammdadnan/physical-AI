from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
import asyncio
from ...backend.src.services.whisper_service import WhisperService
from ..config import Config

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/whisper", tags=["whisper"])

class WhisperProcessRequest(BaseModel):
    """Request model for Whisper processing"""
    audio_data: str  # Base64 encoded audio data or URL
    audio_format: str = "wav"
    language: Optional[str] = None  # Optional language specification

class WhisperProcessResponse(BaseModel):
    """Response model for Whisper processing"""
    text: str
    confidence: float
    language: str
    duration: float
    processed_at: str

@router.post("/process", response_model=WhisperProcessResponse)
async def process_audio_with_whisper(request: WhisperProcessRequest):
    """
    Process audio using Whisper API and return transcribed text
    This endpoint is specifically designed for the RAG system to convert voice to text
    that can be used for semantic search and LLM processing
    """
    try:
        # Initialize Whisper service
        # Note: We're using the backend service here, but in a real system you might want
        # to have a separate instance or configuration for the RAG-specific processing
        whisper_service = WhisperService()

        # Transcribe the audio
        result = await whisper_service.transcribe_audio(
            request.audio_data,
            request.audio_format
        )

        from datetime import datetime
        response = WhisperProcessResponse(
            text=result["text"],
            confidence=result["confidence"],
            language=result["language"],
            duration=result["duration"],
            processed_at=datetime.utcnow().isoformat()
        )

        logger.info(f"Successfully processed audio with Whisper, confidence: {result['confidence']}")
        return response

    except Exception as e:
        logger.error(f"Error processing audio with Whisper: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/convert-and-query")
async def convert_audio_and_query_rag(request: WhisperProcessRequest):
    """
    Convert audio to text using Whisper and immediately query the RAG system
    This creates a complete voice-to-RAG-query pipeline
    """
    try:
        # First, process the audio with Whisper
        whisper_service = WhisperService()
        transcription_result = await whisper_service.transcribe_audio(
            request.audio_data,
            request.audio_format
        )

        # Then, use the transcribed text to query the RAG system
        # For now, we'll return the transcription and a placeholder for RAG query
        # In a real implementation, we would call the RAG pipeline here
        from ..storage.rag_pipeline import RAGPipeline
        rag_pipeline = RAGPipeline()

        # Build context from the transcribed query
        context = await rag_pipeline.build_context_window(transcription_result["text"])

        result = {
            "transcription": transcription_result["text"],
            "confidence": transcription_result["confidence"],
            "context_chunks": len(context.split("---")),  # Count context sections
            "context_preview": context[:500] + "..." if len(context) > 500 else context
        }

        logger.info(f"Completed voice-to-RAG pipeline, confidence: {transcription_result['confidence']}")
        return result

    except Exception as e:
        logger.error(f"Error in voice-to-RAG pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def whisper_health():
    """
    Health check for Whisper processing service
    """
    try:
        # Check if required configuration is present
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not configured for Whisper service")

        return {
            "status": "healthy",
            "service": "whisper-processing",
            "configured": True
        }
    except Exception as e:
        logger.error(f"Whisper service health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add the router to the main RAG app
def register_routes(app):
    app.include_router(router)