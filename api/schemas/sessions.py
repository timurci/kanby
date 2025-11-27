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

"""Provides models for managing ADK sessions and agent interactions."""

from typing import Any

from google.adk.agents.run_config import RunConfig
from google.genai.types import Content
from pydantic import BaseModel, Field


class AgentQuery(BaseModel):
    """Payload that is used to send a query or continuation request to an ADK agent."""

    invocation_id: str | None = Field(
        default=None, description="Invocation ID to resume an interrupted invocation"
    )
    new_message: Content | None = None
    state_delta: dict[str, Any] | None = None
    run_config: RunConfig | None = None
