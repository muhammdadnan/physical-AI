from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
import uuid
from ..services.vision_service import VisionService
from ..models.perception_data import PerceptionData
from ..logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/vision", tags=["vision"])

class DetectObjectsRequest(BaseModel):
    """Request model for object detection"""
    image_data: str  # Base64 encoded image data
    image_format: str = "JPEG"
    target_objects: Optional[List[str]] = None  # Specific objects to detect

class DetectObjectsResponse(BaseModel):
    """Response model for object detection"""
    detection_id: str
    timestamp: datetime
    objects: List[Dict[str, Any]]
    scene_description: str
    processing_time: float
    validation: Dict[str, Any]

class GetObjectLocationRequest(BaseModel):
    """Request model for getting object location"""
    image_data: str
    object_type: str

class GetObjectLocationResponse(BaseModel):
    """Response model for object location"""
    object_found: bool
    object_data: Optional[Dict[str, Any]] = None
    confidence: Optional[float] = None

class AnalyzeSceneRequest(BaseModel):
    """Request model for scene analysis"""
    image_data: str

class AnalyzeSceneResponse(BaseModel):
    """Response model for scene analysis"""
    scene_context: Dict[str, Any]
    object_count: int
    object_types: List[str]
    scene_complexity: str

@router.post("/detect-objects", response_model=DetectObjectsResponse)
async def detect_objects(request: DetectObjectsRequest):
    """
    Detect objects in an image using computer vision
    """
    try:
        import time
        start_time = time.time()

        # Initialize the vision service
        vision_service = VisionService()

        if request.target_objects:
            # Detect specific objects
            detected_objects = await vision_service.detect_specific_objects(
                request.image_data,
                request.target_objects
            )

            # Create a temporary perception data object for validation
            temp_perception = PerceptionData(
                id=f"temp_{uuid.uuid4().hex[:8]}",
                timestamp=datetime.utcnow(),
                camera_source="default_camera",
                objects=detected_objects,
                scene_description="",
                processed=True
            )
        else:
            # Detect all objects
            perception_data = await vision_service.detect_objects_in_image(
                request.image_data,
                request.image_format
            )

            detected_objects = perception_data.objects

        # Validate detection accuracy
        temp_perception = PerceptionData(
            id=f"temp_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.utcnow(),
            camera_source="default_camera",
            objects=detected_objects,
            scene_description="",
            processed=True
        )
        validation = await vision_service.validate_detection_accuracy(temp_perception)

        processing_time = time.time() - start_time

        # Generate scene description for the detected objects
        scene_description = await vision_service._generate_scene_description(detected_objects)

        response = DetectObjectsResponse(
            detection_id=f"detection_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.utcnow(),
            objects=detected_objects,
            scene_description=scene_description,
            processing_time=processing_time,
            validation=validation
        )

        logger.info(f"Detected {len(detected_objects)} objects in image, processing time: {processing_time:.3f}s")
        return response

    except Exception as e:
        logger.error(f"Error in object detection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/get-object-location", response_model=GetObjectLocationResponse)
async def get_object_location(request: GetObjectLocationRequest):
    """
    Get the location of a specific object type in an image
    """
    try:
        vision_service = VisionService()

        object_data = await vision_service.get_object_location(
            request.image_data,
            request.object_type
        )

        if object_data:
            response = GetObjectLocationResponse(
                object_found=True,
                object_data=object_data,
                confidence=object_data.get("confidence")
            )
        else:
            response = GetObjectLocationResponse(
                object_found=False
            )

        logger.info(f"Object location query for '{request.object_type}': {'found' if object_data else 'not found'}")
        return response

    except Exception as e:
        logger.error(f"Error getting object location: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-scene", response_model=AnalyzeSceneResponse)
async def analyze_scene(request: AnalyzeSceneRequest):
    """
    Analyze the scene to provide context for planning
    """
    try:
        vision_service = VisionService()

        scene_context = await vision_service.analyze_scene_context(request.image_data)

        response = AnalyzeSceneResponse(
            scene_context=scene_context,
            object_count=scene_context["object_count"],
            object_types=scene_context["object_types"],
            scene_complexity=scene_context["scene_complexity"]
        )

        logger.info(f"Scene analysis completed: {scene_context['object_count']} objects, complexity: {scene_context['scene_complexity']}")
        return response

    except Exception as e:
        logger.error(f"Error analyzing scene: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate-detection")
async def validate_detection(perception_data: PerceptionData):
    """
    Validate the accuracy of object detections
    """
    try:
        vision_service = VisionService()

        validation_result = await vision_service.validate_detection_accuracy(perception_data)

        logger.info(f"Detection validation completed, quality score: {validation_result['quality_score']}")
        return validation_result

    except Exception as e:
        logger.error(f"Error validating detection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/supported-classes")
async def get_supported_classes():
    """
    Get list of object classes that the vision system can detect
    """
    try:
        vision_service = VisionService()

        return {
            "supported_classes": vision_service.supported_classes,
            "total_classes": len(vision_service.supported_classes)
        }
    except Exception as e:
        logger.error(f"Error getting supported classes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def vision_health():
    """
    Health check for vision service
    """
    try:
        vision_service = VisionService()

        return {
            "status": "healthy",
            "service": "vision",
            "supported_classes": len(vision_service.supported_classes),
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        logger.error(f"Vision service health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add the router to the main app in main.py
def register_routes(app):
    app.include_router(router)