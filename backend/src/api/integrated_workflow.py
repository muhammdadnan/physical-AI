from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
import uuid
from ..services.integrated_vla_service import IntegratedVLAPipeline
from ..models.vla_pipeline import VLAPipeline
from ..logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/integrated", tags=["integrated"])

class VoiceControlledTaskRequest(BaseModel):
    """Request model for voice-controlled task execution"""
    audio_data: str  # Base64 encoded audio data
    camera_image_data: Optional[str] = None  # Optional camera image for perception
    task_context: Optional[Dict[str, Any]] = {}

class VoiceControlledTaskResponse(BaseModel):
    """Response model for voice-controlled task execution"""
    pipeline_id: str
    success: bool
    command: Optional[str] = None
    summary: str
    transcription_confidence: Optional[float] = None
    plan_tasks: Optional[int] = None
    actions_executed: Optional[int] = None
    execution_status: Optional[str] = None
    perception_used: Optional[bool] = None
    start_time: str
    end_time: str
    duration: float
    error: Optional[str] = None

class CreatePipelineRequest(BaseModel):
    """Request model for creating a VLA pipeline"""
    name: str
    description: str
    components: List[str]
    configuration: Dict[str, Any]

class CreatePipelineResponse(BaseModel):
    """Response model for pipeline creation"""
    pipeline_id: str
    name: str
    description: str
    components: List[str]
    created_at: str
    status: str

class RunPipelineRequest(BaseModel):
    """Request model for running a pipeline"""
    pipeline_id: str
    input_data: Dict[str, Any]

class RunPipelineResponse(BaseModel):
    """Response model for pipeline execution"""
    pipeline_id: str
    success: bool
    result: Dict[str, Any]
    duration: float
    timestamp: str

@router.post("/voice-task", response_model=VoiceControlledTaskResponse)
async def execute_voice_controlled_task(request: VoiceControlledTaskRequest):
    """
    Execute a complete voice-controlled task through the integrated VLA pipeline
    """
    try:
        # Initialize the integrated VLA pipeline
        vla_pipeline = IntegratedVLAPipeline()

        # Initialize ROS 2 connection
        ros2_connected = await vla_pipeline.initialize_ros2_connection()

        # Process the voice-controlled task
        result = await vla_pipeline.process_voice_controlled_task(
            audio_data=request.audio_data,
            camera_image_data=request.camera_image_data,
            task_context=request.task_context
        )

        # Create response based on result
        response = VoiceControlledTaskResponse(
            pipeline_id=result.get("pipeline_id", "unknown"),
            success=result["success"],
            command=result.get("command"),
            summary=result["summary"],
            transcription_confidence=result.get("transcription_confidence"),
            plan_tasks=result.get("plan_tasks"),
            actions_executed=result.get("actions_executed"),
            execution_status=result.get("execution_status"),
            perception_used=result.get("perception_used"),
            start_time=result["start_time"],
            end_time=result["end_time"],
            duration=result["duration"],
            error=result.get("error")
        )

        logger.info(f"Voice-controlled task completed: {result['summary']}")
        return response

    except Exception as e:
        logger.error(f"Error executing voice-controlled task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-pipeline", response_model=CreatePipelineResponse)
async def create_vla_pipeline(request: CreatePipelineRequest):
    """
    Create a new VLA pipeline configuration
    """
    try:
        # Initialize the integrated VLA pipeline
        vla_pipeline = IntegratedVLAPipeline()

        # Create the pipeline
        pipeline = await vla_pipeline.create_vla_pipeline(
            name=request.name,
            description=request.description,
            components=request.components,
            configuration=request.configuration
        )

        response = CreatePipelineResponse(
            pipeline_id=pipeline.id,
            name=pipeline.name,
            description=pipeline.description,
            components=pipeline.components,
            created_at=pipeline.created_at.isoformat(),
            status=pipeline.status
        )

        logger.info(f"Created VLA pipeline: {pipeline.id} - {pipeline.name}")
        return response

    except Exception as e:
        logger.error(f"Error creating VLA pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/run-pipeline", response_model=RunPipelineResponse)
async def run_vla_pipeline(request: RunPipelineRequest):
    """
    Run a configured VLA pipeline with input data
    """
    try:
        # Initialize the integrated VLA pipeline
        vla_pipeline = IntegratedVLAPipeline()

        # Run the pipeline
        start_time = datetime.utcnow()
        result = await vla_pipeline.run_pipeline_with_context(
            pipeline_id=request.pipeline_id,
            input_data=request.input_data
        )
        duration = (datetime.utcnow() - start_time).total_seconds()

        response = RunPipelineResponse(
            pipeline_id=request.pipeline_id,
            success=result["success"],
            result=result,
            duration=duration,
            timestamp=datetime.utcnow().isoformat()
        )

        logger.info(f"Pipeline {request.pipeline_id} execution completed, success: {result['success']}")
        return response

    except Exception as e:
        logger.error(f"Error running VLA pipeline {request.pipeline_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pipeline/{pipeline_id}", response_model=VLAPipeline)
async def get_pipeline_status(pipeline_id: str):
    """
    Get the status of a specific pipeline
    """
    try:
        # Initialize the integrated VLA pipeline
        vla_pipeline = IntegratedVLAPipeline()

        # Get pipeline status
        status = await vla_pipeline.get_pipeline_status(pipeline_id)

        if not status["exists"]:
            raise HTTPException(status_code=404, detail=f"Pipeline {pipeline_id} not found")

        # For now, return the basic pipeline info
        # In a real implementation, we'd retrieve the stored pipeline
        return VLAPipeline(
            id=pipeline_id,
            name=f"Pipeline {pipeline_id}",
            description="VLA pipeline",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            components=["speech-to-text", "llm-planning", "ros2-execution"],
            status=status["status"],
            configuration={}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting pipeline status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/system-status")
async def get_system_status():
    """
    Get overall system status including all active pipelines
    """
    try:
        # Initialize the integrated VLA pipeline
        vla_pipeline = IntegratedVLAPipeline()

        # Get system status
        status = await vla_pipeline.get_system_status()

        logger.info(f"System status requested, operational pipelines: {status['active_pipelines']}")
        return status

    except Exception as e:
        logger.error(f"Error getting system status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate-pipeline")
async def validate_pipeline_integrity(pipeline_id: str, test_input: Dict[str, Any]):
    """
    Validate that a pipeline can process the given input successfully
    """
    try:
        # Initialize the integrated VLA pipeline
        vla_pipeline = IntegratedVLAPipeline()

        # Validate the pipeline
        validation_result = await vla_pipeline.validate_pipeline_integrity(
            pipeline_id=pipeline_id,
            test_input=test_input
        )

        logger.info(f"Pipeline {pipeline_id} validation completed, valid: {validation_result['is_valid']}")
        return validation_result

    except Exception as e:
        logger.error(f"Error validating pipeline {pipeline_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def integrated_workflow_health():
    """
    Health check for integrated workflow service
    """
    try:
        # Initialize the integrated VLA pipeline
        vla_pipeline = IntegratedVLAPipeline()

        # Get system status as health indicator
        status = await vla_pipeline.get_system_status()

        return {
            "status": "healthy",
            "service": "integrated-vla-workflow",
            "active_pipelines": status.get("active_pipelines", 0),
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        logger.error(f"Integrated workflow health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add the router to the main app in main.py
def register_routes(app):
    app.include_router(router)