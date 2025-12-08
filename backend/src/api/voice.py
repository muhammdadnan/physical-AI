from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
import logging
import uuid
from datetime import datetime
from ..services.whisper_service import WhisperService
from ..models.voice_command import VoiceCommand
from ..logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/voice", tags=["voice"])

class VoiceCommandRequest(BaseModel):
    """Request model for voice command processing"""
    audio_data: str  # Base64 encoded audio data or URL
    audio_format: str = "wav"

class VoiceCommandResponse(BaseModel):
    """Response model for voice command processing"""
    id: str
    text_transcription: str
    confidence: float
    timestamp: datetime
    processed: bool
    error_message: Optional[str] = None

class StreamingVoiceRequest(BaseModel):
    """Request model for streaming voice input"""
    audio_chunk: str  # Base64 encoded audio chunk
    session_id: str
    is_final: bool = False

@router.post("/transcribe", response_model=VoiceCommandResponse)
async def transcribe_voice(request: VoiceCommandRequest):
    """
    Transcribe voice command using Whisper API
    """
    try:
        # Initialize Whisper service
        whisper_service = WhisperService()

        # Create voice command from audio data
        voice_command = await whisper_service.create_voice_command(
            request.audio_data,
            request.audio_format
        )

        response = VoiceCommandResponse(
            id=voice_command.id,
            text_transcription=voice_command.text_transcription,
            confidence=voice_command.confidence,
            timestamp=voice_command.timestamp,
            processed=voice_command.processed
        )

        logger.info(f"Successfully processed voice command: {voice_command.id}")
        return response

    except Exception as e:
        logger.error(f"Error processing voice command: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-audio", response_model=VoiceCommandResponse)
async def upload_and_transcribe(
    audio_file: UploadFile = File(...),
    audio_format: str = Form("wav")
):
    """
    Upload an audio file and transcribe it using Whisper API
    """
    try:
        # Read the uploaded file
        audio_content = await audio_file.read()

        # Encode as base64 for processing
        import base64
        audio_data = f"data:{audio_file.content_type};base64,{base64.b64encode(audio_content).decode('utf-8')}"

        # Initialize Whisper service
        whisper_service = WhisperService()

        # Create voice command from audio data
        voice_command = await whisper_service.create_voice_command(
            audio_data,
            audio_format
        )

        response = VoiceCommandResponse(
            id=voice_command.id,
            text_transcription=voice_command.text_transcription,
            confidence=voice_command.confidence,
            timestamp=voice_command.timestamp,
            processed=voice_command.processed
        )

        logger.info(f"Successfully processed uploaded audio file: {voice_command.id}")
        return response

    except Exception as e:
        logger.error(f"Error processing uploaded audio file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/streaming")
async def streaming_voice(request: StreamingVoiceRequest):
    """
    Handle streaming voice input for real-time processing
    """
    try:
        # For now, we'll process each chunk individually
        # In a real implementation, we might buffer chunks until final chunk
        whisper_service = WhisperService()

        result = await whisper_service.transcribe_audio(request.audio_chunk)

        response = {
            "session_id": request.session_id,
            "text": result["text"],
            "confidence": result["confidence"],
            "is_final": request.is_final,
            "timestamp": datetime.utcnow()
        }

        logger.info(f"Processed streaming voice chunk for session {request.session_id}")
        return response

    except Exception as e:
        logger.error(f"Error processing streaming voice: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def voice_health():
    """
    Health check for voice service
    """
    try:
        # Check if Whisper API key is configured
        import os
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not configured")

        return {
            "status": "healthy",
            "service": "voice",
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        logger.error(f"Voice service health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add the router to the main app in main.py
def register_routes(app):
    app.include_router(router)