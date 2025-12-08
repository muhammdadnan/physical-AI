import asyncio
import logging
import json
import re
from typing import Dict, Any, List, Optional
from openai import OpenAI
from ..config import Config
from ..models.llm_plan import LLMPlan
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class LLMPlanningService:
    """
    Service for using LLMs for cognitive planning and task decomposition
    """
    def __init__(self):
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for LLM planning service")

        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.LLM_MODEL

    async def create_plan_from_goal(self, goal: str, context: Optional[Dict[str, Any]] = None) -> LLMPlan:
        """
        Create an LLM plan from a high-level goal using cognitive planning
        """
        try:
            # Create the prompt for the LLM
            prompt = self._build_planning_prompt(goal, context)

            # Call the OpenAI API
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert robot task planner. Always return valid JSON for robot action sequences."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Low temperature for consistent, structured output
                max_tokens=1500,
                response_format={"type": "json_object"}  # Request JSON format
            )

            # Extract and parse the response
            content = response.choices[0].message.content
            plan_data = json.loads(content)

            # Create an LLMPlan object
            plan_id = f"plan_{uuid.uuid4().hex[:8]}"
            llm_plan = LLMPlan(
                id=plan_id,
                goal=goal,
                sub_tasks=plan_data.get("sub_tasks", []),
                generated_at=datetime.utcnow(),
                source_command=plan_data.get("source_command", "manual"),
                status="completed",
                error_message=None
            )

            logger.info(f"Successfully created LLM plan {plan_id} for goal: {goal}")
            return llm_plan

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing LLM response as JSON: {str(e)}")
            # Create a plan with error status
            plan_id = f"plan_{uuid.uuid4().hex[:8]}"
            return LLMPlan(
                id=plan_id,
                goal=goal,
                sub_tasks=[],
                generated_at=datetime.utcnow(),
                source_command="manual",
                status="failed",
                error_message=f"LLM response parsing error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Error creating LLM plan: {str(e)}")
            plan_id = f"plan_{uuid.uuid4().hex[:8]}"
            return LLMPlan(
                id=plan_id,
                goal=goal,
                sub_tasks=[],
                generated_at=datetime.utcnow(),
                source_command="manual",
                status="failed",
                error_message=str(e)
            )

    def _build_planning_prompt(self, goal: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Build the prompt for LLM-based planning
        """
        context_str = json.dumps(context, indent=2) if context else "No specific context provided"

        prompt = f"""
        You are a robot task planning expert. Decompose the following high-level goal into specific, executable sub-tasks.
        Consider the robot's capabilities and the provided environmental context.

        GOAL: {goal}

        ENVIRONMENTAL CONTEXT:
        {context_str}

        INSTRUCTIONS:
        1. Break down the goal into a sequence of specific, executable actions
        2. Each sub-task should have an action type, parameters, and description
        3. Consider physical constraints and environmental factors
        4. Include safety checks where appropriate
        5. Return the result as valid JSON

        REQUIRED JSON FORMAT:
        {{
            "sub_tasks": [
                {{
                    "action": "action_type",
                    "parameters": {{"param1": "value1", "param2": "value2"}},
                    "description": "Human-readable description of the action",
                    "required_capabilities": ["capability1", "capability2"]
                }}
            ],
            "source_command": "original_command_identifier"
        }}

        EXAMPLE:
        Goal: "Pick up the red cup and put it on the table"
        Response: {{
            "sub_tasks": [
                {{
                    "action": "locate_object",
                    "parameters": {{"object_type": "cup", "color": "red"}},
                    "description": "Find the red cup in the environment",
                    "required_capabilities": ["vision", "object_detection"]
                }},
                {{
                    "action": "navigate_to",
                    "parameters": {{"target": "red_cup_location", "approach_angle": 0.0}},
                    "description": "Move to the location of the red cup",
                    "required_capabilities": ["navigation"]
                }},
                {{
                    "action": "grasp_object",
                    "parameters": {{"object_id": "red_cup", "grasp_type": "top"}},
                    "description": "Pick up the red cup",
                    "required_capabilities": ["manipulation"]
                }},
                {{
                    "action": "navigate_to",
                    "parameters": {{"target": "table_location"}},
                    "description": "Move to the table",
                    "required_capabilities": ["navigation"]
                }},
                {{
                    "action": "place_object",
                    "parameters": {{"object_id": "red_cup", "location": "table", "placement_type": "center"}},
                    "description": "Place the red cup on the table",
                    "required_capabilities": ["manipulation"]
                }}
            ],
            "source_command": "user_command_123"
        }}

        Now create the plan for the provided goal:
        """

        return prompt

    async def validate_plan(self, plan: LLMPlan) -> tuple[bool, List[str]]:
        """
        Validate an LLM-generated plan for feasibility and safety
        """
        issues = []

        # Check if sub_tasks exist
        if not plan.sub_tasks:
            issues.append("Plan has no sub-tasks")

        # Validate each sub-task
        for i, task in enumerate(plan.sub_tasks):
            if not isinstance(task, dict):
                issues.append(f"Sub-task {i} is not a dictionary: {type(task)}")
                continue

            if "action" not in task:
                issues.append(f"Sub-task {i} missing 'action' field")

            if "parameters" not in task:
                issues.append(f"Sub-task {i} missing 'parameters' field")
            elif not isinstance(task["parameters"], dict):
                issues.append(f"Sub-task {i} parameters is not a dictionary")

            if "description" not in task:
                issues.append(f"Sub-task {i} missing 'description' field")

        is_valid = len(issues) == 0
        return is_valid, issues

    async def refine_plan(self, plan: LLMPlan, feedback: str) -> LLMPlan:
        """
        Refine an existing plan based on feedback
        """
        try:
            # Create a refinement prompt
            refinement_prompt = f"""
            You are refining a robot task plan based on feedback. The original goal was: {plan.goal}

            Original plan:
            {json.dumps(plan.sub_tasks, indent=2)}

            Feedback:
            {feedback}

            Please return an improved version of the plan that addresses the feedback.
            Return as valid JSON with the same structure as before.
            """

            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert robot task planner. Always return valid JSON for robot action sequences."
                    },
                    {
                        "role": "user",
                        "content": refinement_prompt
                    }
                ],
                temperature=0.1,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            refined_data = json.loads(content)

            # Create a new plan with refined sub-tasks
            refined_plan = LLMPlan(
                id=f"refined_{plan.id}",
                goal=plan.goal,
                sub_tasks=refined_data.get("sub_tasks", plan.sub_tasks),
                generated_at=datetime.utcnow(),
                source_command=plan.source_command,
                status="completed",
                error_message=None
            )

            logger.info(f"Successfully refined plan {plan.id}")
            return refined_plan

        except Exception as e:
            logger.error(f"Error refining plan: {str(e)}")
            return plan  # Return original plan if refinement fails