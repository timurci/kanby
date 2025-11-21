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

"""Logging plugin Implement guardrails, monitoring, etc."""

import logging

from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.plugins.base_plugin import BasePlugin

logger = logging.getLogger(__name__)


class LoggingPlugin(BasePlugin):
    """A custom plugin that logs contextual agent and model invocations."""

    def __init__(self) -> None:
        """Initialize the plugin."""
        super().__init__(name="logging_plugin")

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """Log agent run details with context."""
        logger.info("[Plugin] callback_context: %s", callback_context)
        logger.info(
            "[Plugin] Agent run started.",
            extra={
                "event_type": "agent_start",
                "agent_name": agent.name,
            },
        )

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> None:
        """Log LLM request details with context."""
        logger.info("[Plugin] callback_context: %s", callback_context)
        logger.debug("[Plugin] LLM request initiated. %s", llm_request)
