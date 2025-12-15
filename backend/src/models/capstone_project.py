from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class CapstoneProject(BaseModel):
    """
    Capstone Project: Complete implementation integrating all VLA components for
    voice-commanded robot behavior demonstrating mastery of the complete VLA system
    """
    id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    status: str  # 'active', 'completed', 'failed', 'in_progress'
    sessions: List[str]  # List of session IDs associated with this project
    configuration: Dict[str, Any]
    metrics: Dict[str, Any]  # Performance metrics and success rates
    last_execution: Optional[datetime] = None
    total_executions: int = 0
    success_rate: float = 0.0
    error_log: List[Dict[str, Any]] = []

    class Config:
        json_schema_extra = {
            "example": {
                "id": "capstone-001",
                "name": "Autonomous Humanoid Capstone",
                "description": "Complete voice-controlled humanoid robot project",
                "created_at": "2023-10-01T10:00:00Z",
                "updated_at": "2023-10-01T10:00:00Z",
                "status": "active",
                "sessions": ["session-001", "session-002"],
                "configuration": {
                    "robot_type": "humanoid",
                    "capabilities": ["navigation", "manipulation", "perception", "voice_control"],
                    "environment": "indoor_office"
                },
                "metrics": {
                    "total_tasks": 45,
                    "successful_tasks": 42,
                    "average_execution_time": 120.5,
                    "most_common_commands": ["go_to_kitchen", "pick_up_object", "bring_to_user"]
                },
                "last_execution": "2023-10-01T15:30:00Z",
                "total_executions": 15,
                "success_rate": 0.93,
                "error_log": [
                    {
                        "timestamp": "2023-10-01T14:20:00Z",
                        "error": "Navigation failed due to obstacle",
                        "recovery": "Used alternative path planning"
                    }
                ]
            }
        }


class CapstoneSession(BaseModel):
    """
    Capstone Session: A single session of the capstone project with specific tasks and outcomes
    """
    id: str
    project_id: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    status: str  # 'active', 'completed', 'failed', 'cancelled'
    user_preferences: Dict[str, Any]
    robot_state: Dict[str, Any]
    task_history: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    active: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "id": "session-001",
                "project_id": "capstone-001",
                "started_at": "2023-10-01T10:00:00Z",
                "ended_at": "2023-10-01T11:30:00Z",
                "status": "completed",
                "user_preferences": {
                    "voice_volume": "medium",
                    "navigation_speed": "slow",
                    "safety_thresholds": {"distance": 0.5, "force": 10.0}
                },
                "robot_state": {
                    "position": {"x": 1.0, "y": 2.0, "theta": 0.0},
                    "battery_level": 0.85,
                    "active_actions": 0
                },
                "task_history": [
                    {
                        "command": "Go to the kitchen",
                        "result": {"success": True, "execution_time": 45.2},
                        "timestamp": "2023-10-01T10:05:00Z"
                    }
                ],
                "metrics": {
                    "total_tasks": 5,
                    "successful_tasks": 5,
                    "success_rate": 1.0,
                    "execution_time": 1500.0
                },
                "active": False
            }
        }


class CapstoneTask(BaseModel):
    """
    Capstone Task: A specific task within the capstone project, potentially complex and multi-step
    """
    id: str
    session_id: str
    command: str
    plan: Dict[str, Any]  # The LLM-generated plan
    execution_log: List[Dict[str, Any]]
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: str  # 'pending', 'in_progress', 'completed', 'failed', 'cancelled'
    success: bool = False
    execution_time: Optional[float] = None
    error_message: Optional[str] = None
    recovery_attempts: int = 0
    final_state: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "task-001",
                "session_id": "session-001",
                "command": "Set the dining table for two people",
                "plan": {
                    "sub_tasks": [
                        {"action": "navigate_to", "parameters": {"target": "kitchen"}},
                        {"action": "grasp_object", "parameters": {"object": "plate"}},
                        {"action": "navigate_to", "parameters": {"target": "dining_table"}},
                        {"action": "place_object", "parameters": {"location": "setting_1"}}
                    ]
                },
                "execution_log": [
                    {
                        "step": 0,
                        "action": "navigate_to",
                        "result": {"success": True, "details": "Reached kitchen"},
                        "timestamp": "2023-10-01T10:05:10Z"
                    }
                ],
                "started_at": "2023-10-01T10:05:00Z",
                "completed_at": "2023-10-01T10:12:30Z",
                "status": "completed",
                "success": True,
                "execution_time": 450.0,
                "recovery_attempts": 0,
                "final_state": {
                    "robot_position": {"x": 3.2, "y": 1.8, "theta": 1.57},
                    "manipulator_status": "holding_plate"
                }
            }
        }