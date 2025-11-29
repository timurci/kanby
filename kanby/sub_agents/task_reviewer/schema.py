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

"""Pydantic schemas for task_reviewer agent."""

from enum import Enum

from pydantic import BaseModel, Field


class TaskReviewFindingType(str, Enum):
    """Enum for task review finding types in task planning workflow."""

    CIRCULAR_DEPENDENCY = "circular_dependency"  # Critical: breaks execution flow
    MISSING_DEPENDENCY = "missing_dependency"  # High: incomplete plan
    OPTIMIZATION = "optimization"  # Medium: parallelization opportunities
    WARNING = "warning"  # Low: quality concerns (large tasks, unclear, duplicates)


class TaskReviewSeverity(str, Enum):
    """Enum for task review severity levels."""

    CRITICAL = "critical"  # Blocks execution (e.g., circular dependencies)
    HIGH = "high"  # Major issues requiring immediate attention
    MEDIUM = "medium"  # Important improvements and optimizations
    LOW = "low"  # Minor quality warnings


class TaskReviewStatus(str, Enum):
    """Enum for overall task review status."""

    APPROVED = "approved"  # No issues found, ready to proceed
    NEEDS_CHANGES = "needs_changes"  # Medium/high priority findings to address
    CRITICAL_ISSUES = "critical_issues"  # Critical blockers preventing execution


class TaskReviewFinding(BaseModel):
    """Individual finding from task plan review in task planning workflow."""

    type: TaskReviewFindingType = Field(..., description="Type of finding")
    severity: TaskReviewSeverity = Field(
        ..., description="Severity level of the finding"
    )
    task_id: int | None = Field(
        default=None, description="ID of task related to this finding if applicable"
    )
    description: str = Field(..., description="Detailed description of the issue")
    suggestion: str = Field(..., description="Suggested fix or improvement")


class PlanReview(BaseModel):
    """Output schema for task_reviewer agent.

    Contains review status, fingings and recommendations.
    """

    review_status: TaskReviewStatus = Field(..., description="Overall review status")
    findings: list[TaskReviewFinding] = Field(
        ..., description="List of findings from the review"
    )
    optimized_order: list[int] | None = Field(
        default=None,
        description="Suggested optimal task execution order as list of task IDs",
    )
    summary: str = Field(..., description="Brief summary of review results")
