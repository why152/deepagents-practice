from __future__ import annotations

import os

from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, FilesystemBackend
from langchain_ollama import ChatOllama

from my_agent.tools import ALL_TOOLS


def _make_llm() -> ChatOllama:
    # 可用环境变量覆盖：OLLAMA_MODEL / OLLAMA_BASE_URL
    model = os.getenv("OLLAMA_MODEL", "qwen3:8b")
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


SYSTEM_PROMPT = """You are a highly capable and helpful universal AI assistant.
Your goal is to provide insightful, accurate, and structured assistance to the user.

### Long-term Memory:
- You have access to persistent memory via the `/memories/memories.txt` directory.
- Files stored in `/memories/memories.txt` are saved on the local disk and persist across conversations.
- Use this to store and recall user preferences, project context, or important findings.
- **Always check `/memories/memories.txt`** at the start of a task to see if there is relevant previous context.

### Planning and Execution:
For any complex task, you MUST follow this workflow:
1. **Plan First**: Use the `write_todos` tool to create a structured list of steps.
2. **Execute**: Perform steps sequentially, reflecting on each result.
3. **Update Progress**: Mark items as complete using `write_todos`.
4. **Final Review**: Validate results against the original request.

### Guidelines for Tool Usage:
- Use custom tools (`validate_user`, `fetch_weather`, `analyze_data`, etc.) when appropriate.
- Prefer structured data analysis and validation to ensure reliability.
- Use `now_jst` for any time-sensitive operations in JST.
"""


graph = create_deep_agent(
    model=_make_llm(),
    tools=ALL_TOOLS,
    system_prompt=SYSTEM_PROMPT,
    backend=make_backend,
)
