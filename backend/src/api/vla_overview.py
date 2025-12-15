from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
from ..models.vla_pipeline import VLAPipeline
from ..logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/vla", tags=["vla"])

class VLAOverviewResponse(BaseModel):
    """Response model for VLA system overview"""
    system_status: str
    active_pipelines: int
    total_components: int
    component_status: Dict[str, str]  # Status of each component
    recent_activities: List[Dict[str, Any]]

@router.get("/overview", response_model=VLAOverviewResponse)
async def get_vla_overview():
    """
    Get an overview of the VLA system status
    """
    try:
        # For now, return a basic overview
        # In a real system, this would query the actual VLA components
        overview = VLAOverviewResponse(
            system_status="operational",
            active_pipelines=1,
            total_components=4,  # speech-to-text, llm-planning, ros2-execution, perception
            component_status={
                "speech-to-text": "active",
                "llm-planning": "active",
                "ros2-execution": "standby",
                "perception": "active"
            },
            recent_activities=[
                {
                    "id": "activity-001",
                    "timestamp": "2023-10-01T10:00:00Z",
                    "type": "pipeline_created",
                    "description": "Basic Voice Command Pipeline initialized"
                }
            ]
        )

        logger.info("VLA overview retrieved successfully")
        return overview
    except Exception as e:
        logger.error(f"Error retrieving VLA overview: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/components")
async def get_vla_components():
    """
    Get detailed information about VLA system components
    """
    try:
        components = {
            "speech_to_text": {
                "name": "Speech-to-Text",
                "description": "Handles voice input using OpenAI Whisper",
                "status": "active",
                "models": ["whisper-1"]
            },
            "llm_planning": {
                "name": "LLM Cognitive Planning",
                "description": "Translates goals into action sequences using LLMs",
                "status": "active",
                "models": ["gpt-4-turbo"]
            },
            "ros2_execution": {
                "name": "ROS 2 Action Execution",
                "description": "Executes action sequences on ROS 2 robots",
                "status": "standby",
                "supported_actions": ["navigation", "manipulation", "perception"]
            },
            "perception": {
                "name": "Vision Processing",
                "description": "Processes camera streams for object detection",
                "status": "active",
                "capabilities": ["object_detection", "localization", "scene_analysis"]
            }
        }

        logger.info("VLA components retrieved successfully")
        return components
    except Exception as e:
        logger.error(f"Error retrieving VLA components: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add the router to the main app in main.py
def register_routes(app):
    app.include_router(router)