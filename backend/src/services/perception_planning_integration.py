import asyncio
import logging
from typing import Dict, Any, List, Optional
from ..models.perception_data import PerceptionData
from ..models.llm_plan import LLMPlan
from ..services.vision_service import VisionService
from ..services.llm_planning_service import LLMPlanningService
from ..services.ros2_mapping_service import ROS2MappingService
from datetime import datetime

logger = logging.getLogger(__name__)

class PerceptionPlanningIntegration:
    """
    Service for integrating perception results with LLM planning workflow
    """
    def __init__(self):
        self.vision_service = VisionService()
        self.planning_service = LLMPlanningService()
        self.mapping_service = ROS2MappingService()

    async def create_perception_aware_plan(self, goal: str, image_data: str,
                                         additional_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create an LLM plan that incorporates perception data from an image
        """
        try:
            # Step 1: Analyze the current scene using vision
            perception_data = await self.vision_service.detect_objects_in_image(image_data)

            # Step 2: Analyze scene context for planning
            scene_context = await self.vision_service.analyze_scene_context(image_data)

            # Step 3: Combine perception data with planning context
            combined_context = await self._build_planning_context(
                goal,
                perception_data,
                scene_context,
                additional_context
            )

            # Step 4: Create plan with perception-aware context
            llm_plan = await self.planning_service.create_plan_from_goal(
                goal=goal,
                context=combined_context
            )

            # Step 5: Validate the plan considering perception constraints
            is_valid, validation_issues = await self.planning_service.validate_plan(llm_plan)

            result = {
                "plan": llm_plan,
                "perception_data": perception_data,
                "scene_analysis": scene_context,
                "combined_context": combined_context,
                "validation": {
                    "is_valid": is_valid,
                    "issues": validation_issues
                },
                "timestamp": datetime.utcnow().isoformat()
            }

            logger.info(f"Created perception-aware plan for goal: {goal}")
            return result

        except Exception as e:
            logger.error(f"Error creating perception-aware plan: {str(e)}")
            raise

    async def _build_planning_context(self, goal: str, perception_data: PerceptionData,
                                    scene_context: Dict[str, Any],
                                    additional_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Build a comprehensive context for planning that includes perception data
        """
        # Extract key information from perception data
        objects_info = []
        for obj in perception_data.objects:
            objects_info.append({
                "id": obj["id"],
                "type": obj["type"],
                "confidence": obj["confidence"],
                "location_3d": obj["location_3d"],
                "bbox": obj["bbox"]
            })

        # Build context dictionary
        context = {
            "perception": {
                "timestamp": perception_data.timestamp.isoformat(),
                "camera_source": perception_data.camera_source,
                "detected_objects": objects_info,
                "scene_description": perception_data.scene_description,
                "object_count": len(objects_info)
            },
            "scene_analysis": scene_context,
            "original_goal": goal,
            "environment_constraints": await self._analyze_environment_constraints(objects_info),
            "action_feasibility": await self._analyze_action_feasibility(goal, objects_info)
        }

        # Add any additional context provided
        if additional_context:
            context.update(additional_context)

        return context

    async def _analyze_environment_constraints(self, objects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze environment constraints based on detected objects
        """
        constraints = {
            "obstacles": [],
            "navigation_clear": True,
            "manipulation_space": "available",
            "object_densities": {}
        }

        # Identify potential obstacles
        large_objects = [obj for obj in objects if self._is_large_object(obj["type"])]
        for obj in large_objects:
            constraints["obstacles"].append({
                "type": obj["type"],
                "location": obj["location_3d"],
                "approximate_size": self._estimate_object_size(obj["type"])
            })

        # Determine if navigation is clear
        if len(constraints["obstacles"]) > 5:  # Arbitrary threshold
            constraints["navigation_clear"] = False

        # Analyze object densities in different areas
        if objects:
            # Simplified density analysis (in a real system, this would be more sophisticated)
            constraints["object_densities"]["high"] = len(objects) > 8
            constraints["object_densities"]["medium"] = 3 <= len(objects) <= 8
            constraints["object_densities"]["low"] = len(objects) < 3

        return constraints

    async def _analyze_action_feasibility(self, goal: str, objects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze which actions are feasible based on detected objects
        """
        goal_lower = goal.lower()
        feasibility = {
            "grasp_feasible": False,
            "navigation_feasible": True,
            "manipulation_targets": [],
            "required_objects_present": True
        }

        # Check if required objects for the goal are present
        if "grasp" in goal_lower or "pick up" in goal_lower or "take" in goal_lower:
            # Look for graspable objects
            graspable_types = ["bottle", "cup", "box", "book", "laptop"]
            graspable_objects = [obj for obj in objects if obj["type"].lower() in graspable_types]
            feasibility["grasp_feasible"] = len(graspable_objects) > 0
            feasibility["manipulation_targets"] = graspable_objects

            if not graspable_objects:
                feasibility["required_objects_present"] = False

        elif "navigate" in goal_lower or "go to" in goal_lower:
            # Navigation is generally feasible unless environment is extremely cluttered
            feasibility["navigation_feasible"] = len(objects) < 20  # Arbitrary threshold

        return feasibility

    def _is_large_object(self, obj_type: str) -> bool:
        """
        Determine if an object type is considered large/would be an obstacle
        """
        large_objects = ["table", "chair", "sofa", "cabinet", "refrigerator", "person"]
        return obj_type.lower() in large_objects

    def _estimate_object_size(self, obj_type: str) -> str:
        """
        Estimate object size category
        """
        small_objects = ["cup", "bottle", "book", "phone", "remote"]
        medium_objects = ["box", "laptop", "bowl", "plate"]

        obj_lower = obj_type.lower()
        if obj_lower in small_objects:
            return "small"
        elif obj_lower in medium_objects:
            return "medium"
        else:
            return "large"

    async def update_plan_with_new_perception(self, current_plan: LLMPlan, new_image_data: str) -> Dict[str, Any]:
        """
        Update an existing plan based on new perception data
        """
        try:
            # Get new perception data
            new_perception = await self.vision_service.detect_objects_in_image(new_image_data)

            # Analyze how the new perception affects the current plan
            plan_updates = await self._analyze_plan_updates_needed(current_plan, new_perception)

            if plan_updates["needs_revision"]:
                # Create a revised plan incorporating new perception
                revised_plan = await self.planning_service.refine_plan(
                    current_plan,
                    plan_updates["feedback"]
                )

                result = {
                    "original_plan": current_plan,
                    "revised_plan": revised_plan,
                    "perception_update": new_perception,
                    "update_reason": plan_updates["reason"],
                    "changes_made": plan_updates["changes"]
                }
            else:
                # No significant changes needed
                result = {
                    "original_plan": current_plan,
                    "revised_plan": current_plan,  # Same as original
                    "perception_update": new_perception,
                    "update_reason": "no_significant_changes",
                    "changes_made": []
                }

            logger.info(f"Processed perception update for plan {current_plan.id}")
            return result

        except Exception as e:
            logger.error(f"Error updating plan with new perception: {str(e)}")
            raise

    async def _analyze_plan_updates_needed(self, current_plan: LLMPlan, new_perception: PerceptionData) -> Dict[str, Any]:
        """
        Analyze if a plan needs updates based on new perception
        """
        updates_needed = {
            "needs_revision": False,
            "feedback": "",
            "reason": "",
            "changes": []
        }

        # Check if critical objects mentioned in the plan are still present
        for task in current_plan.sub_tasks:
            if "object_id" in str(task) or "object_type" in str(task):
                # Extract object references from the task
                # This is a simplified approach - in reality, this would be more sophisticated
                task_str = str(task).lower()

                # Check if referenced objects still exist in new perception
                for obj in new_perception.objects:
                    if obj["type"].lower() in task_str:
                        # Object still exists, no update needed for this task
                        break
                else:
                    # Object referenced in plan is not in new perception
                    updates_needed["needs_revision"] = True
                    updates_needed["reason"] = f"Referenced object not found in new perception"
                    updates_needed["feedback"] = f"Object referenced in plan is no longer visible in the environment. Plan may need adjustment."
                    updates_needed["changes"].append({
                        "task_affected": task,
                        "issue": "object_not_found",
                        "suggestion": "Re-locate object or adjust plan"
                    })

        # Check if environment has changed significantly
        if abs(len(new_perception.objects) - len(current_plan.sub_tasks)) > 5:
            updates_needed["needs_revision"] = True
            updates_needed["reason"] = "significant_environment_change"
            updates_needed["feedback"] += " Environment has changed significantly since plan creation."
            updates_needed["changes"].append({
                "issue": "environment_change",
                "suggestion": "Consider environment changes in plan execution"
            })

        return updates_needed

    async def validate_perception_plan_alignment(self, plan: LLMPlan, perception_data: PerceptionData) -> Dict[str, Any]:
        """
        Validate that a plan aligns with current perception of the environment
        """
        validation = {
            "is_aligned": True,
            "issues": [],
            "confidence_score": 0.0,
            "recommendations": []
        }

        # Check if objects referenced in plan exist in perception
        missing_objects = []
        for task in plan.sub_tasks:
            task_str = str(task).lower()
            for obj in perception_data.objects:
                if obj["type"].lower() in task_str:
                    break
            else:
                # No matching object found for this task
                if any(obj_type in task_str for obj_type in ["cup", "bottle", "table", "chair"]):
                    missing_objects.append(task)

        if missing_objects:
            validation["is_aligned"] = False
            validation["issues"].append({
                "type": "missing_objects",
                "description": f"Objects referenced in {len(missing_objects)} tasks not found in current perception",
                "tasks_affected": missing_objects
            })
            validation["recommendations"].append("Re-scan environment or adjust plan for current objects")

        # Calculate alignment confidence
        if perception_data.objects:
            aligned_tasks = len(plan.sub_tasks) - len(missing_objects)
            validation["confidence_score"] = aligned_tasks / len(plan.sub_tasks) if plan.sub_tasks else 1.0
        else:
            validation["confidence_score"] = 0.0  # No objects detected, low confidence

        return validation

    async def create_perception_enhanced_context(self, user_query: str, image_data: str) -> Dict[str, Any]:
        """
        Create a context that combines user query, perception data, and relevant knowledge
        for enhanced planning
        """
        # Get perception data
        perception_data = await self.vision_service.detect_objects_in_image(image_data)

        # Analyze the scene
        scene_analysis = await self.vision_service.analyze_scene_context(image_data)

        # Create enhanced context
        enhanced_context = {
            "user_query": user_query,
            "perception_data": {
                "objects": perception_data.objects,
                "scene_description": perception_data.scene_description,
                "object_count": len(perception_data.objects)
            },
            "scene_analysis": scene_analysis,
            "environment_state": {
                "object_types_present": list(set(obj["type"] for obj in perception_data.objects)),
                "spatial_distribution": scene_analysis["spatial_distribution"],
                "complexity": scene_analysis["scene_complexity"]
            },
            "task_suggestions": await self._suggest_tasks_from_perception(perception_data, user_query)
        }

        return enhanced_context

    async def _suggest_tasks_from_perception(self, perception_data: PerceptionData, user_query: str) -> List[str]:
        """
        Suggest possible tasks based on what's perceived in the environment and user query
        """
        suggestions = []

        # Analyze user query intent
        query_lower = user_query.lower()

        # Suggest tasks based on detected objects and query
        for obj in perception_data.objects:
            obj_type = obj["type"].lower()

            # If user wants to manipulate objects
            if any(verb in query_lower for verb in ["pick", "grasp", "take", "move"]):
                if obj_type in ["cup", "bottle", "box", "book"]:
                    suggestions.append(f"Grasp the {obj_type} at location {obj['location_3d']}")

            # If user wants to navigate
            elif any(verb in query_lower for verb in ["go", "navigate", "move to"]):
                if obj_type in ["table", "chair", "kitchen"]:
                    suggestions.append(f"Navigate near the {obj_type}")

        return suggestions