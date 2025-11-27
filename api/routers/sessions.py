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

"""API endpoints to manage ADK sessions and send queries to agents."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from google.adk.sessions import Session
from google.adk.sessions.base_session_service import ListSessionsResponse
from google.genai.types import Content

from api.dependencies import CurrentUserDep
from api.schemas.sessions import AgentQuery
from api.services.sessions import SessionNotFoundError, SessionService

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("/")
async def list_sessions(user: CurrentUserDep) -> ListSessionsResponse:
    """List all sessions created by user."""
    return await SessionService.list_sessions(user)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_session(user: CurrentUserDep) -> Session:
    """Create a session for the user."""
    return await SessionService.create_session(user)


@router.get("/{session_id}")
async def get_session(user: CurrentUserDep, session_id: UUID) -> Session:
    """Retrieve a session history for the user."""
    try:
        return await SessionService.get_session(user, session_id)
    except SessionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.delete("/{session_id}")
async def delete_session(user: CurrentUserDep, session_id: UUID) -> None:
    """Delete a session for the user."""
    try:
        return await SessionService.delete_session(user, session_id)
    except SessionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.post("/{session_id}")
async def run_agent(
    user: CurrentUserDep, session_id: UUID, query: AgentQuery
) -> Content | None:
    """Send query or response to the agent."""
    try:
        return await SessionService.run_agent(user, session_id, query)
    except SessionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
