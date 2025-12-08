from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class VLAPipeline(BaseModel):
    """
    VLA Pipeline: Complete system architecture connecting voice input to robot action execution,
    including speech-to-text, LLM planning, ROS 2 execution, and perception
    """
    id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    components: List[str]  # ['speech-to-text', 'llm-planning', 'ros2-execution', 'perception']
    status: str  # 'active', 'inactive', 'error'
    configuration: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "id": "pipeline-001",
                "name": "Basic Voice Command Pipeline",
                "description": "Simple pipeline for voice-to-action conversion",
                "created_at": "2023-10-01T10:00:00Z",
                "updated_at": "2023-10-01T10:00:00Z",
                "components": ["speech-to-text", "llm-planning", "ros2-execution"],
                "status": "active",
                "configuration": {
                    "whisper_model": "whisper-1",
                    "llm_model": "gpt-4-turbo",
                    "ros2_action_timeout": 30
                }
            }
        }