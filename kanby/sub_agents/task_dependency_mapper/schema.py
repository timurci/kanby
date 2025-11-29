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

"""Pydantic schemas for task_dependency_mapper agent."""

from enum import Enum

from pydantic import BaseModel, Field

from kanby.sub_agents.task_decomposer.schema import TaskItem


class TaskDependencyType(str, Enum):
    """Enum for task dependency types in task planning workflow."""

    HARD = "hard"  # Task B cannot start until Task A completes (blocking)
    SOFT = "soft"  # Task B benefits from Task A but can run in parallel


class TaskItemWithId(TaskItem):
    """Task with assigned ID for task dependency mapping.

    Extends TaskItem with an ID field for dependency tracking in the task planning
    workflow. Used by task_dependency_mapper to assign sequential IDs to tasks.
    """

    id: int = Field(..., description="Sequential task ID starting from 1")


class TaskDependency(BaseModel):
    """Dependency relationship between two tasks in task planning workflow."""

    from_task: int = Field(..., alias="from", description="ID of prerequisite task")
    to_task: int = Field(..., alias="to", description="ID of dependent task")
    type: TaskDependencyType = Field(
        ...,
        description="Dependency type: hard=blocking, soft=preferred order",
    )

    class Config:
        """Model configuration."""

        populate_by_name = True  # Allow using both field name and alias


class TaskDependencyMapperInput(BaseModel):
    """Input schema for task_dependency_mapper agent.

    Accepts tasks from task_decomposer for dependency analysis.
    """

    tasks: list[TaskItem]


class TaskDependencyMapperOutput(BaseModel):
    """Output schema for task_dependency_mapper agent.

    Contains tasks with sequential IDs and their dependency relationships.
    This is the second stage in the task planning workflow after decomposition.
    """

    tasks: list[TaskItemWithId] = Field(
        ..., description="Tasks with assigned sequential IDs"
    )
    dependencies: list[TaskDependency] = Field(
        ..., description="List of dependencies between tasks"
    )
