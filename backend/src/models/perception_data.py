from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class PerceptionData(BaseModel):
    """
    Perception Data: Visual information from camera streams including object detection,
    localization, and scene understanding
    """
    id: str
    timestamp: datetime
    camera_source: str  # Camera identifier
    objects: List[Dict[str, Any]]  # Detected objects with bounding boxes, types, etc.
    scene_description: Optional[str] = None  # Natural language description of the scene
    processed: bool = False
    related_plan_id: Optional[str] = None  # Link to related LLM plan

    class Config:
        json_schema_extra = {
            "example": {
                "id": "perception-001",
                "timestamp": "2023-10-01T10:00:00Z",
                "camera_source": "front_camera",
                "objects": [
                    {
                        "id": "obj-001",
                        "type": "bottle",
                        "confidence": 0.95,
                        "bbox": {"x": 100, "y": 200, "width": 50, "height": 100},
                        "location_3d": {"x": 1.5, "y": 2.0, "z": 0.8}
                    }
                ],
                "scene_description": "A room with a table containing a red bottle",
                "processed": True
            }
        }