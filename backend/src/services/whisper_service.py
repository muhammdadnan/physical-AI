import asyncio
import logging
import tempfile
import os
from typing import Optional, Dict, Any
from openai import OpenAI
from ..config import Config
from ..models.voice_command import VoiceCommand
import base64
from io import BytesIO

logger = logging.getLogger(__name__)

class WhisperService:
    """
    Service for handling Whisper API integration for speech-to-text conversion
    """
    def __init__(self):
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for Whisper service")

        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.WHISPER_MODEL

    async def transcribe_audio(self, audio_data: str, audio_format: str = "wav") -> Dict[str, Any]:
        """
        Transcribe audio data using OpenAI Whisper API

        Args:
            audio_data: Base64 encoded audio data or file path
            audio_format: Audio format (wav, mp3, etc.)

        Returns:
            Dictionary with transcription results
        """
        try:
            # Handle base64 encoded audio data
            if audio_data.startswith("data:"):
                # Extract audio data from data URL
                header, encoded = audio_data.split(",", 1)
                audio_bytes = base64.b64decode(encoded)

                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_format}") as temp_file:
                    temp_file.write(audio_bytes)
                    temp_path = temp_file.name
            else:
                # Assume it's a file path
                temp_path = audio_data

            # Perform transcription
            with open(temp_path, "rb") as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file
                )

            # Clean up temporary file if we created one
            if audio_data.startswith("data:"):
                os.unlink(temp_path)

            # Calculate confidence (using avg_logprob from verbose response as proxy)
            # Note: For more detailed confidence, we could use translation.create with response_format="verbose_json"
            with open(temp_path if audio_data.startswith("data:") else audio_data, "rb") as audio_file:
                detailed_transcript = self.openai_client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    response_format="verbose_json"
                )

            confidence = getattr(detailed_transcript, 'avg_logprob', -0.1)  # Default to -0.1 if not available

            result = {
                "text": transcript.text,
                "confidence": confidence,
                "language": getattr(detailed_transcript, 'language', 'unknown'),
                "duration": getattr(detailed_transcript, 'duration', 0)
            }

            logger.info(f"Successfully transcribed audio with confidence: {confidence}")
            return result

        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            raise

    async def create_voice_command(self, audio_data: str, audio_format: str = "wav") -> VoiceCommand:
        """
        Create a VoiceCommand object from audio data
        """
        try:
            transcription_result = await self.transcribe_audio(audio_data, audio_format)

            # Create a unique ID for the voice command
            import uuid
            from datetime import datetime

            voice_command = VoiceCommand(
                id=f"vc_{uuid.uuid4().hex[:8]}",
                audio_data=audio_data if len(audio_data) < 1000 else f"data:{audio_format};base64:[truncated]",  # Don't store large audio data
                text_transcription=transcription_result["text"],
                confidence=transcription_result["confidence"],
                timestamp=datetime.utcnow(),
                processed=False
            )

            logger.info(f"Created voice command {voice_command.id} with text: {transcription_result['text']}")
            return voice_command

        except Exception as e:
            logger.error(f"Error creating voice command: {str(e)}")
            raise

    async def transcribe_from_url(self, audio_url: str) -> Dict[str, Any]:
        """
        Transcribe audio from a URL
        """
        import requests

        try:
            response = requests.get(audio_url)
            response.raise_for_status()

            # Create temporary file from URL content
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(response.content)
                temp_path = temp_file.name

            # Perform transcription
            result = await self.transcribe_audio(temp_path, "wav")

            # Clean up
            os.unlink(temp_path)

            return result
        except Exception as e:
            logger.error(f"Error transcribing from URL: {str(e)}")
            raise