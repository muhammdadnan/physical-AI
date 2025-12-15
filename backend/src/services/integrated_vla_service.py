import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
from ..services.whisper_service import WhisperService
from ..services.llm_planning_service import LLMPlanningService
from ..services.vision_service import VisionService
from ..services.ros2_mapping_service import ROS2MappingService
from ..services.ros2_integration import ROS2IntegrationService
from ..services.perception_planning_integration import PerceptionPlanningIntegration
from ..models.vla_pipeline import VLAPipeline
from ..models.voice_command import VoiceCommand
from ..models.llm_plan import LLMPlan
from ..models.ros2_action import ROS2ActionSequence
from ..models.perception_data import PerceptionData

logger = logging.getLogger(__name__)

class IntegratedVLAPipeline:
    """
    Integrated VLA pipeline service that combines all VLA components
    """
    def __init__(self):
        # Initialize all VLA services
        self.whisper_service = WhisperService()
        self.planning_service = LLMPlanningService()
        self.vision_service = VisionService()
        self.ros2_mapping_service = ROS2MappingService()
        self.ros2_integration_service = ROS2IntegrationService()
        self.perception_planning_integration = PerceptionPlanningIntegration()

        # Track active pipelines
        self.active_pipelines = {}

    async def initialize_ros2_connection(self) -> bool:
        """
        Initialize connection to ROS 2 system
        """
        try:
            connected = await self.ros2_integration_service.connect_to_ros2()
            if connected:
                logger.info("Successfully connected to ROS 2 system")
            else:
                logger.warning("Could not connect to ROS 2 system - running in simulation mode")
            return connected
        except Exception as e:
            logger.error(f"Error initializing ROS 2 connection: {str(e)}")
            return False

    async def process_voice_controlled_task(
        self,
        audio_data: str,
        camera_image_data: Optional[str] = None,
        task_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a complete voice-controlled task through the integrated VLA pipeline
        """
        try:
            # Create a unique pipeline ID for this task
            pipeline_id = f"vla_pipeline_{uuid.uuid4().hex[:8]}"
            start_time = datetime.utcnow()

            # Phase 1: Voice Processing
            logger.info(f"Pipeline {pipeline_id}: Starting voice processing")
            voice_result = await self._process_voice_command(audio_data)

            if not voice_result["success"]:
                return {
                    "pipeline_id": pipeline_id,
                    "success": False,
                    "error": voice_result["error"],
                    "phase": "voice_processing",
                    "start_time": start_time.isoformat(),
                    "end_time": datetime.utcnow().isoformat(),
                    "duration": (datetime.utcnow() - start_time).total_seconds()
                }

            command_text = voice_result["command"]
            logger.info(f"Pipeline {pipeline_id}: Recognized command: '{command_text}'")

            # Phase 2: Perception Integration (if camera data available)
            perception_context = {}
            if camera_image_data:
                logger.info(f"Pipeline {pipeline_id}: Processing perception data")
                perception_result = await self._integrate_perception(camera_image_data, command_text)
                perception_context = perception_result.get("enhanced_context", {})
                logger.info(f"Pipeline {pipeline_id}: Integrated perception with {len(perception_context.get('perception', {}).get('detected_objects', []))} objects")

            # Combine with any additional task context
            combined_context = {**perception_context}
            if task_context:
                combined_context.update(task_context)

            # Phase 3: LLM Planning
            logger.info(f"Pipeline {pipeline_id}: Generating LLM plan")
            plan_result = await self._generate_plan(command_text, combined_context)
            plan = plan_result["plan"]
            logger.info(f"Pipeline {pipeline_id}: Generated plan with {len(plan.sub_tasks)} sub-tasks")

            # Phase 4: Action Mapping
            logger.info(f"Pipeline {pipeline_id}: Mapping plan to ROS 2 actions")
            action_sequence = await self._map_to_ros2_actions(plan)
            logger.info(f"Pipeline {pipeline_id}: Mapped to {len(action_sequence.actions)} ROS 2 actions")

            # Phase 5: Execution
            logger.info(f"Pipeline {pipeline_id}: Executing action sequence")
            execution_result = await self._execute_action_sequence(action_sequence)

            # Phase 6: Result Compilation
            result = {
                "pipeline_id": pipeline_id,
                "success": True,
                "command": command_text,
                "transcription_confidence": voice_result["confidence"],
                "plan_tasks": len(plan.sub_tasks),
                "actions_executed": len(action_sequence.actions),
                "execution_status": execution_result["status"],
                "execution_result": execution_result,
                "perception_used": bool(camera_image_data),
                "start_time": start_time.isoformat(),
                "end_time": datetime.utcnow().isoformat(),
                "duration": (datetime.utcnow() - start_time).total_seconds(),
                "summary": f"Successfully executed '{command_text}' with {len(plan.sub_tasks)} tasks"
            }

            logger.info(f"Pipeline {pipeline_id}: Task completed successfully")
            return result

        except Exception as e:
            logger.error(f"Error in integrated VLA pipeline: {str(e)}")
            return {
                "pipeline_id": "unknown",
                "success": False,
                "error": str(e),
                "start_time": start_time.isoformat() if 'start_time' in locals() else datetime.utcnow().isoformat(),
                "end_time": datetime.utcnow().isoformat(),
                "duration": (datetime.utcnow() - start_time).total_seconds() if 'start_time' in locals() else 0,
                "summary": f"Task failed due to error: {str(e)}"
            }

    async def _process_voice_command(self, audio_data: str) -> Dict[str, Any]:
        """
        Process voice command using Whisper
        """
        try:
            transcription_result = await self.whisper_service.transcribe_audio(audio_data)

            if transcription_result["confidence"] < 0.5:
                return {
                    "success": False,
                    "error": f"Low transcription confidence: {transcription_result['confidence']:.2f}",
                    "confidence": transcription_result["confidence"]
                }

            return {
                "success": True,
                "command": transcription_result["text"],
                "confidence": transcription_result["confidence"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Voice processing error: {str(e)}",
                "confidence": 0.0
            }

    async def _integrate_perception(self, image_data: str, command_text: str) -> Dict[str, Any]:
        """
        Integrate perception data with the command
        """
        try:
            # Create perception-aware context
            enhanced_context = await self.perception_planning_integration.create_perception_enhanced_context(
                user_query=command_text,
                image_data=image_data
            )

            return {
                "success": True,
                "enhanced_context": enhanced_context
            }
        except Exception as e:
            logger.warning(f"Perception integration failed: {str(e)}, proceeding without perception")
            return {
                "success": True,
                "enhanced_context": {}
            }

    async def _generate_plan(self, command_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate LLM plan for the command
        """
        try:
            # Create plan with or without context
            plan = await self.planning_service.create_plan_from_goal(
                goal=command_text,
                context=context
            )

            # Validate the plan
            is_valid, issues = await self.planning_service.validate_plan(plan)

            return {
                "plan": plan,
                "is_valid": is_valid,
                "validation_issues": issues
            }
        except Exception as e:
            raise Exception(f"Plan generation failed: {str(e)}")

    async def _map_to_ros2_actions(self, plan: LLMPlan) -> ROS2ActionSequence:
        """
        Map LLM plan to ROS 2 action sequence
        """
        try:
            action_sequence = await self.ros2_mapping_service.map_plan_to_action_sequence(plan)

            # Validate the action sequence
            is_valid, issues = await self.ros2_mapping_service.validate_action_sequence(action_sequence)

            if not is_valid:
                logger.warning(f"Action sequence validation issues: {issues}")

            return action_sequence
        except Exception as e:
            raise Exception(f"Action mapping failed: {str(e)}")

    async def _execute_action_sequence(self, action_sequence: ROS2ActionSequence) -> Dict[str, Any]:
        """
        Execute the ROS 2 action sequence
        """
        try:
            execution_result = await self.ros2_integration_service.execute_action_sequence(action_sequence)
            return execution_result
        except Exception as e:
            raise Exception(f"Action execution failed: {str(e)}")

    async def create_vla_pipeline(
        self,
        name: str,
        description: str,
        components: List[str],
        configuration: Dict[str, Any]
    ) -> VLAPipeline:
        """
        Create a new VLA pipeline configuration
        """
        pipeline_id = f"pipeline_{uuid.uuid4().hex[:8]}"
        now = datetime.utcnow()

        pipeline = VLAPipeline(
            id=pipeline_id,
            name=name,
            description=description,
            created_at=now,
            updated_at=now,
            components=components,
            status="active",
            configuration=configuration
        )

        # Store in active pipelines
        self.active_pipelines[pipeline_id] = pipeline

        logger.info(f"Created VLA pipeline: {pipeline_id} - {name}")
        return pipeline

    async def run_pipeline_with_context(
        self,
        pipeline_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Run a configured pipeline with specific input data
        """
        if pipeline_id not in self.active_pipelines:
            raise ValueError(f"Pipeline {pipeline_id} not found")

        pipeline = self.active_pipelines[pipeline_id]

        try:
            # Determine pipeline type based on components
            if "speech-to-text" in pipeline.components and "llm-planning" in pipeline.components:
                # This is a voice-controlled pipeline
                audio_data = input_data.get("audio_data")
                camera_data = input_data.get("camera_data")

                result = await self.process_voice_controlled_task(
                    audio_data=audio_data,
                    camera_image_data=camera_data,
                    task_context=pipeline.configuration
                )

                return result
            else:
                # For other pipeline types, implement accordingly
                raise ValueError(f"Pipeline type not supported: {pipeline.components}")

        except Exception as e:
            logger.error(f"Error running pipeline {pipeline_id}: {str(e)}")
            return {
                "pipeline_id": pipeline_id,
                "success": False,
                "error": str(e),
                "summary": f"Pipeline execution failed: {str(e)}"
            }

    async def get_pipeline_status(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Get the status of a specific pipeline
        """
        if pipeline_id not in self.active_pipelines:
            return {
                "pipeline_id": pipeline_id,
                "exists": False,
                "status": "not_found"
            }

        pipeline = self.active_pipelines[pipeline_id]
        return {
            "pipeline_id": pipeline_id,
            "exists": True,
            "name": pipeline.name,
            "status": pipeline.status,
            "components": pipeline.components,
            "created_at": pipeline.created_at.isoformat(),
            "updated_at": pipeline.updated_at.isoformat()
        }

    async def get_system_status(self) -> Dict[str, Any]:
        """
        Get overall system status including all active pipelines
        """
        try:
            # Get status of all services
            ros2_status = await self.ros2_integration_service.get_robot_status()

            return {
                "system_status": "operational",
                "active_pipelines": len(self.active_pipelines),
                "pipeline_ids": list(self.active_pipelines.keys()),
                "services": {
                    "whisper": "available",
                    "planning": "available",
                    "vision": "available",
                    "ros2_integration": ros2_status.get("connected", False),
                    "perception_planning_integration": "available"
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting system status: {str(e)}")
            return {
                "system_status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    async def update_pipeline_configuration(
        self,
        pipeline_id: str,
        configuration: Dict[str, Any]
    ) -> VLAPipeline:
        """
        Update the configuration of an existing pipeline
        """
        if pipeline_id not in self.active_pipelines:
            raise ValueError(f"Pipeline {pipeline_id} not found")

        pipeline = self.active_pipelines[pipeline_id]

        # Update configuration and timestamp
        pipeline.configuration.update(configuration)
        pipeline.updated_at = datetime.utcnow()

        logger.info(f"Updated configuration for pipeline {pipeline_id}")
        return pipeline

    async def validate_pipeline_integrity(
        self,
        pipeline_id: str,
        test_input: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate that a pipeline can process the given input successfully
        """
        try:
            # Run a test execution with the pipeline
            result = await self.run_pipeline_with_context(pipeline_id, test_input)

            validation_result = {
                "pipeline_id": pipeline_id,
                "is_valid": result["success"],
                "validation_result": result,
                "issues": [] if result["success"] else [result.get("error", "Unknown error")]
            }

            return validation_result

        except Exception as e:
            return {
                "pipeline_id": pipeline_id,
                "is_valid": False,
                "validation_result": None,
                "issues": [str(e)]
            }