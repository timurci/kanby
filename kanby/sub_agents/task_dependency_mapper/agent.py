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

"""Provides the `task_dependency_mapper` agent."""

from google.adk import Agent

from kanby.sub_agents.task_dependency_mapper.prompt import DEPENDENCY_MAPPER_PROMPT
from kanby.sub_agents.task_dependency_mapper.schema import (
    TaskDependencyMapperInput,
    TaskDependencyMapperOutput,
)

task_dependency_mapper = Agent(
    model="gemini-2.5-flash",
    name="task_dependency_mapper",
    description=(
        "Maps dependencies between tasks and determines optimal execution order"
    ),
    instruction=DEPENDENCY_MAPPER_PROMPT,
    input_schema=TaskDependencyMapperInput,
    output_schema=TaskDependencyMapperOutput,
    output_key="task_dependency_mapper",
)
