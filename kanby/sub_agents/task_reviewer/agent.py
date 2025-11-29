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

"""Provides the `task_reviewer` agent."""

from google.adk import Agent

from kanby.sub_agents.task_reviewer.prompt import TASK_REVIEWER_PROMPT
from kanby.sub_agents.task_reviewer.schema import (
    TaskReviewerInput,
    TaskReviewerOutput,
)

task_reviewer = Agent(
    model="gemini-2.5-flash",
    name="task_reviewer",
    description=(
        "Reviews task plans for logical consistency, circular dependencies, and"
        " optimization opportunities"
    ),
    instruction=TASK_REVIEWER_PROMPT,
    input_schema=TaskReviewerInput,
    output_schema=TaskReviewerOutput,
    output_key="task_reviewer",
)
