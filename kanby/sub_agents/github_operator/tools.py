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

"""Provides tools for the GitHub operator agent."""

import logging
import os

from dotenv import load_dotenv
from google.adk.tools import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

logger = logging.getLogger(__name__)


def get_github_pat(key: str = "GITHUB_PERSONAL_ACCESS_TOKEN") -> str | None:
    """Retrieve a GitHub personal access token from the environment.

    First checks `os.environ`. If not found, loads the local `.env` file and retries.

    Args:
        key: Environment variable name for the token.

    Returns:
        The GitHub personal access token, or `None` if it is not set.
    """
    token = os.getenv(key, None)

    if token is None:
        logger.warning(
            "Environment variable '%s' was not found. Attempting to load `.env`.", key
        )
        load_dotenv()
        token = os.getenv(key, None)

    return token


def build_github_mcp_toolset(
    github_toolsets: list[str] | None = None,
    github_readonly: bool | None = None,  # noqa: FBT001 # Specific to GitHub API.
    **kwargs,  # noqa: ANN003 # Directly passed to a well-documented function.
) -> McpToolset:
    """Build an McpToolset for GitHub MCP server.

    By default, reads the authorization token from `GITHUB_PERSONAL_ACCESS_TOKEN`
    (loaded from `.env` if not present in the environment). To customize this,
    provide a `header_provider` via `**kwargs` for dynamic token retrieval
    using `ToolContext`. See `McpToolset` for details.

    Args:
        github_toolsets: Whitelist of GitHub toolsets to enable.
            See GitHub MCP documentation for valid values.
        github_readonly: If `True`, expose only read-only tools.
        **kwargs: Additional arguments passed to `McpToolset`.
    """
    static_headers: dict[str, str] = {"Authorization": f"Bearer {get_github_pat()}"}

    if github_readonly is not None:
        static_headers.update({"X-MCP-Readonly": str(github_readonly).lower()})
    if github_toolsets is not None:
        static_headers.update({"X-MCP-Toolsets": ",".join(github_toolsets)})

    return McpToolset(
        connection_params=StreamableHTTPServerParams(
            url="https://api.githubcopilot.com/mcp/",
            headers=static_headers,
        ),
        **kwargs,
    )
