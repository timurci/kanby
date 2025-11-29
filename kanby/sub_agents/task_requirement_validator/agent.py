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

"""Provides the `task_requirement_validator` agent."""

from google.adk import Agent

from .prompt import TASK_REQUIREMENT_VALIDATOR_PROMPT
from .schema import TaskRequirementValidatorOutput

task_requirement_validator = Agent(
    model="gemini-2.5-flash",
    name="task_requirement_validator",
    description=(
        "Validates clarity and completeness of project specifications,"
        " forwards questions if there is ambiguity."
    ),
    instruction=TASK_REQUIREMENT_VALIDATOR_PROMPT,
    output_schema=TaskRequirementValidatorOutput,
    output_key="task_requirement_validator",
)
