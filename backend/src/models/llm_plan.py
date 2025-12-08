from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class LLMPlan(BaseModel):
    """
    LLM Plan: Cognitive planning output that decomposes high-level goals into executable sub-tasks
    """
    id: str
    goal: str  # High-level goal like "Clean the room"
    sub_tasks: List[Dict[str, Any]]  # List of sub-tasks with parameters
    generated_at: datetime
    source_command: str  # Reference to the voice command or text input
    status: str  # 'planning', 'completed', 'failed'
    error_message: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "plan-001",
                "goal": "Clean the room",
                "sub_tasks": [
                    {
                        "action": "navigate_to_object",
                        "parameters": {"object_type": "bottle", "location": "table"},
                        "description": "Navigate to the bottle on the table"
                    },
                    {
                        "action": "pick_up_object",
                        "parameters": {"object_id": "bottle-001"},
                        "description": "Pick up the bottle"
                    },
                    {
                        "action": "dispose_object",
                        "parameters": {"location": "trash_bin"},
                        "description": "Dispose of the bottle in the trash bin"
                    }
                ],
                "generated_at": "2023-10-01T10:00:00Z",
                "source_command": "vc-001",
                "status": "completed"
            }
        }