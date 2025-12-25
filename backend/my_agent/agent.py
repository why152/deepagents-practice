from __future__ import annotations

import os

from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, FilesystemBackend
from langchain_ollama import ChatOllama

from my_agent.tools import ALL_TOOLS


def _make_llm() -> ChatOllama:
    # 可用环境变量覆盖：OLLAMA_MODEL / OLLAMA_BASE_URL
    model = os.getenv("OLLAMA_MODEL", "qwen3:0.6b")
    base_url = os.getenv("OLLAMA_BASE_URL")  # e.g. http://127.0.0.1:11434

    kwargs = {
        "model": model,
        "temperature": 0,
    }
    if base_url:
        kwargs["base_url"] = base_url

    return ChatOllama(**kwargs)


# --- Long-term Memory Configuration ---
# Ensure the memory directory exists at module import time (startup)
# This prevents BlockingError when running in the async event loop
MEMORY_DIR = os.path.join(os.getcwd(), "long_term_memory")
if not os.path.exists(MEMORY_DIR):
    os.makedirs(MEMORY_DIR)


# Configure CompositeBackend:
# - Default: StateBackend (ephemeral files)
# - /memories/: FilesystemBackend (persistent files on local disk)
def make_backend(runtime):
    return CompositeBackend(
        default=StateBackend(runtime),
        routes={
            "/memories/": FilesystemBackend(root_dir=MEMORY_DIR)
        },
    )


SYSTEM_PROMPT = """You are a highly capable and helpful universal AI assistant Acting as a PLANNER.
Your goal is to provide insightful, accurate, and structured assistance to the user by PLANNING tasks and DELEGATING them to your executor sub-agent.

### Long-term Memory:
- You have access to persistent memory via the `/memories/memories.txt` directory.
- Files stored in `/memories/memories.txt` are saved on the local disk and persist across conversations.
- Use this to store and recall user preferences, project context, or important findings.
- **Always check `/memories/memories.txt`** at the start of a task to see if there is relevant previous context.

### Planning and Execution Workflow:
For any complex task, you MUST follow this workflow:
1. **Plan**: Use the `write_todos` tool to create a structured list of steps.
2. **Delegate**: Use the `task` tool to delegate execution of specific steps to the `executor` subagent. 
   - The `executor` has access to all the actual tools (weather, calculations, data analysis, etc.).
   - Pass clear, context-rich instructions to the `executor`.
3. **Review**: Check the output of the `executor` and update your todo list.
4. **Finalize**: When all steps are complete, provide the final answer to the user.

### Guidelines:
- **DO NOT** try to execute specific tools (like `now_jst` or `add`) yourself. You do not have them. DELEGATE them.
- You ONLY have access to planning tools (`write_todos`) and delegation (`task`).
"""


# Define the Executor Sub-agent
# This agent has the actual tools to do the work.
executor_subagent = {
    "name": "executor",
    "description": "A sub-agent capable of executing specific tools like weather checking, calculations, data analysis, etc.",
    "system_prompt": "You are a precise executor. Your job is to strictly follow instructions, execute tools, and return the results. Do not plan; just do.",
    "tools": ALL_TOOLS, 
}


agent = create_deep_agent(
    model=_make_llm(),
    tools=[], # Main agent only has built-in methodology tools (todos, file ops, etc.)
    subagents=[executor_subagent],
    system_prompt=SYSTEM_PROMPT,
    backend=make_backend,
)
