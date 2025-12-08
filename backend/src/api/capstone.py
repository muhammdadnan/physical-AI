from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
import uuid
from ..services.capstone_service import CapstoneService
from ..models.capstone_project import CapstoneProject, CapstoneSession, CapstoneTask
from ..logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/capstone", tags=["capstone"])

class CreateProjectRequest(BaseModel):
    """Request model for creating a capstone project"""
    name: str
    description: str
    configuration: Optional[Dict[str, Any]] = {}

class CreateProjectResponse(BaseModel):
    """Response model for project creation"""
    project_id: str
    name: str
    description: str
    created_at: str
    status: str

class StartSessionRequest(BaseModel):
    """Request model for starting a capstone session"""
    project_id: str
    user_preferences: Optional[Dict[str, Any]] = {}

class StartSessionResponse(BaseModel):
    """Response model for session start"""
    session_id: str
    project_id: str
    started_at: str
    status: str

class ExecuteTaskRequest(BaseModel):
    """Request model for executing a capstone task"""
    session_id: str
    command: str
    audio_data: Optional[str] = None  # Base64 encoded audio data
    camera_data: Optional[str] = None  # Base64 encoded camera image
    task_context: Optional[Dict[str, Any]] = {}

class ExecuteTaskResponse(BaseModel):
    """Response model for task execution"""
    task_id: str
    session_id: str
    command: str
    success: bool
    execution_time: Optional[float] = None
    status: str
    error_message: Optional[str] = None
    summary: str

class ProjectStatusResponse(BaseModel):
    """Response model for project status"""
    project_id: str
    name: str
    description: str
    status: str
    metrics: Dict[str, Any]
    total_executions: int
    success_rate: float
    last_execution: Optional[str] = None
    updated_at: str

class SessionStatusResponse(BaseModel):
    """Response model for session status"""
    session_id: str
    project_id: str
    status: str
    active: bool
    metrics: Dict[str, Any]
    task_count: int

class TaskStatusResponse(BaseModel):
    """Response model for task status"""
    task_id: str
    session_id: str
    command: str
    success: bool
    status: str
    execution_time: Optional[float] = None
    error_message: Optional[str] = None
    started_at: str
    completed_at: Optional[str] = None

class ProjectAnalyticsResponse(BaseModel):
    """Response model for project analytics"""
    project_id: str
    project_name: str
    total_sessions: int
    total_tasks: int
    overall_success_rate: float
    average_task_time: float
    session_analytics: List[Dict[str, Any]]
    most_common_commands: List[str]
    recent_errors: List[Dict[str, Any]]

@router.post("/create-project", response_model=CreateProjectResponse)
async def create_capstone_project(request: CreateProjectRequest):
    """
    Create a new capstone project
    """
    try:
        # Initialize the capstone service
        capstone_service = CapstoneService()

        # Create the project
        project = await capstone_service.create_capstone_project(
            name=request.name,
            description=request.description,
            configuration=request.configuration
        )

        response = CreateProjectResponse(
            project_id=project.id,
            name=project.name,
            description=project.description,
            created_at=project.created_at.isoformat(),
            status=project.status
        )

        logger.info(f"Created capstone project: {project.id} - {project.name}")
        return response

    except Exception as e:
        logger.error(f"Error creating capstone project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/start-session", response_model=StartSessionResponse)
async def start_capstone_session(request: StartSessionRequest):
    """
    Start a new capstone session
    """
    try:
        # Initialize the capstone service
        capstone_service = CapstoneService()

        # Start the session
        session = await capstone_service.start_capstone_session(
            project_id=request.project_id,
            user_preferences=request.user_preferences
        )

        response = StartSessionResponse(
            session_id=session.id,
            project_id=session.project_id,
            started_at=session.started_at.isoformat(),
            status=session.status
        )

        logger.info(f"Started capstone session: {session.id} for project {session.project_id}")
        return response

    except Exception as e:
        logger.error(f"Error starting capstone session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute-task", response_model=ExecuteTaskResponse)
async def execute_capstone_task(request: ExecuteTaskRequest):
    """
    Execute a capstone task with full VLA integration
    """
    try:
        # Initialize the capstone service
        capstone_service = CapstoneService()

        # Execute the task
        task = await capstone_service.execute_capstone_task(
            session_id=request.session_id,
            command=request.command,
            audio_data=request.audio_data,
            camera_data=request.camera_data,
            task_context=request.task_context
        )

        response = ExecuteTaskResponse(
            task_id=task.id,
            session_id=task.session_id,
            command=task.command,
            success=task.success,
            execution_time=task.execution_time,
            status=task.status,
            error_message=task.error_message,
            summary=f"Task {'completed' if task.success else 'failed'}: {request.command}"
        )

        logger.info(f"Executed capstone task: {task.id}, success: {task.success}")
        return response

    except Exception as e:
        logger.error(f"Error executing capstone task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/project/{project_id}", response_model=ProjectStatusResponse)
async def get_capstone_project_status(project_id: str):
    """
    Get the status of a capstone project
    """
    try:
        # Initialize the capstone service
        capstone_service = CapstoneService()

        # Get project status
        project = await capstone_service.get_project_status(project_id)

        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

        response = ProjectStatusResponse(
            project_id=project.id,
            name=project.name,
            description=project.description,
            status=project.status,
            metrics=project.metrics,
            total_executions=project.total_executions,
            success_rate=project.success_rate,
            last_execution=project.last_execution.isoformat() if project.last_execution else None,
            updated_at=project.updated_at.isoformat()
        )

        logger.info(f"Retrieved status for project: {project_id}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting project status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{session_id}", response_model=SessionStatusResponse)
async def get_capstone_session_status(session_id: str):
    """
    Get the status of a capstone session
    """
    try:
        # Initialize the capstone service
        capstone_service = CapstoneService()

        # Get session status
        session = await capstone_service.get_session_status(session_id)

        if not session:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

        response = SessionStatusResponse(
            session_id=session.id,
            project_id=session.project_id,
            status=session.status,
            active=session.active,
            metrics=session.metrics,
            task_count=len(session.task_history)
        )

        logger.info(f"Retrieved status for session: {session_id}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/task/{task_id}", response_model=TaskStatusResponse)
async def get_capstone_task_status(task_id: str):
    """
    Get the status of a capstone task
    """
    try:
        # Initialize the capstone service
        capstone_service = CapstoneService()

        # Get task status
        task = await capstone_service.get_task_status(task_id)

        if not task:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        response = TaskStatusResponse(
            task_id=task.id,
            session_id=task.session_id,
            command=task.command,
            success=task.success,
            status=task.status,
            execution_time=task.execution_time,
            error_message=task.error_message,
            started_at=task.started_at.isoformat(),
            completed_at=task.completed_at.isoformat() if task.completed_at else None
        )

        logger.info(f"Retrieved status for task: {task_id}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/end-session/{session_id}")
async def end_capstone_session(session_id: str):
    """
    End a capstone session
    """
    try:
        # Initialize the capstone service
        capstone_service = CapstoneService()

        # End the session
        session = await capstone_service.end_session(session_id)

        if not session:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

        result = {
            "session_id": session.id,
            "project_id": session.project_id,
            "ended_at": session.ended_at.isoformat(),
            "status": session.status,
            "summary": f"Session {session_id} ended successfully"
        }

        logger.info(f"Ended session: {session_id}")
        return result

    except Exception as e:
        logger.error(f"Error ending session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/{project_id}", response_model=ProjectAnalyticsResponse)
async def get_capstone_project_analytics(project_id: str):
    """
    Get analytics for a capstone project
    """
    try:
        # Initialize the capstone service
        capstone_service = CapstoneService()

        # Get project analytics
        analytics = await capstone_service.get_project_analytics(project_id)

        if "error" in analytics:
            raise HTTPException(status_code=404, detail=analytics["error"])

        response = ProjectAnalyticsResponse(**analytics)

        logger.info(f"Retrieved analytics for project: {project_id}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting project analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def capstone_health():
    """
    Health check for capstone service
    """
    try:
        # Initialize the capstone service
        capstone_service = CapstoneService()

        return {
            "status": "healthy",
            "service": "capstone-vla-integration",
            "active_projects": len(capstone_service.active_projects),
            "active_sessions": len(capstone_service.active_sessions),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Capstone service health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add the router to the main app in main.py
def register_routes(app):
    app.include_router(router)