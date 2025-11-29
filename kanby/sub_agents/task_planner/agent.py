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

from kanby.sub_agents.task_decomposer.agent import task_decomposer
from kanby.sub_agents.task_dependency_mapper.agent import task_dependency_mapper
from kanby.sub_agents.task_planner.prompt import TASK_PLANNER_PROMPT
from kanby.sub_agents.task_requirement_validator.agent import task_requirement_validator
from kanby.sub_agents.task_reviewer.agent import task_reviewer

task_planner = Agent(
    model="gemini-2.5-flash",
    name="task_planner",
    description=(
        """
        Conversational task planner that orchestrates requirement validation,
        task decomposition, dependency mapping, and plan review
        """
    ),
    instruction=TASK_PLANNER_PROMPT,
    tools=[
        AgentTool(agent=task_requirement_validator),
        AgentTool(agent=task_decomposer),
        AgentTool(agent=task_dependency_mapper),
        AgentTool(agent=task_reviewer),
    ],
)
