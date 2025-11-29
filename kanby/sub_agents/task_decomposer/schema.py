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

"""Pydantic schemas for task_decomposer agent."""

from typing import ClassVar

from pydantic import BaseModel, Field


class TaskItem(BaseModel):
    """Individual task item for task decomposition output.

    Base class containing common task fields used across the task planning workflow.
    """

    title: str = Field(..., description="Verb-Noun task title")
    description: str = Field(..., description="Detailed acceptance criteria")


class TaskDecomposerOutput(BaseModel):
    """Output schema for task_decomposer agent.

    Contains either decomposed tasks or clarification questions based on input clarity.
    This is the first stage in the task planning workflow.
    """

    tasks: list[TaskItem] | None = Field(
        default=None, description="List of decomposed tasks if requirements are clear"
    )
    clarification_questions: list[str] | None = Field(
        default=None,
        description="List of clarification questions if requirements are vague",
    )

    class Config:
        """Model configuration."""

        json_schema_extra: ClassVar[dict[str, str]] = {
            "description": "Either tasks OR clarification_questions provided"
        }
