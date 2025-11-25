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

"""Provides `root_agent` (coordinator) and `app`."""

import logging

from google.adk import Agent
from google.adk.apps import App, ResumabilityConfig

from kanby.prompt import COORDINATOR_PROMPT
from kanby.sub_agents.github_operator.agent import github_operator
from kanby.sub_agents.task_decomposer.agent import task_decomposer

from .plugins.logging import LoggingPlugin

logger = logging.getLogger(__name__)

logger.debug("Logging system initialized successfully.")

root_agent = Agent(
    model="gemini-2.5-flash",
    name="coordinator",
    description="The root agent responsible for intent detection and routing",
    instruction=COORDINATOR_PROMPT,
    sub_agents=[task_decomposer, github_operator],
)

app = App(
    name="kanby",
    root_agent=root_agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
    plugins=[LoggingPlugin()]
)
