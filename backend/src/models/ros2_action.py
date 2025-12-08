from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class ROS2ActionSequence(BaseModel):
    """
    ROS 2 Action Sequence: Executable series of robot commands generated from LLM planning
    with feedback and error handling
    """
    id: str
    plan_id: str  # Reference to the LLM plan
    actions: List[Dict[str, Any]]  # List of ROS 2 actions to execute
    status: str  # 'pending', 'executing', 'completed', 'failed', 'cancelled'
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    feedback: List[Dict[str, Any]] = []  # Execution feedback and status updates
    error_message: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "action-001",
                "plan_id": "plan-001",
                "actions": [
                    {
                        "action_type": "navigation",
                        "parameters": {"target_pose": {"x": 1.0, "y": 2.0, "theta": 0.0}},
                        "timeout": 30
                    },
                    {
                        "action_type": "manipulation",
                        "parameters": {"action": "pick_up", "object_id": "bottle-001"},
                        "timeout": 15
                    }
                ],
                "status": "pending",
                "feedback": []
            }
        }