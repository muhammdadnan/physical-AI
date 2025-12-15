from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
import uuid
from ..services.ros2_mapping_service import ROS2MappingService
from ..models.ros2_action import ROS2ActionSequence
from ..models.llm_plan import LLMPlan
from ..logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/actions", tags=["actions"])

class MapPlanRequest(BaseModel):
    """Request model for mapping an LLM plan to ROS 2 actions"""
    llm_plan: LLMPlan

class MapPlanResponse(BaseModel):
    """Response model for plan mapping"""
    sequence_id: str
    plan_id: str
    action_count: int
    actions: List[Dict[str, Any]]

class ExecuteSequenceRequest(BaseModel):
    """Request model for executing an action sequence"""
    sequence: ROS2ActionSequence
    environment_context: Optional[Dict[str, Any]] = {}

class ExecuteSequenceResponse(BaseModel):
    """Response model for sequence execution"""
    sequence_id: str
    status: str
    execution_log: List[Dict[str, Any]]
    completed_at: Optional[str] = None
    error_message: Optional[str] = None

class ValidateSequenceRequest(BaseModel):
    """Request model for sequence validation"""
    sequence: ROS2ActionSequence

class ValidateSequenceResponse(BaseModel):
    """Response model for sequence validation"""
    is_valid: bool
    issues: List[str]

@router.post("/map-plan", response_model=MapPlanResponse)
async def map_llm_plan_to_ros2_actions(request: MapPlanRequest):
    """
    Map an LLM-generated plan to a ROS 2 action sequence
    """
    try:
        # Initialize the ROS2 mapping service
        mapping_service = ROS2MappingService()

        # Map the LLM plan to a ROS 2 action sequence
        action_sequence = await mapping_service.map_plan_to_action_sequence(request.llm_plan)

        response = MapPlanResponse(
            sequence_id=action_sequence.id,
            plan_id=action_sequence.plan_id,
            action_count=len(action_sequence.actions),
            actions=action_sequence.actions
        )

        logger.info(f"Successfully mapped LLM plan {request.llm_plan.id} to ROS2 sequence {action_sequence.id}")
        return response

    except Exception as e:
        logger.error(f"Error mapping LLM plan to ROS2 actions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute", response_model=ExecuteSequenceResponse)
async def execute_ros2_action_sequence(request: ExecuteSequenceRequest):
    """
    Execute a ROS 2 action sequence
    Note: In a real implementation, this would interface with actual ROS 2 nodes
    For this example, we'll simulate execution
    """
    try:
        sequence = request.sequence

        # Validate the sequence first
        mapping_service = ROS2MappingService()
        is_valid, issues = await mapping_service.validate_action_sequence(sequence)

        if not is_valid:
            logger.warning(f"Executing sequence {sequence.id} with validation issues: {issues}")

        # Update status to executing
        sequence.status = "executing"
        sequence.started_at = datetime.utcnow()

        # Simulate execution of each action
        execution_log = []
        error_occurred = False
        error_message = None

        for i, action in enumerate(sequence.actions):
            try:
                # Log the action execution
                action_log = {
                    "action_index": i,
                    "action_type": action.get("action_type", "unknown"),
                    "llm_action": action.get("llm_action", "unknown"),
                    "status": "in_progress",
                    "timestamp": datetime.utcnow().isoformat()
                }
                execution_log.append(action_log)

                # Simulate action execution (in real system, this would call ROS 2)
                # Here we'll just log and simulate success/failure
                import random
                # 90% success rate for simulation
                success = random.random() < 0.9

                if success:
                    action_log.update({
                        "status": "completed",
                        "result": {"success": True, "details": f"Action {i} completed successfully"},
                        "completed_at": datetime.utcnow().isoformat()
                    })
                else:
                    action_log.update({
                        "status": "failed",
                        "result": {"success": False, "error": f"Simulated failure for action {i}"},
                        "completed_at": datetime.utcnow().isoformat()
                    })
                    # For simulation, we'll continue with other actions, but in real system
                    # you might want to stop execution based on criticality

            except Exception as action_error:
                logger.error(f"Error executing action {i} in sequence {sequence.id}: {str(action_error)}")
                execution_log.append({
                    "action_index": i,
                    "status": "error",
                    "error": str(action_error),
                    "timestamp": datetime.utcnow().isoformat()
                })

        # Determine final status
        if any(log.get("status") == "error" or
               (log.get("result", {}).get("success") == False) for log in execution_log):
            sequence.status = "failed"
            error_message = "One or more actions failed during execution"
        else:
            sequence.status = "completed"

        sequence.completed_at = datetime.utcnow()
        sequence.feedback = execution_log

        response = ExecuteSequenceResponse(
            sequence_id=sequence.id,
            status=sequence.status,
            execution_log=execution_log,
            completed_at=sequence.completed_at.isoformat() if sequence.completed_at else None,
            error_message=error_message
        )

        logger.info(f"Completed execution of sequence {sequence.id}, status: {sequence.status}")
        return response

    except Exception as e:
        logger.error(f"Error executing ROS2 action sequence: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate", response_model=ValidateSequenceResponse)
async def validate_ros2_action_sequence(request: ValidateSequenceRequest):
    """
    Validate a ROS 2 action sequence for execution feasibility
    """
    try:
        mapping_service = ROS2MappingService()

        is_valid, issues = await mapping_service.validate_action_sequence(request.sequence)

        response = ValidateSequenceResponse(
            is_valid=is_valid,
            issues=issues
        )

        logger.info(f"Validated sequence {request.sequence.id}, valid: {is_valid}, issues: {len(issues)}")
        return response

    except Exception as e:
        logger.error(f"Error validating ROS2 action sequence: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/compatible-actions")
async def get_compatible_actions(robot_capabilities: Optional[str] = None):
    """
    Get list of actions compatible with robot capabilities
    """
    try:
        mapping_service = ROS2MappingService()

        if robot_capabilities:
            # Parse comma-separated capabilities if provided
            capabilities_list = [cap.strip() for cap in robot_capabilities.split(",")]
        else:
            capabilities_list = []  # Empty list means all supported actions

        compatible_actions = await mapping_service.get_compatible_robot_actions(capabilities_list)

        return {
            "compatible_actions": compatible_actions,
            "total_count": len(compatible_actions),
            "robot_capabilities": capabilities_list
        }

    except Exception as e:
        logger.error(f"Error getting compatible actions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/action-mapping")
async def get_action_mapping():
    """
    Get the mapping from LLM actions to ROS 2 actions
    """
    try:
        mapping_service = ROS2MappingService()

        # Return the action mapping dictionary
        return {
            "action_mapping": mapping_service.action_mapping,
            "total_mappings": len(mapping_service.action_mapping)
        }
    except Exception as e:
        logger.error(f"Error getting action mapping: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def actions_health():
    """
    Health check for actions service
    """
    try:
        # Check if the service is properly initialized
        mapping_service = ROS2MappingService()

        return {
            "status": "healthy",
            "service": "ros2-actions",
            "supported_actions": len(mapping_service.action_mapping),
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        logger.error(f"Actions service health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add the router to the main app in main.py
def register_routes(app):
    app.include_router(router)