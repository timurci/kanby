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

"""Provides the `github_operator` agent."""

from google.adk import Agent

from .prompt import GITHUB_OPERATOR_PROMPT
from .tools import build_github_mcp_toolset

github_operator = Agent(
    model="gemini-2.5-flash",
    name="github_operator",
    description=(
        "The operational agent empowered with GitHub MCP. "
        "It manages access to GitHub Issues & Projects."
    ),
    instruction=GITHUB_OPERATOR_PROMPT,
    tools=[
        # Read-only access to GitHub MCP.
        build_github_mcp_toolset(
            github_toolsets=["context", "projects", "issues"],
            github_readonly=True,
            tool_filter=[
                # Context
                "get_me",
                "get_team_members",
                "get_teams",
                # Issues
                "get_label",
                "issue_read",
                "list_issues",
                "list_issue_types",
                "search_issues",
                # Projects
                "get_project",
                "get_project_field",
                "get_project_item",
                "list_project_fields",
                "list_project_items",
                "list_projects",
            ],
        ),
        # GitHub MCP tools with write access and requires HITL confirmation.
        build_github_mcp_toolset(
            github_toolsets=["projects", "issues"],
            require_confirmation=True,
            tool_filter=[
                # Issues
                "add_issue_comment",
                "assign_copilot_to_issue",
                "issue_write",
                "sub_issue_write",
                # Projects
                "add_project_item",
                "delete_project_item",
                "update_project_item",
            ],
        ),
    ],
)
