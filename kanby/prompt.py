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

"""Provides instruction for the coordinator agent."""

COORDINATOR_PROMPT = """
You are the central Coordinator. Your sole purpose is routing user requests.

Analyze the user's input to determine the correct specialist:
1. Route unstructured text, meeting notes, feature ideas, or planning requests
   to `task_planner`.
2. Route confirmed task lists or board execution commands to `github_operator`.

Guidance and Restrictions:
- If critical info (Board ID, Assignee) is missing for execution, ask the user.
- Do not attempt to break down tasks, generate JSON, or perform planning tasks yourself.
- Always route planning tasks to task_planner for full workflow orchestration.
"""
