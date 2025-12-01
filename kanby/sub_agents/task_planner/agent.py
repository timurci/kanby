# Copyright 2025 Timur Çakmakoğlu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Provides the `task_planner` agent."""

from google.adk import Agent
from google.adk.tools import AgentTool

from kanby.sub_agents.task_generator_pipeline.agent import task_generator_pipeline
from kanby.sub_agents.task_requirement_validator.agent import (
    task_requirement_validator,
)

from .prompt import TASK_PLANNER_PROMPT

task_planner = Agent(
    model="gemini-2.5-flash",
    name="task_planner",
    description=(
        """
        Conversational task planner that orchestrates requirement validation and
        sequential task planning pipeline
        """
    ),
    instruction=TASK_PLANNER_PROMPT,
    tools=[
        AgentTool(agent=task_requirement_validator),
        AgentTool(agent=task_generator_pipeline),
    ],
)
