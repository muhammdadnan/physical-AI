from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging
import asyncio
from ...backend.src.services.llm_planning_service import LLMPlanningService
from ..config import Config

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/planning", tags=["planning"])

class PlanRequest(BaseModel):
    """Request model for LLM planning"""
    goal: str
    context: Optional[Dict[str, Any]] = {}
    user_query: Optional[str] = ""

class PlanResponse(BaseModel):
    """Response model for LLM planning"""
    plan_id: str
    goal: str
    sub_tasks: List[Dict[str, Any]]
    generated_at: str
    status: str
    error_message: Optional[str] = None

class PlanWithContextRequest(BaseModel):
    """Request model for planning with RAG context"""
    goal: str
    rag_context: str  # Context retrieved from RAG system
    user_context: Optional[Dict[str, Any]] = {}

@router.post("/create", response_model=PlanResponse)
async def create_cognitive_plan(request: PlanRequest):
    """
    Create a cognitive plan using LLM for task decomposition
    This endpoint integrates with the OpenAI API for cognitive planning
    """
    try:
        # Initialize the LLM planning service
        planning_service = LLMPlanningService()

        # Create the plan from the goal and context
        llm_plan = await planning_service.create_plan_from_goal(
            goal=request.goal,
            context=request.context
        )

        from datetime import datetime
        response = PlanResponse(
            plan_id=llm_plan.id,
            goal=llm_plan.goal,
            sub_tasks=llm_plan.sub_tasks,
            generated_at=llm_plan.generated_at.isoformat(),
            status=llm_plan.status,
            error_message=llm_plan.error_message
        )

        logger.info(f"Successfully created cognitive plan: {llm_plan.id}")
        return response

    except Exception as e:
        logger.error(f"Error creating cognitive plan: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/with-context")
async def create_plan_with_rag_context(request: PlanWithContextRequest):
    """
    Create a plan using both the user goal and context retrieved from RAG system
    This combines semantic search results with LLM planning for more informed decisions
    """
    try:
        # Initialize the LLM planning service
        planning_service = LLMPlanningService()

        # Combine the RAG context with user context
        combined_context = {
            "rag_retrieved_context": request.rag_context,
            "user_context": request.user_context,
            "current_environment": "vla_robot_system",
            "available_actions": [
                "navigate_to", "grasp_object", "place_object", "locate_object",
                "detect_objects", "move_arm", "speak_response", "wait"
            ]
        }

        # Create the plan using both goal and enriched context
        llm_plan = await planning_service.create_plan_from_goal(
            goal=request.goal,
            context=combined_context
        )

        # Validate the plan
        is_valid, issues = await planning_service.validate_plan(llm_plan)

        if not is_valid:
            logger.warning(f"Plan created with validation issues: {issues}")

        result = {
            "plan_id": llm_plan.id,
            "goal": llm_plan.goal,
            "sub_tasks": llm_plan.sub_tasks,
            "generated_at": llm_plan.generated_at.isoformat(),
            "status": llm_plan.status,
            "validation": {
                "is_valid": is_valid,
                "issues": issues
            },
            "context_used": {
                "rag_context_length": len(request.rag_context),
                "user_context_keys": list(request.user_context.keys()) if request.user_context else []
            }
        }

        logger.info(f"Successfully created contextual plan: {llm_plan.id}")
        return result

    except Exception as e:
        logger.error(f"Error creating contextual plan: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refine")
async def refine_plan_with_feedback(goal: str, current_plan: List[Dict[str, Any]], feedback: str):
    """
    Refine an existing plan based on feedback and context
    """
    try:
        # Create a temporary LLMPlan object for refinement
        from ...backend.src.models.llm_plan import LLMPlan
        from datetime import datetime

        temp_plan = LLMPlan(
            id="temp_refinement",
            goal=goal,
            sub_tasks=current_plan,
            generated_at=datetime.utcnow(),
            source_command="refinement",
            status="completed"
        )

        # Initialize the LLM planning service
        planning_service = LLMPlanningService()

        # Refine the plan based on feedback
        refined_plan = await planning_service.refine_plan(temp_plan, feedback)

        result = {
            "original_plan_id": temp_plan.id,
            "refined_plan_id": refined_plan.id,
            "goal": refined_plan.goal,
            "sub_tasks": refined_plan.sub_tasks,
            "refined_at": refined_plan.generated_at.isoformat(),
            "status": refined_plan.status
        }

        logger.info(f"Successfully refined plan from {temp_plan.id} to {refined_plan.id}")
        return result

    except Exception as e:
        logger.error(f"Error refining plan: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def planning_service_health():
    """
    Health check for the planning service
    """
    try:
        # Check if required configuration is present
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not configured for planning service")

        return {
            "status": "healthy",
            "service": "llm-planning-service",
            "configured": True
        }
    except Exception as e:
        logger.error(f"Planning service health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add the router to the main RAG app
def register_routes(app):
    app.include_router(router)