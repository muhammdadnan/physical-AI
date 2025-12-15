import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from ..models.capstone_project import CapstoneProject, CapstoneSession, CapstoneTask
from ..services.integrated_vla_service import IntegratedVLAPipeline
from ..services.whisper_service import WhisperService
from ..services.llm_planning_service import LLMPlanningService
from ..services.vision_service import VisionService
from ..services.ros2_integration import ROS2IntegrationService
from ..services.perception_planning_integration import PerceptionPlanningIntegration

logger = logging.getLogger(__name__)

class CapstoneService:
    """
    Service for full VLA integration in the capstone project
    """
    def __init__(self):
        # Initialize all VLA services
        self.vla_pipeline = IntegratedVLAPipeline()
        self.whisper_service = WhisperService()
        self.planning_service = LLMPlanningService()
        self.vision_service = VisionService()
        self.ros2_integration = ROS2IntegrationService()
        self.perception_integration = PerceptionPlanningIntegration()

        # Track active projects and sessions
        self.active_projects = {}
        self.active_sessions = {}
        self.task_history = []

    async def create_capstone_project(
        self,
        name: str,
        description: str,
        configuration: Optional[Dict[str, Any]] = None
    ) -> CapstoneProject:
        """
        Create a new capstone project
        """
        project_id = f"capstone_{uuid.uuid4().hex[:8]}"
        now = datetime.utcnow()

        project = CapstoneProject(
            id=project_id,
            name=name,
            description=description,
            created_at=now,
            updated_at=now,
            status="active",
            sessions=[],
            configuration=configuration or {},
            metrics={
                "total_tasks": 0,
                "successful_tasks": 0,
                "failed_tasks": 0,
                "success_rate": 0.0,
                "average_execution_time": 0.0
            },
            last_execution=None,
            total_executions=0,
            success_rate=0.0,
            error_log=[]
        )

        self.active_projects[project_id] = project

        logger.info(f"Created capstone project: {project_id} - {name}")
        return project

    async def start_capstone_session(
        self,
        project_id: str,
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> CapstoneSession:
        """
        Start a new capstone session
        """
        if project_id not in self.active_projects:
            raise ValueError(f"Project {project_id} not found")

        session_id = f"session_{uuid.uuid4().hex[:8]}"
        now = datetime.utcnow()

        # Get initial robot state
        robot_state = await self._get_current_robot_state()

        session = CapstoneSession(
            id=session_id,
            project_id=project_id,
            started_at=now,
            status="active",
            user_preferences=user_preferences or {},
            robot_state=robot_state,
            task_history=[],
            metrics={
                "total_tasks": 0,
                "successful_tasks": 0,
                "failed_tasks": 0,
                "success_rate": 0.0,
                "execution_time": 0.0
            },
            active=True
        )

        self.active_sessions[session_id] = session

        # Add session to project
        project = self.active_projects[project_id]
        project.sessions.append(session_id)
        project.updated_at = now

        logger.info(f"Started capstone session: {session_id} for project {project_id}")
        return session

    async def execute_capstone_task(
        self,
        session_id: str,
        command: str,
        audio_data: Optional[str] = None,
        camera_data: Optional[str] = None,
        task_context: Optional[Dict[str, Any]] = None
    ) -> CapstoneTask:
        """
        Execute a capstone task with full VLA integration
        """
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")

        task_id = f"task_{uuid.uuid4().hex[:8]}"
        start_time = datetime.utcnow()

        # Create task record
        task = CapstoneTask(
            id=task_id,
            session_id=session_id,
            command=command,
            plan={},
            execution_log=[],
            started_at=start_time,
            status="in_progress",
            success=False,
            execution_time=None,
            error_message=None,
            recovery_attempts=0,
            final_state=None
        )

        try:
            # If audio data is provided, process it through the full pipeline
            if audio_data:
                result = await self.vla_pipeline.process_voice_controlled_task(
                    audio_data=audio_data,
                    camera_image_data=camera_data,
                    task_context=task_context or {}
                )

                if result["success"]:
                    task.success = True
                    task.status = "completed"
                    task.execution_time = result["duration"]
                    task.execution_log = await self._format_execution_log(result)
                    task.plan = result.get("execution_result", {}).get("plan", {})
                    task.final_state = await self._get_current_robot_state()
                else:
                    task.success = False
                    task.status = "failed"
                    task.error_message = result.get("error", "Unknown error")
                    task.execution_log = [{"error": result.get("error"), "timestamp": datetime.utcnow().isoformat()}]

            else:
                # Execute with just command text
                result = await self._execute_command_task(command, camera_data, task_context)

                if result["success"]:
                    task.success = True
                    task.status = "completed"
                    task.execution_time = result["duration"]
                    task.execution_log = await self._format_execution_log(result)
                    task.plan = result.get("plan", {})
                    task.final_state = await self._get_current_robot_state()
                else:
                    task.success = False
                    task.status = "failed"
                    task.error_message = result.get("error", "Unknown error")
                    task.execution_log = [{"error": result.get("error"), "timestamp": datetime.utcnow().isoformat()}]

            # Update session metrics
            await self._update_session_metrics(session_id, task)

            # Update project metrics
            await self._update_project_metrics(self.active_sessions[session_id].project_id, task)

            # Add to task history
            self.task_history.append(task)

            logger.info(f"Completed capstone task: {task_id}, success: {task.success}")
            return task

        except Exception as e:
            logger.error(f"Error executing capstone task {task_id}: {str(e)}")
            task.status = "failed"
            task.error_message = str(e)
            task.success = False
            task.execution_time = (datetime.utcnow() - start_time).total_seconds()
            task.execution_log = [{"error": str(e), "timestamp": datetime.utcnow().isoformat()}]

            # Update session metrics for failure
            await self._update_session_metrics(session_id, task)

            # Update project metrics for failure
            await self._update_project_metrics(self.active_sessions[session_id].project_id, task)

            # Add to task history
            self.task_history.append(task)

            return task

    async def _execute_command_task(
        self,
        command: str,
        camera_data: Optional[str] = None,
        task_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a task based on command text (when no audio provided)
        """
        start_time = datetime.utcnow()

        try:
            # Create plan from command
            context = task_context or {}
            if camera_data:
                context["camera_data"] = camera_data

            plan = await self.planning_service.create_plan_from_goal(
                goal=command,
                context=context
            )

            # Map plan to ROS2 actions
            action_sequence = await self.vla_pipeline.ros2_mapping_service.map_plan_to_action_sequence(plan)

            # Execute the action sequence
            execution_result = await self.vla_pipeline.ros2_integration_service.execute_action_sequence(action_sequence)

            return {
                "success": True,
                "command": command,
                "plan": plan,
                "execution_result": execution_result,
                "duration": (datetime.utcnow() - start_time).total_seconds(),
                "summary": f"Executed '{command}' successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "command": command,
                "error": str(e),
                "duration": (datetime.utcnow() - start_time).total_seconds(),
                "summary": f"Failed to execute '{command}': {str(e)}"
            }

    async def _format_execution_log(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Format execution result into a standardized log format
        """
        log_entries = []

        # Add the main execution result
        log_entries.append({
            "event": "task_execution",
            "result": result.get("execution_result", {}),
            "timestamp": datetime.utcnow().isoformat(),
            "duration": result.get("duration", 0)
        })

        # Add any execution logs from the result
        execution_result = result.get("execution_result", {})
        if "execution_log" in execution_result:
            for log_entry in execution_result["execution_log"]:
                log_entries.append({
                    "event": "action_execution",
                    "details": log_entry,
                    "timestamp": datetime.utcnow().isoformat()
                })

        return log_entries

    async def _update_session_metrics(self, session_id: str, task: CapstoneTask):
        """
        Update session metrics based on task completion
        """
        if session_id not in self.active_sessions:
            return

        session = self.active_sessions[session_id]

        # Update metrics
        session.metrics["total_tasks"] += 1
        if task.success:
            session.metrics["successful_tasks"] += 1
        else:
            session.metrics["failed_tasks"] += 1

        # Recalculate success rate
        total = session.metrics["total_tasks"]
        successful = session.metrics["successful_tasks"]
        session.metrics["success_rate"] = successful / total if total > 0 else 0.0

        # Update execution time
        if task.execution_time is not None:
            current_avg = session.metrics["execution_time"]
            new_avg = (current_avg * (total - 1) + task.execution_time) / total
            session.metrics["execution_time"] = new_avg

        # Add task to history
        session.task_history.append({
            "task_id": task.id,
            "command": task.command,
            "success": task.success,
            "execution_time": task.execution_time,
            "timestamp": task.started_at.isoformat()
        })

    async def _update_project_metrics(self, project_id: str, task: CapstoneTask):
        """
        Update project metrics based on task completion
        """
        if project_id not in self.active_projects:
            return

        project = self.active_projects[project_id]

        # Update metrics
        project.metrics["total_tasks"] += 1
        if task.success:
            project.metrics["successful_tasks"] += 1
        else:
            project.metrics["failed_tasks"] += 1

        # Recalculate success rate
        total = project.metrics["total_tasks"]
        successful = project.metrics["successful_tasks"]
        project.metrics["success_rate"] = successful / total if total > 0 else 0.0

        # Update execution time
        if task.execution_time is not None:
            current_avg = project.metrics["average_execution_time"]
            new_avg = (current_avg * (total - 1) + task.execution_time) / total
            project.metrics["average_execution_time"] = new_avg

        # Update success rate and total executions
        project.total_executions += 1
        project.success_rate = project.metrics["success_rate"]

        # Update last execution time
        project.last_execution = datetime.utcnow()

        # Add to error log if failed
        if not task.success and task.error_message:
            project.error_log.append({
                "timestamp": task.started_at.isoformat(),
                "task_id": task.id,
                "error": task.error_message,
                "command": task.command
            })

        # Keep only the last 100 errors
        if len(project.error_log) > 100:
            project.error_log = project.error_log[-100:]

        project.updated_at = datetime.utcnow()

    async def _get_current_robot_state(self) -> Dict[str, Any]:
        """
        Get the current state of the robot
        """
        try:
            state = await self.ros2_integration.get_robot_status()
            return state
        except Exception as e:
            logger.warning(f"Could not get robot status: {str(e)}, returning default state")
            return {
                "position": {"x": 0.0, "y": 0.0, "theta": 0.0},
                "battery_level": 1.0,
                "active_actions": 0,
                "connected": False
            }

    async def get_project_status(self, project_id: str) -> Optional[CapstoneProject]:
        """
        Get the status of a capstone project
        """
        return self.active_projects.get(project_id)

    async def get_session_status(self, session_id: str) -> Optional[CapstoneSession]:
        """
        Get the status of a capstone session
        """
        return self.active_sessions.get(session_id)

    async def get_task_status(self, task_id: str) -> Optional[CapstoneTask]:
        """
        Get the status of a capstone task
        """
        # Look in active sessions
        for session in self.active_sessions.values():
            for task in session.task_history:
                if task.get("task_id") == task_id:
                    # Find the actual task object
                    for hist_task in self.task_history:
                        if hist_task.id == task_id:
                            return hist_task

        # Look in task history
        for task in self.task_history:
            if task.id == task_id:
                return task

        return None

    async def end_session(self, session_id: str) -> Optional[CapstoneSession]:
        """
        End a capstone session
        """
        if session_id not in self.active_sessions:
            return None

        session = self.active_sessions[session_id]
        session.active = False
        session.ended_at = datetime.utcnow()
        session.status = "completed"

        logger.info(f"Ended capstone session: {session_id}")
        return session

    async def get_project_analytics(self, project_id: str) -> Dict[str, Any]:
        """
        Get analytics for a capstone project
        """
        project = await self.get_project_status(project_id)
        if not project:
            return {"error": f"Project {project_id} not found"}

        # Get session analytics
        session_analytics = []
        for session_id in project.sessions:
            session = await self.get_session_status(session_id)
            if session:
                session_analytics.append({
                    "session_id": session.id,
                    "duration": (session.ended_at - session.started_at).total_seconds() if session.ended_at else None,
                    "tasks_completed": session.metrics["total_tasks"],
                    "success_rate": session.metrics["success_rate"],
                    "active": session.active
                })

        # Get most common commands
        all_commands = []
        for session_id in project.sessions:
            session = await self.get_session_status(session_id)
            if session:
                for task in session.task_history:
                    all_commands.append(task["command"])

        from collections import Counter
        command_counts = Counter(all_commands)
        most_common_commands = [cmd for cmd, count in command_counts.most_common(10)]

        return {
            "project_id": project_id,
            "project_name": project.name,
            "total_sessions": len(project.sessions),
            "total_tasks": project.metrics["total_tasks"],
            "overall_success_rate": project.success_rate,
            "average_task_time": project.metrics["average_execution_time"],
            "session_analytics": session_analytics,
            "most_common_commands": most_common_commands,
            "recent_errors": project.error_log[-5:] if project.error_log else []
        }