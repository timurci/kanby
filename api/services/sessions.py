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

"""Service to manage ADK sessions and agent interactions."""

from typing import Any
from uuid import UUID

from google.adk import Runner
from google.adk.sessions import (
    BaseSessionService,
    DatabaseSessionService,
    InMemorySessionService,
    Session,
)
from google.adk.sessions.base_session_service import ListSessionsResponse
from google.genai.types import Content

from api.core.config import SESSION_SERVICE_URI
from api.schemas.sessions import AgentQuery
from api.schemas.users import User
from kanby.agent import app as kanby_app


class SessionNotFoundError(Exception):
    """Exception raised when a user session cannot be found in SessionService."""

    def __init__(self, user_id: str, session_id: str) -> None:
        """Initialize the error with user and session identifiers."""
        super().__init__(f"Session '{session_id}' not found for user '{user_id}'")


def _init_adk_session_service() -> BaseSessionService:
    if SESSION_SERVICE_URI is None:
        return InMemorySessionService()
    return DatabaseSessionService(db_url=SESSION_SERVICE_URI)


class SessionService:
    """This class manages ADK SessionService for Kanby."""

    adk_runner = Runner(
        app=kanby_app,
        session_service=_init_adk_session_service(),
    )

    @classmethod
    async def list_sessions(cls, user: User) -> ListSessionsResponse:
        """List all sessions created by user."""
        return await cls.adk_runner.session_service.list_sessions(
            app_name=cls.adk_runner.app_name, user_id=user.id
        )

    @classmethod
    async def create_session(
        cls, user: User, initial_state: dict[str, Any] | None = None
    ) -> Session:
        """Create a session for the user.

        Args:
            user: Target user.
            initial_state: Initial session state.
        """
        return await cls.adk_runner.session_service.create_session(
            app_name=cls.adk_runner.app_name,
            user_id=user.id,
            state=initial_state,
        )

    @classmethod
    async def get_session(cls, user: User, session_id: UUID) -> Session:
        """Retrieve a session history for the user."""
        session = await cls.adk_runner.session_service.get_session(
            app_name=cls.adk_runner.app_name,
            user_id=user.id,
            session_id=str(session_id),
        )
        if session is None:
            raise SessionNotFoundError(user.id, str(session_id))
        return session

    @classmethod
    async def delete_session(cls, user: User, session_id: UUID) -> None:
        """Delete a session for the user."""
        return await cls.adk_runner.session_service.delete_session(
            app_name=cls.adk_runner.app_name,
            user_id=user.id,
            session_id=str(session_id),
        )

    @classmethod
    async def run_agent(
        cls, user: User, session_id: UUID, query: AgentQuery
    ) -> Content | None:
        """Run an event in ADK runtime."""
        events = cls.adk_runner.run_async(
            user_id=user.id,
            session_id=str(session_id),
            new_message=query.new_message,
            invocation_id=query.invocation_id,
            state_delta=query.state_delta,
            run_config=query.run_config,
        )

        async for event in events:
            if event.is_final_response():
                return event.content

        return None
