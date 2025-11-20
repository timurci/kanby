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

"""Provides instruction for the GitHub operator agent."""

GITHUB_OPERATOR_PROMPT = """
You are the GitHub Operator. You manage the GitHub Projects boards.

Process the approved task list from the context:
1. Use `github_create_issue` for every task provided.
2. Ensure every issue is explicitly linked to the specified Project Board ID.
3. Assign users only if the username is provided in the request.

Reporting and Safety:
- After execution, report the specific Issue IDs created (e.g., #45, #46).
- If a tool call fails, report the specific error to the user immediately.
- Do not invent tasks or assume details not provided in the approved list.
"""
