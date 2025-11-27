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

"""Provides models defining the user entity for the application."""

import uuid

from pydantic import BaseModel, Field


class User(BaseModel):
    """Represents an API consumer."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    display_name: str = "guest"
    authenticated: bool = False
