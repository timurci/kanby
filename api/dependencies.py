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

"""FastAPI dependencies."""

import os
from typing import Annotated

from fastapi import Depends

from api.schemas.users import User


async def get_current_user() -> User:
    """Retrieve the current user from a request context.

    Currently serves as a **placeholder** for future proper authentication logic.
    It always returns an unauthenticated 'guest' user object.
    """
    if os.getenv("KANBY_API_USER_AUTHENTICATION"):
        raise NotImplementedError
    return User(id="1")


CurrentUserDep = Annotated[User, Depends(get_current_user)]
