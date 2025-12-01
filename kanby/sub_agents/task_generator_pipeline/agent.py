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

"""Provides the sequential task planning pipeline combining multiple agents."""

from google.adk.agents import SequentialAgent

from .sub_agents.task_decomposer.agent import task_decomposer
from .sub_agents.task_dependency_mapper.agent import task_dependency_mapper
from .sub_agents.task_reviewer.agent import task_reviewer

# The final output is the review of the generated plan, however,
# the intermediate outputs are accessed from session state or by key templating.
task_generator_pipeline = SequentialAgent(
    name="task_generator_pipeline",
    description="Sequential pipeline that transforms text into reviewed task plans",
    sub_agents=[
        task_decomposer,
        task_dependency_mapper,
        task_reviewer,
    ],
)
