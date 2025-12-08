import asyncio
import logging
from typing import Dict, Any, List, Optional
from ..models.ros2_action import ROS2ActionSequence
from ..models.llm_plan import LLMPlan
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class ROS2MappingService:
    """
    Service for mapping LLM-generated plans to ROS 2 action sequences
    """
    def __init__(self):
        # Define the mapping from LLM actions to ROS 2 actions
        self.action_mapping = {
            # Navigation actions
            "navigate_to": {
                "ros2_action": "nav2_msgs/action/NavigateToPose",
                "required_params": ["target"],
                "optional_params": ["speed", "avoid_obstacles", "planner_id"]
            },
            "get_map_location": {
                "ros2_action": "std_srvs/srv/Trigger",  # Simplified for example
                "required_params": ["location"],
                "optional_params": []
            },

            # Manipulation actions
            "grasp_object": {
                "ros2_action": "control_msgs/action/FollowJointTrajectory",
                "required_params": ["object_id"],
                "optional_params": ["grasp_type", "force_limit"]
            },
            "place_object": {
                "ros2_action": "control_msgs/action/FollowJointTrajectory",
                "required_params": ["location"],
                "optional_params": ["object_id", "placement_type"]
            },

            # Perception actions
            "locate_object": {
                "ros2_action": "vision_msgs/action/DetectObjects",  # Example action
                "required_params": ["object_type"],
                "optional_params": ["search_area", "color"]
            },
            "detect_objects": {
                "ros2_action": "vision_msgs/action/DetectObjects",
                "required_params": [],
                "optional_params": ["object_types", "search_area"]
            },

            # Generic actions
            "wait": {
                "ros2_action": "builtin_interfaces/msg/Duration",
                "required_params": ["duration"],
                "optional_params": []
            },
            "speak_response": {
                "ros2_action": "text_to_speech_msgs/action/Speak",  # Example
                "required_params": ["text"],
                "optional_params": ["voice_type", "volume"]
            }
        }

    async def map_plan_to_action_sequence(self, llm_plan: LLMPlan) -> ROS2ActionSequence:
        """
        Map an LLM-generated plan to a ROS 2 action sequence
        """
        try:
            # Convert LLM plan sub-tasks to ROS 2 actions
            ros2_actions = []

            for i, task in enumerate(llm_plan.sub_tasks):
                if not isinstance(task, dict):
                    raise ValueError(f"Task {i} is not a dictionary: {type(task)}")

                if "action" not in task:
                    raise ValueError(f"Task {i} missing 'action' field")

                llm_action = task["action"]
                parameters = task.get("parameters", {})

                # Map the LLM action to ROS 2 action
                ros2_action = await self._map_single_action(llm_action, parameters)
                ros2_actions.append(ros2_action)

            # Create a ROS2ActionSequence object
            sequence_id = f"action_seq_{uuid.uuid4().hex[:8]}"
            action_sequence = ROS2ActionSequence(
                id=sequence_id,
                plan_id=llm_plan.id,
                actions=ros2_actions,
                status="pending",
                started_at=None,
                completed_at=None,
                feedback=[],
                error_message=None
            )

            logger.info(f"Mapped plan {llm_plan.id} to action sequence {sequence_id} with {len(ros2_actions)} actions")
            return action_sequence

        except Exception as e:
            logger.error(f"Error mapping plan to action sequence: {str(e)}")
            raise

    async def _map_single_action(self, llm_action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map a single LLM action to a ROS 2 action
        """
        if llm_action not in self.action_mapping:
            raise ValueError(f"Unknown LLM action: {llm_action}. Available actions: {list(self.action_mapping.keys())}")

        mapping_info = self.action_mapping[llm_action]
        ros2_action_type = mapping_info["ros2_action"]

        # Validate required parameters
        for param in mapping_info["required_params"]:
            if param not in parameters:
                raise ValueError(f"LLM action '{llm_action}' requires parameter '{param}' but it's missing")

        # Create the ROS 2 action representation
        ros2_action = {
            "action_type": ros2_action_type,
            "llm_action": llm_action,  # Keep reference to original action
            "parameters": parameters,
            "description": f"ROS 2 action for LLM task: {llm_action}",
            "timeout": parameters.get("timeout", 30),  # Default timeout of 30 seconds
            "retry_count": parameters.get("retry_count", 1)  # Default to 1 try
        }

        # Add any additional fields that might be needed
        if "required_capabilities" in parameters:
            ros2_action["required_capabilities"] = parameters["required_capabilities"]

        return ros2_action

    async def validate_action_sequence(self, action_sequence: ROS2ActionSequence) -> tuple[bool, List[str]]:
        """
        Validate a ROS 2 action sequence for execution feasibility
        """
        issues = []

        # Check if actions list is not empty
        if not action_sequence.actions:
            issues.append("Action sequence is empty")

        # Validate each action
        for i, action in enumerate(action_sequence.actions):
            if not isinstance(action, dict):
                issues.append(f"Action {i} is not a dictionary: {type(action)}")
                continue

            if "action_type" not in action:
                issues.append(f"Action {i} missing 'action_type' field")

            if "parameters" not in action:
                issues.append(f"Action {i} missing 'parameters' field")

        is_valid = len(issues) == 0
        return is_valid, issues

    async def get_compatible_robot_actions(self, robot_capabilities: List[str]) -> List[str]:
        """
        Get list of actions that are compatible with the given robot capabilities
        """
        # This would normally query the robot's actual capabilities
        # For now, return all supported actions
        return list(self.action_mapping.keys())

    async def optimize_action_sequence(self, action_sequence: ROS2ActionSequence) -> ROS2ActionSequence:
        """
        Optimize an action sequence for better execution (e.g., combining similar actions)
        """
        # For now, return the original sequence
        # In a real implementation, this could:
        # - Combine multiple navigation actions to nearby locations
        # - Optimize the order of actions for efficiency
        # - Add safety checks between critical actions

        logger.info(f"Action sequence {action_sequence.id} optimization completed (no changes made in this implementation)")
        return action_sequence

    async def create_execution_context(self, action_sequence: ROS2ActionSequence, environment_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create execution context combining action sequence with environment information
        """
        context = {
            "sequence_id": action_sequence.id,
            "plan_id": action_sequence.plan_id,
            "actions": action_sequence.actions,
            "environment": environment_context,
            "execution_config": {
                "default_timeout": 30,
                "max_retries": 3,
                "error_recovery": True,
                "feedback_enabled": True
            }
        }

        logger.info(f"Created execution context for sequence {action_sequence.id}")
        return context