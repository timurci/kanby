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

from pydantic import BaseModel, Field


class TaskItem(BaseModel):
    """Individual task item for task decomposition output.

    Base class containing common task fields used across the task planning workflow.
    """

    id: int = Field(..., description="Sequential task ID start from 1")
    title: str = Field(..., description="Verb-Noun task title")
    description: str = Field(..., description="Task description")
    acceptance_criteria: list[str] = Field(..., description="Task acceptance critera")


class TaskList(BaseModel):
    """Contains list of tasks."""

    tasks: list[TaskItem] = Field(..., description="List of decomposed tasks")
