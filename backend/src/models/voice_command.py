from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VoiceCommand(BaseModel):
    """
    Voice Command: Natural language input processed through Whisper speech recognition
    for robot task triggering
    """
    id: str
    audio_data: Optional[str] = None  # Base64 encoded audio data or URL
    text_transcription: str
    confidence: float  # Speech recognition confidence (0.0-1.0)
    timestamp: datetime
    processed: bool = False
    error_message: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "vc-001",
                "text_transcription": "Move forward 1 meter",
                "confidence": 0.95,
                "timestamp": "2023-10-01T10:00:00Z",
                "processed": False
            }
        }