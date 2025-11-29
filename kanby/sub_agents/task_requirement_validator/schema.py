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

"""Pydantic schemas for requirement_validator agent."""

from enum import Enum

from pydantic import BaseModel, Field


class RequirementStatus(str, Enum):
    """Status of requirement validation."""

    CLEAR = "clear"
    NEEDS_CLARIFICATION = "needs_clarification"


class TaskRequirementValidatorOutput(BaseModel):
    """Output schema for requirement_validator agent.

    Contains validation status and questions if requirements need clarification.
    """

    status: RequirementStatus = Field(
        ...,
        description=(
            "Validation status: 'clear' if requirements are sufficient"
            " 'needs_clarification' if missing critical information"
        ),
    )

    questions: list[str] | None = Field(
        default=None,
        description="List of specific questions needed to clarify requirements.",
    )
