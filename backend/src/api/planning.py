from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
import uuid
from ..services.llm_planning_service import LLMPlanningService
from ..models.llm_plan import LLMPlan
from ..logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/planning", tags=["planning"])

class CreatePlanRequest(BaseModel):
    """Request model for creating an LLM plan"""
    goal: str
    context: Optional[Dict[str, Any]] = {}
    source_command: Optional[str] = "manual"

class CreatePlanResponse(BaseModel):
    """Response model for plan creation"""
    id: str
    goal: str
    sub_tasks: List[Dict[str, Any]]
    generated_at: datetime
    status: str
    error_message: Optional[str] = None

class ValidatePlanRequest(BaseModel):
    """Request model for plan validation"""
    plan: LLMPlan

class ValidatePlanResponse(BaseModel):
    """Response model for plan validation"""
    is_valid: bool
    issues: List[str]

class RefinePlanRequest(BaseModel):
    """Request model for plan refinement"""
    plan: LLMPlan
    feedback: str

@router.post("/create", response_model=CreatePlanResponse)
async def create_llm_plan(request: CreatePlanRequest):
    """
    Create an LLM plan from a high-level goal
    """
    try:
        # Initialize the LLM planning service
        planning_service = LLMPlanningService()

        # Create the plan
        llm_plan = await planning_service.create_plan_from_goal(
            goal=request.goal,
            context=request.context
        )

        # Validate the plan
        is_valid, issues = await planning_service.validate_plan(llm_plan)

        if not is_valid:
            logger.warning(f"Created plan with validation issues: {issues}")

        response = CreatePlanResponse(
            id=llm_plan.id,
            goal=llm_plan.goal,
            sub_tasks=llm_plan.sub_tasks,
            generated_at=llm_plan.generated_at,
            status=llm_plan.status,
            error_message=llm_plan.error_message
        )

        logger.info(f"Successfully created LLM plan: {llm_plan.id}")
        return response

    except Exception as e:
        logger.error(f"Error creating LLM plan: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate", response_model=ValidatePlanResponse)
async def validate_llm_plan(request: ValidatePlanRequest):
    """
    Validate an LLM-generated plan for feasibility and safety
    """
    try:
        planning_service = LLMPlanningService()

        is_valid, issues = await planning_service.validate_plan(request.plan)

        response = ValidatePlanResponse(
            is_valid=is_valid,
            issues=issues
        )

        logger.info(f"Validated plan {request.plan.id}, valid: {is_valid}, issues: {len(issues)}")
        return response

    except Exception as e:
        logger.error(f"Error validating LLM plan: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refine")
async def refine_llm_plan(request: RefinePlanRequest):
    """
    Refine an existing LLM plan based on feedback
    """
    try:
        planning_service = LLMPlanningService()

        refined_plan = await planning_service.refine_plan(request.plan, request.feedback)

        response = CreatePlanResponse(
            id=refined_plan.id,
            goal=refined_plan.goal,
            sub_tasks=refined_plan.sub_tasks,
            generated_at=refined_plan.generated_at,
            status=refined_plan.status,
            error_message=refined_plan.error_message
        )

        logger.info(f"Successfully refined plan from {request.plan.id} to {refined_plan.id}")
        return response

    except Exception as e:
        logger.error(f"Error refining LLM plan: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/examples")
async def get_planning_examples():
    """
    Get examples of different types of plans
    """
    examples = {
        "simple_navigation": {
            "goal": "Go to the kitchen",
            "sub_tasks": [
                {
                    "action": "get_map_location",
                    "parameters": {"location": "kitchen"},
                    "description": "Get the coordinates for the kitchen"
                },
                {
                    "action": "navigate_to",
                    "parameters": {"target": "kitchen_coordinates"},
                    "description": "Navigate to the kitchen"
                }
            ]
        },
        "object_manipulation": {
            "goal": "Bring me the blue bottle from the table",
            "sub_tasks": [
                {
                    "action": "locate_object",
                    "parameters": {"object": "bottle", "color": "blue", "location": "table"},
                    "description": "Find the blue bottle on the table"
                },
                {
                    "action": "navigate_to",
                    "parameters": {"target": "bottle_location"},
                    "description": "Move to the bottle's location"
                },
                {
                    "action": "grasp_object",
                    "parameters": {"object_id": "blue_bottle"},
                    "description": "Pick up the blue bottle"
                },
                {
                    "action": "navigate_to",
                    "parameters": {"target": "user_location"},
                    "description": "Move to the user"
                },
                {
                    "action": "place_object",
                    "parameters": {"location": "delivery_position"},
                    "description": "Place the bottle for the user"
                }
            ]
        },
        "complex_task": {
            "goal": "Set the table for dinner",
            "sub_tasks": [
                {
                    "action": "get_object_list",
                    "parameters": {"object_type": "plate", "count": 4},
                    "description": "Identify 4 plates to use"
                },
                {
                    "action": "get_location",
                    "parameters": {"location_type": "dining_table"},
                    "description": "Get the dining table location"
                },
                {
                    "action": "navigate_to",
                    "parameters": {"target": "plate_location"},
                    "description": "Go to where plates are stored"
                },
                {
                    "action": "grasp_object",
                    "parameters": {"object_id": "plate_1"},
                    "description": "Pick up the first plate"
                },
                {
                    "action": "navigate_to",
                    "parameters": {"target": "table_location"},
                    "description": "Go to the dining table"
                },
                {
                    "action": "place_object",
                    "parameters": {"object_id": "plate_1", "location": "table_position_1"},
                    "description": "Place the first plate"
                }
                # ... continue for all 4 plates and other items
            ]
        }
    }

    logger.info("Retrieved planning examples")
    return examples

@router.get("/health")
async def planning_health():
    """
    Health check for planning service
    """
    try:
        # Check if required configuration is present
        import os
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not configured")

        return {
            "status": "healthy",
            "service": "llm-planning",
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        logger.error(f"Planning service health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add the router to the main app in main.py
def register_routes(app):
    app.include_router(router)